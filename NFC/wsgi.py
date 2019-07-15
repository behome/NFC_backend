"""
WSGI config for NFC project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
from os.path import join, dirname, abspath
from django.core.wsgi import get_wsgi_application
PROJECT_DIR = dirname(dirname(abspath(__file__)))
import sys
sys.path.append("/var/www/html/NFC_v1.1/")

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NFC.settings")
os.environ["DJANGO_SETTINGS_MODULE"] = "NFC.settings"
application = get_wsgi_application()
