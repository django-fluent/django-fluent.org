import os

from django.core.wsgi import get_wsgi_application
from netaddr import IPNetwork
from wsgiunproxy import unproxy

# Export application object with WSGI middleware
# Allow X-Forwarded-For from Kubernetes ingress
trusted_cidr = os.environ.get("ALLOWED_CIDR_NETS", "10.0.0.0/8")
application = get_wsgi_application()
application = unproxy(trusted_proxies=IPNetwork(trusted_cidr))(application)
