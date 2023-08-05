from email.policy import default
from pathlib import Path
import time, os, sys
from termcolor import colored
from colorama import init
import click

init()

# LOCAL IMPORTS
try:
    from .core.dj import Django
    from .venvs.Pyenv import Venv
    from .data.Pydata import DataUtils
    from .utils.pyUtils import Util
    from .starter.starter import Generator
except ImportError:
    from core.dj import Django
    from venvs.Pyenv import Venv
    from data.Pydata import DataUtils
    from utils.pyUtils import Util
    from starter.starter import Generator

# INITIAL
django = Django()
Pyvenv = Venv()
util = Util()
data = DataUtils()
generator = Generator()
config = data.get_config_data()


@click.command()
@click.option("--init", "-init", is_flag=True, help="Initialize your setup.")
@click.option("--clean", "-clean", is_flag=True, help="Clean the data configuration JSON file.")
@click.option("--working-directory", "-wd", type=str, help="Provide the absolute path of your working directory [that 'will' contain(s) the 'manage.py' file].")
@click.option("--project-folder", "-pf", type=str, help="Provide or choose the name of your Django project [that 'will' hold(s) the settings.py file].")
@click.option("--create-project",  "-cp",  is_flag=True,  help="Install a new Django project.")
@click.option("--starter",  "-s", type=click.Choice(["bare", "basic", "app", "html", "tailwind"]),  help="Create a Django project starter (boilerplate).")
@click.option("--config-templates", "-ct", is_flag=True, help="Create templates folder and update settings.")
@click.option("--config-static",  "-cs",  is_flag=True,  help="Create static folder and update settings.")
@click.option("--config-media",  "-cm",  is_flag=True,  help="Create media folder and update settings.")
@click.option("--initial-migrate",  "-im",  is_flag=True,  help="Run the migration after creating a new Django project.")
@click.option("--run-server",  "-rs",  is_flag=True,  help="Run the local server.")
@click.option("--install","-i",multiple=True,type=click.Choice([
    "djangorestframework", "django-cors-headers", "crispy-tailwind","django-unicorn", "tailwind", "django-htmx", "django-dbbackup", "django-cron",
    "ckeditor", "taggit", "hitcount"
    ],  case_sensitive=False),help="Install Django package.")
@click.option("--backup-absolute-path", "-bap", type=str, help="specify the absolute path of the backup folder.")
@click.option("--backup-every-mins", "-bem", type=str, help="Backup database every X minutes.", default="10080", show_default=True)
@click.option("--app", "-a", type=str, help="specify the application name.")
def main(create_project, app, config_templates, config_static, config_media,
         initial_migrate, run_server, install, backup_absolute_path, backup_every_mins,
         init, working_directory, project_folder, starter, clean
        ):

    # Print system info
    os_version, pip_version, python_version = util.get_system_data()
    print("Operating system: " + colored(os_version, "blue"))
    print("Python version: " + colored(python_version, "blue"))
    print("Pip version: " + colored(pip_version, "blue"))

    if not Pyvenv.is_venv_activated():
        print("\nYour virtual environment is not activated.\n" +
              colored("Options:", "blue") + "\n")
        print("1-\tActivate it.\n2-\tUse the --venv flag.")
    else:

        if clean:
            data.clean_config_data()


        if init:
            if working_directory and project_folder:
                if util.check_folder_path_validity(working_directory):
                    data.update_data_config(key="working_directory", value=working_directory)
                    data.update_data_config(key="project_folder", value=project_folder)
                    print(colored("\n[+] ", "green")+"project initialized.\n")
                else:
                    print(colored("X ", "red", attrs=["bold"])+ f"{working_directory} doesn't exist!")
            else:
                print(colored("X ", "red", attrs=["bold"])+ "Use the "+colored("--working-directory", attrs=["bold", "underline"])+" and "+colored("--project-folder", attrs=["bold", "underline"])+ " with the init option!")


        if starter:
            if "bare" in starter:
                generator.generate_bare_django_project()
            elif "basic" in starter:
                generator.generate_basic_django_project()
            elif "app" in starter:
                generator.generate_basic_django_project_with_app()
            elif "html" in starter:
                generator.generate_basic_django_with_html_template()
            elif "tailwind" in starter:
                generator.generate_basic_django_with_tailwind_template()

        if create_project:
            project = data.get_project_path_from_config_data()
            django.create_new_django_project(project)

        if app:
            django.create_new_django_app(app)
            if app not in config["app_names"]:
                config["app_names"].append(app)
                data.update_data_config(config_dict=config)

        if config_templates:
            django.config_django_templates()

        if config_static:
            django.config_django_static()

        if config_media:
            django.config_django_media()

        if initial_migrate:
            django.initial_migrate()

        if run_server:
            django.run_server()

        if install:
            if "django-dbbackup" in install and not backup_absolute_path:
                sys.exit(colored("[-] ", "red")+"Please enter the absolute path where you want to save the backup files.")            
            else:
                django.install_and_config_package(install, backup_absolute_path=backup_absolute_path, backup_every_mins=backup_every_mins)


if __name__ == "__main__":
    main()
