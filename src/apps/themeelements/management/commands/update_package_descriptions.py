from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
import operator
from contentitems.themeelements.models import PackageItem


class Command(BaseCommand):
    help = "Update the PackageItem descriptions with the latest GitHub summaries and RTD urls."
    args = "[optional URLs to match, ..]"

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity'))

        packages = PackageItem.objects.all()
        if args:
            query = reduce(operator.or_, (Q(repository_url__contains=arg) for arg in args))
            packages = packages.filter(query)

        if not packages:
            if verbosity >= 1:
                raise CommandError("No packages matching {0}\n".format(' | '.join(args)))

        for package in packages:
            changed = False

            # Update GitHub
            new_summary = package.github_description
            if new_summary and new_summary != package.description:
                old_summary = package.description
                package.description = new_summary
                changed = True

                if verbosity >= 1:
                    self.stderr.write("Updated: {0} ({0} => {1})\n".format(package.slug, old_summary, new_summary))

            # Update RTD
            new_rtd_subdomain = package.rtd_subdomain
            if new_rtd_subdomain and new_rtd_subdomain != package.rtd_html_url:
                old_rtd_subdomain = package.rtd_html_url
                package.rtd_html_url = new_rtd_subdomain
                changed = True

                if verbosity >= 1:
                    self.stderr.write("Updated: {0} ({0} => {1})\n".format(package.slug, old_rtd_subdomain, new_rtd_subdomain))

            if changed:
                package.save()
            else:
                if verbosity >= 1:
                    self.stderr.write("Identical: {0}.\n".format(package.slug))
