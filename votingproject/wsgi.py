"""
WSGI config for votingproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'votingproject.settings')

# Must call setup() before any django commands
django.setup()

from django.core.management import call_command
try:
    call_command('migrate', '--run-syncdb', verbosity=0)
except Exception as e:
    print(f"Migration error: {e}")

application = get_wsgi_application()
