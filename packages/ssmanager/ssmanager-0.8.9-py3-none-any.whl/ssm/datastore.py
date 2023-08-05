from appdirs import *
from decouple import AutoConfig, config
import os
import shutil
from os.path import exists

#DATASTORE setup file for .env and hosts.csv files.

def create_config_files(path: str):
    cwd = os.getcwd()#curr working dir

    if '\\' in path:
        path += '\\'
        platform = 'putty-windows'
        #mv putty.exe to correct location.
        #TODO change this to copy, to avoid error
        #shutil.move(cwd+'/putty.exe', path)
    else:
        path += '/'
        platform = 'putty-linux'

    if not exists(path+'.env') or not exists(path+'hosts.csv'):
        # Create hosts.csv, w+ create if not exists
        with open(path+'hosts.csv', 'a+') as hostf, open(path+'.env', 'a+') as envf:
            text = """location,ip,username,password,ssh_key
Home,127.0.0.1

Office,10.10.1.1
Office,10.10.1.2
Office,10.10.1.3
Office,10.10.1.3

Examples,10.10.1.4,ALT_USER,ALT_PASSWORD
Examples,10.10.1.5,ALT_USER,ALTKEYFILE,True

Examples,10.80.10.1,My_work_user,work_password
Examples,10.80.10.2,ANOTHER_work_user,ANOTHER_work_password

CloudVMs,174.80.1.1:2222,CLOUD_USER,CLOUD_KEY,True"""
            hostf.write(text)

            env_text = f"""MONITOR_SERVER_EXISTS=False 

[credentials]
# PLATFORM=[insert your platform here, determines SSH launch program: putty-windows, putty-linux, gnome-terminal, xterm-terminal]
# Example:
PLATFORM={platform}

HOST_PATH={path}hosts.csv

# Default username and password for all ssh sessions
SSH_USER=your_username
SSH_PASS=your_password

# Example of defining another user/pass, ALT_USER/ALT_PASSWORD can now be passed in the username,password field in hosts.csv for the required host.
ALT_USER=alt_username
ALT_PASSWORD=alternative_password1234
ALTKEYFILE=path/to/keyfile.pem"""

            envf.write(env_text)







def check_datastore(path: str):
    global show_startup
    #Check if the app folder exists in user data dir, if not then create it.

    app_folder_exists: bool = os.path.isdir(path)
    try:
        if not app_folder_exists:
            os.makedirs(path)
            show_startup = True

    except Exception as e:
        print(e)
        print("Unable to create app folder at: ", path)







appname = "ssm"
appauthor = "Lonestar137"
datastore = user_data_dir(appname, appauthor)

show_startup = False
logo: str = f"""
██████╗███████╗███╗   ███╗
██╔════╝██╔════╝████╗ ████║
███████╗███████╗██╔████╔██║
╚════██║╚════██║██║╚██╔╝██║
███████║███████║██║ ╚═╝ ██║
╚══════╝╚══════╝╚═╝     ╚═╝
                          
Welcome to SSM(Simple SSH Manager)

Config files stored at: {datastore}
If you forget you can always see this dir by using the ? key.

Press any key to continue. . . 
"""




#CHECKS, creates config, dirs,files if necessary
check_datastore(datastore)
create_config_files(datastore)


#Change default config lookup path to the OS indepent config path. .env should be stored here.
config = AutoConfig(search_path=datastore)





