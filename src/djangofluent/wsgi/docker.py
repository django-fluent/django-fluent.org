from django.core.wsgi import get_wsgi_application
from netaddr import IPNetwork
from wsgiunproxy import unproxy

# Export application object with WSGI middleware
# Allow X-Forwarded-For from Kubernetes ingress
application = get_wsgi_application()
application = unproxy(trusted_proxies=IPNetwork('192.168.0.0/16'))(application)
