# ---------------------------- CKEDITOR

ckeditor_settings = """\n
\n#CKEDITOR
CKEDITOR_BASEPATH = '/static/ckeditor/ckeditor/'
CKEDITOR_UPLOAD_PATH = 'uploads/'
"""

# ---------------------------- BASIC RENDER VIEW

basic_template_view = """\n
from django.views.generic import TemplateView
class HomeView(TemplateView):
    template_name = "home.html"
"""

# ---------------------------- BASIC APP URL CONF

basic_app_url_conf = """\n
from django.urls import path
from . import views
urlpatterns= []
"""


# ---------------------------- DJANGO CRON JOB
cronjob_dbbackup = """\n
import os
from django.core import management
from django.conf import settings
from django_cron import CronJobBase, Schedule


class Backup(CronJobBase):
    RUN_EVERY_MINS = 10080 # every week
    MIN_NUM_FAILURES = 3
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'APPNAME.Backup'

    def do(self):
        management.call_command('dbbackup')
"""

# -------------------------------- MEDIA FILES

django_media_settings = """\n
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
"""

django_url_conf_imports = """\n
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include\n
"""

django_media_url_path = "\n\n\nurlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\n"

# ------------------------------------ STATIC FILES
django_static_settings = """\n
if DEBUG:
    STATICFILES_DIRS = [BASE_DIR / "static"]
else:
    STATIC_ROOT = BASE_DIR / "static"
"""

# --------------------------------------- DJANGO TAILWIND

django_tailwind_settings = """\n
\n#DJANGO TAILWIND
TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = ['127.0.0.1',]
if platform.system() == 'Windows':
    NPM_BIN_PATH = r'C:\\Program Files\\nodejs\\npm.cmd'
else:
    NPM_BIN_PATH = '/usr/local/bin/npm'
"""

# --------------------------------------- DJANGO CORS HEADERS

django_cors_headers_settings = """\n
#DJANGO CORS HEADERS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:9000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS: True
"""

# --------------------------------------- DJANGO TAILWIND CRISPY

django_tailwind_crispy_settings = """\n
#DJANGO TAILWIND CRISPY
CRISPY_ALLOWED_TEMPLATE_PACKS = 'tailwind'
CRISPY_TEMPLATE_PACK = 'tailwind'
"""


# --------------------------------------- DJANGO DB BACKUP

django_db_backup_settings = """\n
#DJANGO DB BACKUP
DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = 'location': r'LOCATION'
DBBACKUP_HOSTNAME='backup'
"""