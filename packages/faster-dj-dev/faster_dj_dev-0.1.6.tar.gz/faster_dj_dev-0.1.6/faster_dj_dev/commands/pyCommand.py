import subprocess

class Command:
    def get_command_output(self, command):
        try: 
            return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read().decode()
        except:
            return None