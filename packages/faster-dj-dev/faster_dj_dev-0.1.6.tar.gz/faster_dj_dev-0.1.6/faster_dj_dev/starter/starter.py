from pathlib import Path
import subprocess, os
# LOCAL IMPORTS
try:
    from ..core.dj import Django
    from ..data.Pydata import DataUtils
    from ..codebase.html_base_code import *
    from ..codebase.python_code_base import *
    from ..venvs.Pyenv import Venv
    from ..utils.pyUtils import Util
except ImportError:
    from core.dj import Django
    from data.Pydata import DataUtils
    from codebase.html_base_code import *
    from codebase.python_code_base import *
    from venvs.Pyenv import Venv
    from utils.pyUtils import Util

# INITIAL 
django = Django()
data = DataUtils()
util = Util()
venv = Venv()
BASE_PATH = Path(__file__).resolve().absolute().parent.parent

class Generator:
    """
    Generate Dajngo projects boilerplate (starter)  
    """
    
    # Bare Django project (without any app or configurations)
    def generate_bare_django_project(self):
        project = data.get_project_path_from_config_data()
        django.create_new_django_project(project)
        django.initial_migrate()
        django.run_server()

    # Basic Django project with its configurations (media, static, templates)
    def generate_basic_django_project(self):
        project = data.get_project_path_from_config_data()
        django.create_new_django_project(project)  
        django.config_django_templates()
        django.config_django_static()
        django.config_django_media()
        django.initial_migrate()
        django.run_server()

    # Basic Django project plus installing a Django app (plus configurations)
    def generate_basic_django_project_with_app(self, app_name="main"):
        project = data.get_project_path_from_config_data()
        django.create_new_django_project(project) 
        django.create_new_django_app(app_name) 
        django.config_django_templates()
        django.config_django_static()
        django.config_django_media()
        django.initial_migrate()
        django.run_server()

    # Django project with initial HTML page
    def generate_basic_django_with_html_template(self, app_name="main"):
        project = data.get_project_path_from_config_data()
        django.create_new_django_project(project) 
        django.create_new_django_app(app_name) 
        django.config_django_templates()
        django.config_django_static()
        django.config_django_media()
        django.create_basic_render_view(app_name, base_boilerplate=pure_base_html_boilerlate, home_boilerplate=pure_home_html_boilerlate)
        django.initial_migrate()
        django.run_server()

    # Django project with initial HTML page
    def generate_basic_django_with_tailwind_template(self, app_name="main"):

        project = data.get_project_path_from_config_data()
        django.create_new_django_project(project) 
        django.create_new_django_app(app_name) 
        django.config_django_templates()
        django.config_django_static()
        django.config_django_media()

        
        working_directory = data.get_working_directory_path_from_config_data()
        os.chdir(working_directory)
        project_name = data.get_project_path_from_config_data()
        project_path = os.path.join(working_directory, project_name)
        settings_file_path = os.path.join(project_path, "settings.py")
        settings = util.get_file_content(settings_file_path)
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
        
        django.create_basic_render_view(app_name, base_boilerplate=django_tailwind_base_html_boilerplate, home_boilerplate=django_tailwind_home_html_boilerplate)
        django.initial_migrate()
        subprocess.run(f"python manage.py tailwind build", shell=True)
        django.run_server()
