import platform, re, sys, os, json, logging, pathlib, subprocess
from termcolor import colored
from colorama import init
init()
import ast
logging.basicConfig(filename='faster-django.log', filemode='a', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


# LOCAL IMPORTS
try:
    from ..commands.pyCommand import Command
    from ..data.Pydata import DataUtils
except ImportError:
    from commands.pyCommand import Command
    from data.Pydata import DataUtils

# INITIAL
command = Command()
data = DataUtils()

class Util:
    def reformat_python_file(self, path):
        #os.system(f"python -m black {path}")
        reformat_command_output = command.get_command_output(f"yapf -i {path}")
        
    # Check if the given path of a folder or its parent exist or not
    # If the parent doesn't exist, return None
    def check_folder_path_validity(self, path):
        parent = pathlib.Path(path).parent
        if os.path.isdir(parent):
            if not os.path.isdir(path):
                os.mkdir(path)
            return path
        else:
            return None

    def get_system_data(self):
        os_version = platform.system()
        pip_version_text = command.get_command_output("python -m pip --version")
        try:
            pip_version = re.search(r"(\d+\.\d+\.\d+)", pip_version_text.decode()).group()
        except AttributeError:
            pip_version = pip_version_text[3:11].strip()
        except:
            pip_version = "Unknown"
        python_version_text = sys.version
        try:
            python_version = re.search(r"(\d+\.\d+\.\d+)", python_version_text).group()
        except AttributeError:
            python_version = python_version_text[3:11].strip()
        except:
            python_version = "Unknown"

        return os_version, pip_version, python_version


    def get_file_content(self, file):
        with open(file, "r") as f:
            content = f.read()
        return content


    def update_file_content(self, file, content):
        with open(file, "w") as f:
            f.write(content)


    def add_to_the_bottom_of_the_file(self, filename, string_to_add):
        content = self.get_file_content(filename)
        if not string_to_add in content:
            with open(filename, "a") as file:
                file.write("\n"+string_to_add)


    def add_to_the_top_of_the_file(self, filename, string_to_add):
        content = self.get_file_content(filename)
        if not string_to_add in content:
            with open(filename, "w") as file:
                file.write(string_to_add+"\n"+content)


    # get_list_from_settings_file(name="installed_apps_list", pattern=r"(?=INSTALLED_APPS).+(?=MIDDLEWARE)", index="INSTALLED_APPS = ", return_string=False)
    # get_list_from_settings_file(name="middleware_list", pattern=r"(?=MIDDLEWARE).+(?=MIDDLEWARE)", index="MIDDLEWARE = ", return_string=False)
    def get_list_from_settings_file(self, name="", pattern=r"", index="", return_string=False):
        working_directory = data.get_working_directory_path_from_config_data()
        project_name = data.get_project_path_from_config_data()
        project_path = os.path.join(working_directory, project_name)
        settings_file_path = os.path.join(project_path, "settings.py")
        self.reformat_python_file(settings_file_path)
        settings = self.get_file_content(settings_file_path)
        match = re.search(pattern, settings, re.DOTALL)
        if match:
            try:
                if not return_string:
                    settings_list = match.group().replace(index,"")
                    settings_list  = settings_list[settings_list.find("["):settings_list.find("]")+1].replace("\n","").replace(" ","")
                    return ast.literal_eval(settings_list)
                else:
                    settings_list = match.group()
                    settings_list  = settings_list[settings_list.find(index):settings_list.find("]")+1]
                    return settings_list
            except Exception as error:
                logging.critical(f"GET {name} LIST: {error}")
        sys.exit(colored("[!] FATAL ","red", attrs=["bold",])+ f"Couldn't find the {name}!")
        


  
    
    def get_url_patterns_list_string_format(self, app_name=""):
        working_directory = data.get_working_directory_path_from_config_data()
        project_name = data.get_project_path_from_config_data()
        project_path = os.path.join(working_directory, project_name)

        if not app_name:
            urls_file_path = os.path.join(project_path, "urls.py")
            self.reformat_python_file(urls_file_path)
            urls_file = self.get_file_content(urls_file_path)
        else:    
            urls_file_path = os.path.join(working_directory,app_name, "urls.py")
            if not os.path.isfile(urls_file_path):
                logging.critical(f"The app '{app_name}' doesn't have a urls file.")
                sys.exit(colored("[!] FATAL ","red", attrs=["bold",])+f"The app '{app_name}' doesn't have a urls file.")
            self.reformat_python_file(urls_file_path)
            urls_file = self.get_file_content(urls_file_path)
        
        pattern = r'(?=urlpatterns =).+(\])'
        match = re.search(pattern, urls_file, re.DOTALL)
        if match:
            try:
                urls_list = match.group().replace("urlpatterns = ","").replace("urlpatterns= ","").replace("urlpatterns =","").replace("urlpatterns=","")
                urls_list  = urls_list[urls_list.find("["):urls_list.find("]")+1].replace("\n","").replace(" ","")
                return urls_list
            except Exception as error:
                logging.critical(f"GET URLPATTERNS LIST: {error}")
        sys.exit(colored("[!] FATAL ","red", attrs=["bold",])+"Couldn't find URLPATTERNS list!")

    
    def update_installed_apps_list(self, value="", append_after=""):
        working_directory = data.get_working_directory_path_from_config_data()
        project_name = data.get_project_path_from_config_data()
        project_path = os.path.join(working_directory, project_name)
        settings_file_path = os.path.join(project_path, "settings.py")
        self.reformat_python_file(settings_file_path)
        settings = self.get_file_content(settings_file_path)
        installed_apps_list = self.get_list_from_settings_file(name="installed_apps_list", pattern=r"(?=INSTALLED_APPS).+(?=MIDDLEWARE)", index="INSTALLED_APPS = ", return_string=False)
        old_installed_apps_list = self.get_list_from_settings_file(name="installed_apps_list", pattern=r"(?=INSTALLED_APPS).+(?=MIDDLEWARE)", index="INSTALLED_APPS = ", return_string=True)
        if value not in installed_apps_list:
            if append_after:
                try:
                    installed_apps_list.insert((installed_apps_list.index(append_after)+1), value)
                except ValueError:
                    logging.error("{append_after} doesn't belong to the installed apps list.")
                    sys.exit(colored("❌ - ", "red") +f"{append_after} doesn't belong to the installed apps list.")
            else:
                installed_apps_list.append(value)
        
        installed_apps_list_string = "INSTALLED_APPS = "+json.dumps(installed_apps_list)
        old_installed_apps_list_string = json.dumps(old_installed_apps_list)
        
        with open("l.py", "w") as l:
            l.write(old_installed_apps_list)
        old_installed_apps_list_string = self.get_file_content("l.py")
        os.remove("l.py")
        if old_installed_apps_list_string in settings:
            settings = settings.replace(old_installed_apps_list_string, installed_apps_list_string)
            with open(settings_file_path, "w") as settings_file:
                settings_file.write(settings)
        self.reformat_python_file(settings_file_path)


    def update_middleware_list(self, value="", append_after=""):
        working_directory = data.get_working_directory_path_from_config_data()
        project_name = data.get_project_path_from_config_data()
        project_path = os.path.join(working_directory, project_name)
        settings_file_path = os.path.join(project_path, "settings.py")
        self.reformat_python_file(settings_file_path)
        settings = self.get_file_content(settings_file_path)
        middleware_list = self.get_list_from_settings_file(name="middleware_list", pattern=r"(?=MIDDLEWARE).+(?=ROOT_URLCONF)", index="MIDDLEWARE = ", return_string=False)
        old_middleware_list = self.get_list_from_settings_file(name="middleware_list", pattern=r"(?=MIDDLEWARE).+(?=ROOT_URLCONF)", index="MIDDLEWARE = ", return_string=True)
        if value not in middleware_list:
            if append_after:
                middleware_list.insert((middleware_list.index(append_after)+1), value)
            else:
                middleware_list.append(value)
        
        middleware_list_string = "MIDDLEWARE = "+json.dumps(middleware_list)
        old_middleware_list_string = json.dumps(old_middleware_list)
        
        with open("l.py", "w") as l:
            l.write(old_middleware_list)
        old_middleware_list_string = self.get_file_content("l.py")
        os.remove("l.py")
        if old_middleware_list_string in settings:
            settings = settings.replace(old_middleware_list_string, middleware_list_string)
            with open(settings_file_path, "w") as settings_file:
                settings_file.write(settings)
        self.reformat_python_file(settings_file_path)


    def update_urlpatterns_list(self, value="", append_after="", app_name=""):
        working_directory = data.get_working_directory_path_from_config_data()
        project_name = data.get_project_path_from_config_data()
        project_path = os.path.join(working_directory, project_name)

        if app_name == "":
            urls_file_path = os.path.join(project_path, "urls.py")
            self.reformat_python_file(urls_file_path)             
            urls_file = self.get_file_content(urls_file_path)
            urlpatterns_list = self.get_url_patterns_list_string_format()
            old_urlpatterns_list = self.get_url_patterns_list_string_format()
        else:    
            urls_file_path = os.path.join(working_directory, app_name, "urls.py")
            if not os.path.isfile(urls_file_path):
                logging.critical(f"The app '{app_name}' doesn't have a urls file.")
                sys.exit(colored("[!] FATAL ","red", attrs=["bold",])+f"The app '{app_name}' doesn't have a urls file.")

            self.reformat_python_file(urls_file_path)       
            urls_file = self.get_file_content(urls_file_path)
            urlpatterns_list = self.get_url_patterns_list_string_format(app_name=app_name)
            old_urlpatterns_list = self.get_url_patterns_list_string_format(app_name=app_name)

        urlpatterns_list = "urlpatterns = "+urlpatterns_list
        if value not in urlpatterns_list:
            if append_after:
                if append_after+"," in urls_file:
                    urlpatterns_list = urlpatterns_list.replace(append_after,append_after+value+",")
                else:
                    urlpatterns_list = urlpatterns_list.replace(append_after,append_after+","+value+",")
            else:
                urlpatterns_list = urlpatterns_list.replace("urlpatterns = [","urlpatterns = ["+value+",")
        
        
        old_urlpatterns_list_string = "urlpatterns = "+old_urlpatterns_list
        
        with open("l.py", "w") as l:
            l.write(old_urlpatterns_list_string)
        self.reformat_python_file("l.py")
        old_urlpatterns_list_string = self.get_file_content("l.py")
        os.remove("l.py")
        if old_urlpatterns_list_string in urls_file:
            urls_file = urls_file.replace(old_urlpatterns_list_string, urlpatterns_list).replace("urlpatterns +=", "\n\nurlpatterns +=")
            with open(urls_file_path, "w") as urls_f:
                urls_f.write(urls_file)
        self.reformat_python_file(urls_file_path)


    def update_template_dirs(self):
        working_directory = data.get_working_directory_path_from_config_data()
        project_name = data.get_project_path_from_config_data()
        project_path = os.path.join(working_directory, project_name)
        settings_file_path = os.path.join(project_path, "settings.py")
        self.reformat_python_file(settings_file_path)
        settings = self.get_file_content(settings_file_path)
        if "\"DIRS\": []" in settings:
            settings = settings.replace("\"DIRS\": []", "\"DIRS\": [BASE_DIR / \"templates\"]")
        elif "'DIRS': []" in settings:
            settings = settings.replace("'DIRS': []", "'DIRS': [BASE_DIR / 'templates']")
        self.update_file_content(settings_file_path, settings)


    def check_node_installed_version(self):
        node_version = subprocess.check_output(["node", "-v"]).decode("utf-8").strip()
        node_version_regex_pattern = r"v(\d+\.\d+\.\d+)"
        if re.search(node_version_regex_pattern, node_version):
            return True
        else:
            return False

    def save_usage_instructions(self, filename, instructions):
        working_directory = data.get_working_directory_path_from_config_data()
        usage_folder = os.path.join(working_directory, "usage")
        if not os.path.isdir(usage_folder):
            os.mkdir(usage_folder)
        with open(os.path.join(usage_folder, filename), "w") as f:
            f.write(instructions)
            print(colored(f"[+] Usage instructions for {filename} saved in 'usage' folder.", "green"))
