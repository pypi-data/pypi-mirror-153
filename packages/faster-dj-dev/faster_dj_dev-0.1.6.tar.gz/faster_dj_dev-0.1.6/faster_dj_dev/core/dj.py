from dataclasses import replace
import os, subprocess, sys, random, time
from termcolor import colored
from colorama import init
from pathlib import Path
#init to enable the color feature in the cmd
init()
# LOCAL IMPORTS
try:
    from ..venvs.Pyenv import Venv
    from ..data.Pydata import DataUtils
    from ..utils.pyUtils import Util
    from ..codebase.html_base_code import *
    from ..codebase.instructions import *
    from ..codebase.python_code_base import *
except ImportError:
    from venvs.Pyenv import Venv
    from data.Pydata import DataUtils
    from utils.pyUtils import Util
    from codebase.html_base_code import *
    from codebase.instructions import *
    from codebase.python_code_base import *


# INITIAL 
venv = Venv()
util = Util()
data = DataUtils()
config = data.get_config_data()

BASE_PATH = Path(__file__).resolve().absolute().parent.parent

class Django:
    def create_new_django_project(self, project_name, app_name=None):
        working_directory = data.get_working_directory_path_from_config_data()
        os.chdir(working_directory)
        venv.install_python_package("django")
        print(f"\nCreating A New Django Project ... {project_name}")
        subprocess.run(f"django-admin startproject {project_name} .", shell=True, stdout=subprocess.PIPE)
        if app_name:
            print(f"\nCreating A New Django App ... {app_name}")
            subprocess.run(f"python manage.py startapp {app_name}", shell=True, stdout=subprocess.PIPE)


    def create_new_django_app(self, app_name):
        installed_apps_list = util.get_list_from_settings_file(name="installed_apps_list", pattern=r"(?=INSTALLED_APPS).+(?=MIDDLEWARE)", index="INSTALLED_APPS = ", return_string=False)
        if app_name not in installed_apps_list:
            working_directory = data.get_working_directory_path_from_config_data()
            os.chdir(working_directory)
            print(f"\nCreating A New Django App ... {app_name}")
            subprocess.run(f"python manage.py startapp {app_name}", shell=True, stdout=subprocess.PIPE)
            util.update_installed_apps_list(value=app_name)
        else:
            sys.exit(colored(f"❌ - {app_name} ", "red") +"already exists! Use another app name.")


    def config_django_templates(self):
        working_directory = data.get_working_directory_path_from_config_data()
        os.chdir(working_directory)
        #Creating template and static folders
        if not os.path.isdir("templates"):
            os.mkdir("templates")
            print("[+]\tCreating templates folder ... \n")
        util.update_template_dirs()
        print("[+]\tConfiguring templates ... \n")


    def config_django_static(self):
        working_directory = data.get_working_directory_path_from_config_data()
        os.chdir(working_directory)
        #Creating template and static folders
        if not os.path.isdir("static"):
            os.mkdir("static")
            print("[+]\tCreating static folder ... \n")
        project_name = data.get_project_path_from_config_data()
        project_path = os.path.join(working_directory, project_name)
        settings_file_path = os.path.join(project_path, "settings.py")
        urls_file_path = os.path.join(project_path, "urls.py")
        util.add_to_the_top_of_the_file(urls_file_path, django_url_conf_imports)
        settings = util.get_file_content(settings_file_path)
        if not "STATIC_ROOT" in settings:
            util.add_to_the_bottom_of_the_file(settings_file_path, django_static_settings)
        print("[+]\tConfiguring static files ... \n")
        

    def config_django_media(self):
        working_directory = data.get_working_directory_path_from_config_data()
        os.chdir(working_directory)
        working_directory = data.get_working_directory_path_from_config_data()
        project_name = data.get_project_path_from_config_data()
        project_path = os.path.join(working_directory, project_name)
        settings_file_path = os.path.join(project_path, "settings.py")
        settings = util.get_file_content(settings_file_path)
        urls_file_path = os.path.join(project_path, "urls.py")
        util.add_to_the_top_of_the_file(urls_file_path, django_url_conf_imports)
        util.reformat_python_file(urls_file_path)
        if "media" and not os.path.isdir("media"):
            os.mkdir("media")
            venv.install_python_package("Pillow")
            util.add_to_the_bottom_of_the_file(urls_file_path,django_media_url_path)
            print("[+]\tCreating media folder ... \n")
        if "MEDIA_ROOT" not in settings:
            util.add_to_the_bottom_of_the_file(settings_file_path, django_media_settings)
        print("[+]\tConfiguring media files ... \n")

        
    def initial_migrate(self):        
        working_directory = data.get_working_directory_path_from_config_data()
        os.chdir(working_directory)
        print(f"\n\n[+]\tMigrating the project ... \n")
        subprocess.run(f'python "manage.py" migrate', shell=True)


    def run_server(self):
        working_directory = data.get_working_directory_path_from_config_data()
        os.chdir(working_directory)
        print(f"\n\n[+]\tRun the server ... \n")
        os.system('pip freeze > "requirements.txt"')
        subprocess.run(f'python "manage.py" runserver', shell=True)

    def update_app_urlconf(self, appname, value):
        working_directory = data.get_working_directory_path_from_config_data()
        urls_file_path = os.path.join(working_directory, appname, "urls.py")
        util.update_urlpatterns_list(value=f"path('', include('{appname}.urls'))")
        if not os.path.isfile(urls_file_path):
            with open(urls_file_path, "w") as new_file:
                new_file.write(basic_app_url_conf)
                time.sleep(1)
        else:
            util.add_to_the_top_of_the_file("from . import views")
        util.reformat_python_file(urls_file_path)
        util.update_urlpatterns_list(value=value, app_name=appname)
        util.reformat_python_file(urls_file_path)

    def create_basic_render_view(self, app_name, base_boilerplate="" ,home_boilerplate=""):
        working_directory = data.get_working_directory_path_from_config_data()
        base_template_name = os.path.join(working_directory, "templates", "base.html")
        home_template_name = os.path.join(working_directory, "templates", "home.html")
        app_view_name = os.path.join(working_directory, app_name, "views.py")

        with open(base_template_name, "w") as base_temp:
            base_temp.write(base_boilerplate)
        with open(home_template_name, "w") as home_temp:
            home_temp.write(home_boilerplate)
        with open(app_view_name, "w") as view_temp:
            view_temp.write(basic_template_view)

        self.update_app_urlconf(app_name, "path('', views.HomeView.as_view(), name='home')")
    
    def install_and_config_package(self, package_list, *args, **kwargs):
        working_directory = data.get_working_directory_path_from_config_data()
        os.chdir(working_directory)
        project_name = data.get_project_path_from_config_data()
        project_path = os.path.join(working_directory, project_name)
        urls_file_path = os.path.join(project_path, "urls.py")
        settings_file_path = os.path.join(project_path, "settings.py")
        settings = util.get_file_content(settings_file_path)
        util.add_to_the_top_of_the_file(urls_file_path, django_url_conf_imports)

        if "djangorestframework" in package_list:
            venv.install_python_package("djangorestframework")
            util.update_installed_apps_list(value="rest_framework")
            util.update_urlpatterns_list(value="path('api-auth/', include('rest_framework.urls'))")

        if "django-cors-headers" in package_list:
            venv.install_python_package("django-cors-headers")
            util.update_installed_apps_list(value="corsheaders")
            util.update_middleware_list(value="corsheaders.middleware.CorsMiddleware", append_after="django.middleware.common.CommonMiddleware")
            util.add_to_the_bottom_of_the_file(settings_file_path, django_cors_headers_settings)


        if "django-unicorn" in package_list:
            venv.install_python_package("django-unicorn")
            util.update_installed_apps_list(value="django_unicorn")
            util.update_urlpatterns_list(value="path(\"unicorn/\", include(\"django_unicorn.urls\"))")
            util.save_usage_instructions("django_unicorn.txt", django_unicorn_help_text)


        if "tailwind" in package_list:
            if not util.check_node_installed_version():
                print(colored("X", "red") + " Node.js is not installed. Please install node.js first.")
            venv.install_python_package("django-tailwind") 
            util.update_installed_apps_list(value='tailwind')
            subprocess.run("python manage.py tailwind init", shell=True)
            util.update_installed_apps_list(value='theme')
            if "import platform" not in settings:
                util.add_to_the_top_of_the_file(settings_file_path ,"import platform")
            util.add_to_the_bottom_of_the_file(settings_file_path, django_tailwind_settings)
            subprocess.run(f"python manage.py tailwind install", shell=True)
            util.update_installed_apps_list(value='django_browser_reload')
            util.update_middleware_list(value="django_browser_reload.middleware.BrowserReloadMiddleware")
            util.update_urlpatterns_list(value="path('__reload__/', include('django_browser_reload.urls'))")
            util.save_usage_instructions("tailwind.txt", django_tailwind_help_text)


        if "django-htmx" in package_list:
            venv.install_python_package("django-htmx")
            util.update_installed_apps_list("django_htmx")
            #util.add_to_the_bottom_of_the_file(settings_file_path, "\n\n#DJANGO HTMX\nCRISPY_ALLOWED_TEMPLATE_PACKS = 'tailwind'\nCRISPY_TEMPLATE_PACK = 'tailwind'")
            util.save_usage_instructions("django_htmx.txt", django_htmx_help_text)


        if "crispy-tailwind" in package_list:
            venv.install_python_package("crispy-tailwind")
            util.update_installed_apps_list("crispy_forms"),
            util.update_installed_apps_list("crispy_tailwind"),
            util.add_to_the_bottom_of_the_file(settings_file_path, django_tailwind_crispy_settings)
            util.save_usage_instructions("crispy_tailwind.txt", django_tailwind_crispy_help_text)

        if "django-dbbackup" in package_list:
            venv.install_python_package("https://github.com/mjs7231/django-dbbackup.git#egg=django-dbbackup", git=True)
            venv.install_python_package("django4-cron")
            util.update_installed_apps_list("dbbackup")
            util.update_installed_apps_list("django_cron")
            os.system(f"python {os.path.join(working_directory, 'manage.py')} migrate django_cron")
            util.add_to_the_bottom_of_the_file(settings_file_path, django_db_backup_settings.replace("LOCATION", {kwargs.get('backup_absolute_path')}))
            random_app = random.choice(config.get("app_names"))
            cron_file_path = os.path.join(working_directory, random_app, "cron.py")
            cron_content = util.get_file_content(os.path.join(BASE_PATH / "templates", "dbbackup.py"))
            if not os.path.isfile(cron_file_path):
                with open(cron_file_path, "w") as cron_f:
                    cron_f.write(cron_content.replace("10080", kwargs.get("backup_every_mins")).replace("APPNAME", random_app))
            cron_class = f"CRON_CLASSES = ['{random_app}.cron.Backup',]"
            util.add_to_the_bottom_of_the_file(settings_file_path, f"\n\n#DJANGO CRON\n{cron_class}")
            util.reformat_python_file(settings_file_path)
            os.system(f"python {os.path.join(working_directory, 'manage.py')} runcrons")

        if "ckeditor" in package_list:
            venv.install_python_package("django-ckeditor")
            util.update_installed_apps_list("ckeditor")
            debug_found = False
            if "DEBUG = True" in settings:
                settings = settings.replace("DEBUG = True", "DEBUG = False")
                util.update_file_content(settings_file_path, settings)
                subprocess.run("python manage.py collectstatic", shell=True)
                settings = settings.replace("DEBUG = False", "DEBUG = True")
                debug_found = True
            util.update_file_content(settings_file_path, settings)
            util.update_installed_apps_list("ckeditor_uploader")
            util.add_to_the_bottom_of_the_file(filename=settings_file_path, string_to_add=ckeditor_settings)
            util.update_urlpatterns_list(value="path('ckeditor/', include('ckeditor_uploader.urls'))")
            util.save_usage_instructions("ckeditor.txt", ckeditor_help_text)
            if not debug_found:
                print(colored("[REQUIRED]\n", "red")+"\n\nPlease udpate DEBUG to False and run:\npython manage.py collectstatic\n\n")


        if "taggit" in package_list:
            venv.install_python_package("django-taggit")
            util.update_installed_apps_list(value="taggit")
            subprocess.run("python manage.py migrate", shell=True)
            util.save_usage_instructions("taggit.txt", django_taggit_help_text)

        if "hitcount" in package_list:
            venv.install_python_package("django-hitcount")
            util.update_installed_apps_list(value="hitcount")
            subprocess.call(f"{django_hitcount_help_text} > hitcount.md", shell=True)
