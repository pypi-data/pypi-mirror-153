import curses
from curses import wrapper, window
from curses.textpad import Textbox, rectangle

#Regex
import re

#Necessary for PuTTy
import os, subprocess, platform

#Necessary for environmental password configuration.
from decouple import config

#For reading and updating csv during runtime
import csv
from collections import defaultdict

#for cmd line args 
import sys
import getpass

#from UI.datastore import *
from ssm.datastore import *

#TODO set platform
#TODO open .env
#TODO def set default user/pass


#TODO write a file class that is agnostic to platform with read write operations.
class Config_File:
    def __init__(self, path: str):
        self._path: str = path
        self._file: str = self.read()

    def read(self)->str:
        #Read file to string.
        with open(self._path, 'r') as f:
            self._file = f.read()
        return self._file

    def append(self, line: str):
        #append line to file.
        with open(self._path, 'a') as f:
            f.write(line)

    def write(self, s: str):
        # Write a string
        with open(self._path, 'w') as f:
            f.write(s)

        self.read()

    #TODO def find and replace line

    def deleteLineWhere(self, s: str):
        #TODO add kwargs support so more than one expression can be applied.  Find where this and this are both in line.

        #Delete a line where string found
        lines: list = self._file.splitlines()
        for index, line in enumerate(lines):
            if(line.find(s) != -1):
                lines.pop(index)
                break

        # Recombine to write the new file.
        f: str = ''
        for line in lines:
            f += line+'\n'

        self.write(f)

def prune_env(envuser: str, envpass: str):
    # Remove all the non used env variables from .env
    # # Remove all the non used env variables from .env
    create_env_variable('NULL', envuser, envpass)

def delete_host(ip):
    #Delete a specific host from the hosts.csv, note delets the first match by IP.
    hosts_csv.deleteLineWhere(ip)


def create_env_variable(possible_env_var_name: str, username: str, password: str):
    #Checks .env to see if the password already exists, if not create new one, elif exists use original.

    if(password == ''):
        return '', ''

    if(platform.system() == "Windows"):
        with open(datastore+'\\.env', 'r') as f:
            file = f.read().split('\n')
    else:
        with open(datastore+'/.env', 'r') as f:
            file = f.read().split('\n')

    values_keys = dict()
    for line in file:
        if(line.find('=') != -1):
            pv = line.strip().split('=')
            values_keys.update({pv[1]: pv[0]})

    if(username in values_keys and password in values_keys):
        #password exists, return the existing envvar name
        return values_keys[username], values_keys[password]
    else:
        #if not exists, add to .env and return new variables.
        name = possible_env_var_name
        index = str(len(values_keys))
        envuser, envpassw = name+'User'+index, name+'Pass'+index

        #Write the changes.
        if(platform.system() == "Windows"):
            with open(datastore+'\\.env', 'a') as f:
                newVariables = f'\n{envuser}={username}\n{envpassw}={password}'
                file = f.write(newVariables)
        else:
            with open(datastore+'/.env', 'a') as f:
                newVariables = f'\n{envuser}={username}\n{envpassw}={password}'
                file = f.write(newVariables)

        return envuser, envpassw
    


def new_host_screen(stdscr):

    #               (y, x, field, answer)
    #TODO Create a list class for creating a menu screen like this and replace list tuple items with objects.
    options: list = [(3, 3, "location: ", ""), (4, 3, "ip: ", ""), (5, 3, "username: ", ""), (6, 3, "password: ", ""), (7, 3, "ssh_key(T/F): ", ""), (8, 3, "Open hosts.csv", " [ → ]"), (9, 3, "Open .env", " [ → ]")]
    #options: list = [(3, 3, "location: ", ""), (4, 3, "ip: ", ""), (5, 3, "username: ", ""), (6, 3, "password: ", ""), (7, 3, "ssh_key(T/F): ", "")]
    curr_option = 0
    while True:
        max_y, max_x=window.getmaxyx(stdscr)
        rectangle(stdscr, 2,2,len(options)+3,40)
        stdscr.addstr(2,3,"Add a host:", curses.A_UNDERLINE | curses.A_BOLD | curses.color_pair(1))
        stdscr.refresh()
        stdscr.addstr(len(options)+3,3,"(←) Back, (Enter) Save ", curses.color_pair(2))

        if(options[4][3] == 'True'):
            # Changes password field to key_path if ssh_key=True.
            options[3] = (options[3][0],
                    options[3][1],
                    'key_path: ',
                    options[3][3])
        else:
            options[3] = (options[3][0],
                    options[3][1],
                    'password: ',
                    options[3][3])


        for option in options:
            #Hide password as it's printed, and it's not a ssh key path.
            if(option[2] == 'password: ' and options[4][3] != 'True'):
                hiddenpass = option[3].replace(option[3], '*') * len(option[3])
                stdscr.addstr(option[0], option[1], option[2]+hiddenpass)
            else:
                stdscr.addstr(option[0], option[1], option[2]+option[3])

        if(curr_option == 3 and options[4][3] != 'True'):
            # Hide password as it's typed.
            hiddenpass = options[curr_option][3].replace(options[curr_option][3], '*') * len(options[curr_option][3])
            stdscr.addstr(options[curr_option][0],
                    options[curr_option][1],
                    options[curr_option][2]+hiddenpass)

        else:
            stdscr.addstr(options[curr_option][0],
                    options[curr_option][1],
                    options[curr_option][2]+options[curr_option][3])

        key = stdscr.getkey()
        stdscr.clear()
        if(key == "KEY_DOWN"):
            if(curr_option == -1 or curr_option == len(options)-1):
                curr_option = 0
            else:
                curr_option += 1

            stdscr.addstr(options[curr_option][0],
                    options[curr_option][1], 
                    options[curr_option][2]+options[curr_option][3],
                    curses.A_STANDOUT)
        elif(key == "KEY_UP"):
            if(curr_option == -1 or curr_option == len(options)):
                curr_option = len(options)-1
            else:
                curr_option -= 1
            stdscr.addstr(options[curr_option][0],
                    options[curr_option][1],
                    options[curr_option][2]+options[curr_option][3],
                    curses.A_STANDOUT)
        elif(key in ["KEY_LEFT"]):
            break
        elif(key in ["KEY_RIGHT"]):
            config_file = ''
            if(curr_option == 5): config_file = 'hosts.csv'
            elif(curr_option == 6): config_file = '.env'
            #Open file in editor.
            try:
                if(platform.system() == "Darwin"): #if mac
                    subprocess.call(('open', datastore+'/'+config_file))
                elif(platform.system() == "Windows"):
                    os.system("start " + datastore+'\\'+config_file)
                else:
                    subprocess.call(('xdg-open', datastore+'/'+config_file))
            except Exception as e:
                stdscr.clear()
                stdscr.addstr(1,1,"An exception occurred: \n"+ str(e))
                stdscr.getch()
                break
            stdscr.clear()

        elif(key == "KEY_BACKSPACE"):
            stdscr.refresh()
            options[curr_option] = (options[curr_option][0], 
                    options[curr_option][1], 
                    options[curr_option][2],
                    options[curr_option][3][:-1])
        elif(key == "\n"):
            envVarUser, envVariablePass = create_env_variable(options[0][3], options[2][3], options[3][3]) #generate envvar from location if it doesn't already exist.
            csv_line = f'{options[0][3]},{options[1][3]},{envVarUser},{envVariablePass},{options[4][3]}'

            stdscr.addstr(len(options)-1, options[curr_option][1], 'Save the following host?(y/n)')
            stdscr.addstr(len(options), options[curr_option][1], csv_line)
            key = stdscr.getkey()
            if(key in ['\n', 'y', 'Y', 'yes', 'Yes']):
                #Append the new host to the hosts.csv
                hosts_csv.append('\n'+csv_line)
                stdscr.addstr(len(options)+1, options[curr_option][1], "Saved!")
                stdscr.getch()
                stdscr.clear()
            else:
                stdscr.clear()
                
        else:
            options[curr_option] = (options[curr_option][0], 
                    options[curr_option][1],
                    options[curr_option][2],
                    options[curr_option][3]+ key)




def test():
    operating_system = platform.system()#Darwin(mac), Windows, Dist(linux)
    datastore = '/home/jonesgc/.local/share/ssm'
    if(operating_system == 'Windows'):
        datastore += '\\'
    else:
        datastore += '/'

    hosts_csv = Config_File(datastore+'hosts.csv')
    dot_env = Config_File(datastore+'.env')
    hosts_csv.deleteLineWhere('1111111')
    print(hosts_csv.read())


# Define the file objects globally.
operating_system = platform.system()#Darwin(mac), Windows, Dist(linux)
if(operating_system == 'Windows'):
    datastore += '\\'
else:
    datastore += '/'

# Get file objects.
hosts_csv = Config_File(datastore+'hosts.csv')
dot_env = Config_File(datastore+'.env')


if __name__ == "__main__":   
    #NOTE this file is currently not used but planned for future implementations.
    #wrapper(new_host_screen())
    test()
    pass
