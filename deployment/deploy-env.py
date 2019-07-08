#!/usr/bin/env python3
import atexit
import json
import os
import sys
from http.client import HTTPResponse
from tempfile import TemporaryDirectory

from ssl import SSLError
from typing import cast
from urllib.error import HTTPError
from urllib.request import urlopen, Request

from time import sleep

import argparse
import subprocess
from configparser import ConfigParser

# Brief implementation (based on termcolor / django's supports_color())
has_colors = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
GREEN = "\033[32m" if has_colors else ""
RESET = "\033[0m" if has_colors else ""

STATUS_RESOURCES = (
    "pods",
    "jobs",
    "services",
    "deployments",
    "persistentvolumeclaims",
    "configmaps",
    "secrets",
    "ingress",
)


def main():
    os.chdir(os.path.dirname(__file__))
    config = ConfigParser()
    config.read("deploy-env.ini")

    parser = argparse.ArgumentParser(
        description="" "Deploy to a Kubernetes cluster using kustomize.\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "environment",
        metavar="environment",
        choices=config.sections(),
        help="Environment name, as section in deploy-env.ini",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Output what would be deployed"
    )
    parser.add_argument(
        "--server-dry-run",
        action="store_true",
        help="Only check whether the server would accept the YAML",
    )
    parser.add_argument(
        "images",
        metavar="image",
        nargs="*",
        help="Image substitution to deploy (format: name=registry/name:tag)",
    )
    parser.add_argument(
        "--wait-for",
        help="Text to expect at the healthcheck endpoint to detect a successful deployment.",
    )
    args = parser.parse_args()

    # Read the INI file, start deployment
    settings = config[args.environment]
    try:
        start_deployment(
            settings,
            images=args.images,
            dry_run=args.dry_run,
            server_dry_run=args.server_dry_run,
            wait_for=args.wait_for,
        )
    except subprocess.CalledProcessError as e:
        print(str(e), file=sys.stderr)
        exit(e.returncode)


def start_deployment(
    settings, images=None, dry_run=False, server_dry_run=False, wait_for=None
):
    """Perform the complete deployment"""
    try:
        release_name = settings["name"]
        namespace = settings["namespace"]
        label_selector = settings["labels"]
        kustomize = settings["kustomize"]
        healthcheck = settings["healthcheck"]
        job = settings.get("job")
    except KeyError:
        print("Missing settings in INI file!", file=sys.stderr)
        exit(1)
        return  # for pycharm

    # Set the image
    if images:
        kustomize = _create_tmp_customize(
            bases=[kustomize], prefix=kustomize.replace(os.path.sep, "-") + "-"
        )
        subprocess.run(
            ["kustomize", "edit", "set", "image"] + images, cwd=kustomize, check=True
        )

    # Generate the yaml contents. As this is reused several times,
    # there is no need to setup pipes with subprocess.Popen
    yaml_data = subprocess.run(
        ["kustomize", "build", kustomize, "--reorder", "none"],
        stdout=subprocess.PIPE,
        check=True,
    ).stdout
    if dry_run:
        print(yaml_data.decode())
        if not server_dry_run:
            return

    # Remove old job
    if job:
        print(green("Removing old job {} from {}:".format(job, namespace)), flush=True)
        delete_resources(namespace, 'job', job)
        print("")

    # Validate the kustomize output against the API server
    # This checks whether the deployment would break (e.g. due to immutable fields)
    print(green("Validating yaml with server-dry-run:"), flush=True)
    subprocess.run(
        ["kubectl", "apply", "-f", "-", "--server-dry-run"], input=yaml_data, check=True
    )
    print("")

    # Fetch previous configuration that we applied to the server.
    # old_yaml_data = get_previous_release(yaml_data)

    # Apply new yaml config
    # The "kustomize build | kubectl apply -f -" approach allows to use kustomize 2.1,
    # where as "kubectl apply --kustomize" uses kustomize 2.0 in kubectl 1.14.
    print(green("Deploying {} to {}:".format(release_name, namespace)), flush=True)
    subprocess.run(
        ["kubectl", "apply", "-f", "-", "--namespace", namespace, "--record"],
        input=yaml_data,
        check=True,
    )
    if server_dry_run:
        return

    # Show progress
    sleep(1)
    print("")
    print(green("Objects created in {}:".format(namespace)), flush=True)
    show_kube_resources(namespace, label_selector=label_selector)

    # Wait for the deployment to come up. There are many reasons why a deployment fails:
    # - ingress config invalid
    # - service config invalid
    # - missing priorityclasses, secrets, etc..
    # - image pull issues
    # - crashing containers due to wrong db credentials or resource limits.
    #
    # These can't be all accounted for, but testing for a healthcheck to return
    # the latest git hash is a pretty close to catch all of these.
    try:
        wait_until_healthy(
            healthcheck, release_name=release_name, expected_data=wait_for
        )
    except KeyboardInterrupt:
        print("Aborted")
        exit(1)
    except OSError as e:
        print("Deployment failed: {e}".format(e=e))
        exit(1)

        # if old_yaml_data:
        #     perform_rollback(old_yaml_data)
        #     print("Performing rollback")
        #     subprocess.run(
        #         ["kubectl", "apply", "-f", "-"],
        #         input=old_yaml_data,
        #         check=True,
        #     )


def delete_resources(namespace, *objects):
    """Delete a job"""
    subprocess.run(
        [
            "kubectl",
            "delete",
            "job",
            "--namespace",
            namespace,
            "--ignore-not-found",
            "--wait=false",
            "--now",
            *objects,
        ],
        check=True,
    )


def purge_deployment(namespace, label_selector):
    """Delete all resources matching a label selector"""
    delete_resources(namespace, '--selector', label_selector)


def show_kube_resources(namespace, label_selector):
    """Output the status of various objects.."""
    # Fetch in a single command
    all_output = subprocess.run(
        [
            "kubectl",
            "get",
            ",".join(STATUS_RESOURCES),
            "--namespace",
            namespace,
            "--selector",
            label_selector,
            "-o",
            "wide",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    ).stdout.decode()

    # While printing, remove objecttype.foo/ prefix from names
    header = None
    for line in all_output.splitlines():
        if line.startswith("NAME "):
            header = line
        elif line:
            resource_type, line = line.split("/", 1)
            if header:
                print("\xa0")  # for GKE
                print(resource_type.split(".", 1)[0].upper())
                print("NAME" + header[len(resource_type) + 5 :].replace(' ', '\xa0'))
                header = None
            print(line)
    print("")


def get_previous_release(yaml_data):
    """Retrieve the previous released configuration"""
    try:
        result = subprocess.run(
            ["kubectl", "get", "-f", "-", "-o", "json"],
            input=yaml_data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        # Ignore resources which are not found, see if there are any errors left.
        errors = [
            line for line in e.stderr.decode().split("\n") if not "(NotFound)" in line
        ]
        if errors:
            print("\n".join(errors), file=sys.stderr)
            exit(1)
            return None  # for PyCharm
        else:
            return None

    return result.stdout


def green(text):
    """Apply text coloring"""
    return "{}{}{}".format(GREEN, text, RESET) if GREEN else text


def _create_tmp_customize(bases, prefix=None):
    """Create a temporary """

    temp_dir = TemporaryDirectory(prefix=prefix)

    # kustomize only recognizes relative paths, so convert that
    bases = [os.path.abspath(base) for base in bases]
    bases = [os.path.relpath("/", base) + base for base in bases]

    with open(
        os.path.join(temp_dir.name, "kustomization.yaml"), "w", encoding="utf-8"
    ) as f:
        f.write(
            "apiVersion: kustomize.config.k8s.io/v1beta1\n"
            "kind: Kustomization\n"
            "\n"
            "resources: {}\n".format(json.dumps(bases))
        )

    # Ensure a reference exists until the program exits.
    atexit.register(temp_dir.cleanup)
    return temp_dir.name


def wait_until_healthy(check_url, release_name, expected_data=None):
    """Wait until the URL endpoint returns the expected response."""
    if expected_data:
        print("Checking for", expected_data)
        expected_data = expected_data.encode()
    print("Checking deployment status at", check_url, end=" ", flush=True)

    request = Request(check_url, headers={"User-Agent": "deploy-env"})
    seen_regular = False
    for i in range(120):
        error = None
        try:
            response = cast(HTTPResponse, urlopen(request))
        except OSError as e:
            error = e
        else:
            received_data = response.read()
            if not expected_data or expected_data in received_data:
                print(
                    (
                        "got {status}\n"
                        "Successfully deployed {release_name} after {i} seconds"
                    ).format(status=response.status, release_name=release_name, i=i)
                )
                return
            elif not seen_regular:
                print(
                    "got {status}, waiting for right content".format(
                        status=response.status
                    ),
                    end="",
                )
                seen_regular = True

        if error is not None and i >= 60:
            if isinstance(error, HTTPError) and int(error.code) >= 400:
                # Only allow 400/401/403/500/503 for a while, as it could be
                # caused by a configuration error of the previous deployment.
                raise TimeoutError(
                    "Still receiving HTTP {code} after {i} seconds".format(
                        code=error.code, i=i
                    )
                ) from None
            elif isinstance(error, SSLError):
                raise TimeoutError(
                    "Still receiving SSL errors after {i} seconds: {e}".format(
                        e=error, i=i
                    )
                ) from None
            elif seen_regular:
                raise IOError(
                    "Got error with new configuration after {i} seconds: {e}".format(
                        e=error, i=i
                    )
                ) from None

        print(".", end="", flush=True)
        sleep(1)

    raise TimeoutError("Deployment still isn't online!")


if __name__ == "__main__":
    main()
