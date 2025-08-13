import sys
import os

sys.path.insert(0, '/home2/colorspr/django_project')
sys.path.insert(0, '/home2/colorspr/django_project/greensteps')

os.environ['DJANGO_SETTINGS_MODULE'] = 'greensteps.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()