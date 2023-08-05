from email import message
import json, os, pathlib
from pathlib import Path
from termcolor import colored
from colorama import init
init()


# INITIAL
DATA_PATH = Path(__file__).resolve().absolute().parent
config = json.load(open(DATA_PATH / "config.json", "r"))


class DataUtils:
    """ Take care of project related data from importing to saving the projects paths """

    # if key and value are givven, it updates the key-value pair in the config file
    # else if config (dict) is provided, it updated the entire file
    def update_data_config(self, key="", value="", config_dict=None):
        if not config_dict:
            config[key] = value
        with open(DATA_PATH / "config.json", "w") as config_file:
            config_file.write(json.dumps(config))

    def get_working_directory_path_from_config_data(self):
        path = config.get("working_directory")
        parent = pathlib.Path(path).parent
        if os.path.isdir(parent) and path:
            if not os.path.isdir(path):
                os.mkdir(path)
        else:
            print(colored(f"\nUnable to locate the working directory!", "yellow"))
            while True:
                new_path = input("Please enter the absolute path of your working directory!"+colored(" [that contains manage.py file] ", "blue", attrs=["bold",])+" :\n-->\t")
                if new_path != "":
                    self.update_data_config(key="working_directory", value=new_path)
                    path = new_path
                    break
            
        return path

    def get_project_path_from_config_data(self):
        path = config.get("project_folder")
        if not path:
            print(colored(f"\nUnable to find the project name!", "yellow"))
            while True:
                new_path = input("Please enter the name of your project "+colored("[that contains settings.py file]", "blue", attrs=["bold",])+" :\n-->\t")
                if new_path != "":
                    self.update_data_config(key="project_folder", value=new_path)
                    path = new_path
                    break
            
        return path

    def get_apps_list_from_config_data(self):
        apps = config.get("app_names")
        return apps

    def get_config_data(self):
        return config

    def clean_config_data(self):
        empty_config = {
            "project_folder": "",
            "app_names": [],
            "working_directory": "",
        }
        with open(DATA_PATH / "config.json", "w") as config_file:
            config_file.write(json.dumps(empty_config))
        print(colored("[+] ", "green")+" cleaned.")
