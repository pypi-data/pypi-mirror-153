import os, subprocess, logging, platform, pathlib, time
from termcolor import colored
from colorama import init
#init to enable the color feature in the cmd
init()

logging.basicConfig(filename='faster-django.log', filemode='a', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

# LOCAL IMPORTS

#INITIAL
os_version = platform.system()
BASE_PATH = pathlib.Path(__file__).resolve().absolute().parent

class Venv:
    """Handle everything related to Python virtual environment and installing packages"""

    def is_venv_activated(self):
        try:
            os.environ["VIRTUAL_ENV"]
        except KeyError:
            return False
        else:
            return True
    
    def  is_package_installed(self, package):
        packages = " ".join(pack.lower() for pack in os.popen("python -m pip freeze"))
        if package in packages:
            return True
        return False

    def install_python_package(self, package, git=False):
        print(f"\nInstalling {package} ... ")
        try:
            if git:
                subprocess.run(f"pip install -e git+{package}", shell=True, stdout=subprocess.PIPE)
            else:
                subprocess.run(f"python -m pip install {package}", shell=True, stdout=subprocess.PIPE)
            print(colored("✅ - ", "green") + f"{package} installed.")
            return True
        except Exception as error:
            print(colored("❌ - ", "red") + f"Failed to install {package}!")
            logging.critical(f"Failed to install {package}! --> {error}")
            return False

    def install_virtual_environment_and_activate_it(self, working_directory, inside=False):
        if not os.path.isdir(working_directory):
            os.mkdir(working_directory)
        if not self.is_package_installed("virtualenv"):
            self.install_python_package("virtualenv")
        env_path = os.path.join(working_directory, 'venv') if inside else os.path.join(pathlib.Path(working_directory).parent, 'venv')
        if os_version == "Windows":
            env_path = os.path.join(working_directory, 'venv') if inside else os.path.join(pathlib.Path(working_directory).parent, 'venv')
            print("\nCreating A New virtualenv ... ")
            os.system(f"python -m virtualenv {env_path} >nul 2>&1")
            print("\nActivating The virtualenv ... ")
            subprocess.call(f"cmd.exe /k {env_path}\\Scripts\\activate.bat")
        else:
            print("\nCreating A New virtualenv ... \n\n")
            subprocess.run(f"virtualenv {env_path}", shell=True, stdout=subprocess.PIPE)
            print("\nActivating The virtualenv ... ")
            os.system(f'/bin/bash  --rcfile {env_path}/bin/activate')

        print(colored(f"Next, run this command:\npython -m pip install -r {BASE_PATH / 'requirements.txt'}"))