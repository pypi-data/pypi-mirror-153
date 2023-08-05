import curses
from curses import wrapper, window
from curses.textpad import Textbox, rectangle

#Regex
import re

#Necessary for PuTTy
import os
import subprocess

#Necessary for environmental password configuration.
from decouple import config
from ssm.datastore import *
from ssm.interface import delete_host, new_host_screen, hosts_csv, dot_env

#For reading and updating csv during runtime
import csv
from collections import defaultdict

#for cmd line args 
import sys
import getpass

def extra_text(stdscr, y_max, x_max):
    #color definitions, adds support for transparent background.
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1) #IP Selection color
    curses.init_pair(2, curses.COLOR_YELLOW, -1) #Pinging color #5
    curses.init_pair(3, curses.COLOR_RED, -1) #Ping down color  #4
    curses.init_pair(4, curses.COLOR_YELLOW, -1) #IP Selection color # 2
    curses.init_pair(5, curses.COLOR_RED, -1) #Folder color # 3

    #Extra text on the rectangle, i.e., (?) help or (q) quit
    stdscr.addstr(2, 3, 'SSH Sessions', curses.A_UNDERLINE | curses.A_BOLD | curses.color_pair(1))
    stdscr.addstr(2, 30, '(?) Help', curses.color_pair(2))
    stdscr.addstr(y_max-2, 30, '(q) Quit', curses.color_pair(2))

def print_list(stdscr, lst: list, y: int, x:int):
    #y,x = initial start point.

    #How many hosts should be spawned to screen.
    y_limit, x_limit = window.getmaxyx(stdscr)

    for i in lst:
        if y < y_limit-2:
            if i.find('\t') == -1:
                #host found in list
                stdscr.addstr(y,x, str(i)+'\t\t\t', curses.color_pair(5))
            else:
                stdscr.addstr(y,x, str(i)+'\t\t\t', curses.color_pair(4))
            y+=1
        else:
            break

def queue(stdscr, my_list=None):
    #Startup screen for firsttime installers.
    if show_startup:
        stdscr.addstr(0,0, logo)
        stdscr.getch()
        stdscr.clear()

    curses.curs_set(0)
    #global my_list
    if my_list == None:
        my_list, SSH_USER, SSH_PASS, unique_hosts_dict, PLATFORM = initiate_vars()
    else:
        ignore_list, SSH_USER, SSH_PASS, unique_hosts_dict, PLATFORM = initiate_vars()

    list_x=3 #X of list objects
    list_y=3 #Starting y coord of list.

    max_y, max_x=window.getmaxyx(stdscr)

    #Regex to match the full IP address pattern.
    ip_pattern=re.compile("\t([0-9].+)")

    #Clears weirdness on search function.
    #stdscr.clear()

    print_list(stdscr, my_list, list_y, list_x)
    try:
        print_list(stdscr, my_list, list_y, list_x)
    except:
        pass

    pointer = int(len(my_list)/2)
    if pointer > 20:
        pointer = 15# Prevents the cursor from going off the screen.

    #Ensures that the key is made at startup, i.e. if pointer lands on folder it won't error out because key is never created.
    key_made=False

    #Prevents pointer from starting on a folder.
    if str(my_list[pointer]).find('\t') == -1:
        pointer+=1
    

    while True:
        max_y, max_x=window.getmaxyx(stdscr)
        if max_y < 20:
            stdscr.addstr(0, 0, 'Screen too small, please resize.')
            stdscr.getch()
            continue
        

        selected_item = str(my_list[pointer])

        curses.init_pair(156, 155, 154)
        #Place highlighted ontop of the list.  But place selected object in the center always and use color_pair 1 to make green.
        if(len(selected_item) > 18):
            #limits number of chars on selected item to prevent clipping.
            stdscr.addstr(list_y+pointer, list_x, '\t\t'+selected_item[:18], curses.A_STANDOUT | curses.color_pair(1))
        else:
            stdscr.addstr(list_y+pointer, list_x, '\t\t'+selected_item, curses.A_STANDOUT | curses.color_pair(1))

        #Frame, try - to prevent crash if window size becomes too small.
        try:
            rectangle(stdscr, 2,2,max_y-2,40)
            extra_text(stdscr, max_y, max_x)
        except:
            pass

        #If keymade and the current selected item does not match IP pattern then pass else get key press.
        if key_made == True and ip_pattern.fullmatch(selected_item) == None:
            pass#Key should stay equal to your last movement to move you up or down.
        else:
            key = stdscr.getkey()
            key_made = True

        if key in ['k', 'KEY_UP']:
            #Press k key to increment list up.
            last_index = len(my_list)-1
            my_list.insert(0, my_list[last_index])

            last_index = len(my_list)-1
            my_list.pop(last_index)
        elif key in ['K']:
            #Press K key to increment list up by 5.
            for i in range(5):
                last_index = len(my_list)-1
                my_list.insert(0, my_list[last_index])

                last_index = len(my_list)-1
                my_list.pop(last_index)

        elif key in ['j', 'KEY_DOWN']:
            #Press j key to incrment list down.
            last_index = len(my_list)-1
            my_list.append(my_list[0])

            last_index = len(my_list)-1
            my_list.pop(0)

        elif key in ['J']:
            #Press J key to incrment list down by 5.
            for i in range(5):
                last_index = len(my_list)-1
                my_list.append(my_list[0])

                last_index = len(my_list)-1
                my_list.pop(0)

        elif key in ['l', 'KEY_RIGHT']:
            #Open press l, opens up a putty session on the selected device.
            server = selected_item
            found = False
            #SSH program config here

            #If the server has a unique password.
            for folder, hosts in unique_hosts_dict.items():
                for host in hosts:
                    if server[1:] == host[0]:#[1:] because server has tab at start
                        #The .env variable needs to be assigned in the .csv file in the username/password fields.
                        UNIQUE_USER = config(host[1])
                        UNIQUE_PASS = config(host[2])
                        has_key = bool(host[3])

                        if PLATFORM == 'gnome-terminal':
                            try:
                                if(has_key):
                                    target="gnome-terminal -- ssh -i "+UNIQUE_PASS+" -o 'UserKnownHostsFile=/dev/null' -o 'StrictHostKeyChecking=no' ssh://"+UNIQUE_USER+"@"+server.strip()
                                else:
                                    target="gnome-terminal -- sshpass -p " + UNIQUE_PASS +" ssh -o 'UserKnownHostsFile=/dev/null' -o 'StrictHostKeyChecking=no' ssh://"+UNIQUE_USER+"@"+server.strip()
                                os.system(target)
                            except:
                                stdscr.addstr(1,1,'gnome-terminal command not found.')
                        elif PLATFORM == 'putty-linux':
                            try:
                                if(has_key):
                                    os.system('putty -ssh -l '+UNIQUE_USER+' -i '+UNIQUE_PASS+' '+server+' &')
                                else:
                                    os.system('putty -ssh -l '+UNIQUE_USER+' -pw '+UNIQUE_PASS+' '+server+' &')
                            except:
                                stdscr.addstr(1,1,'putty command not found.')
                        elif PLATFORM == 'putty-windows':
                            try:
                                if(has_key):
                                    os.system('START /B putty.exe -ssh -l '+UNIQUE_USER+' -i '+UNIQUE_PASS+' '+server)
                                else:
                                    os.system('START /B putty.exe -ssh -l '+UNIQUE_USER+' -pw '+UNIQUE_PASS+' '+server)
                            except:
                                stdscr.addstr(1,1,"putty.exe not found.  Make sure it's installed and on PATH.")
                        elif PLATFORM == 'xterm-terminal':
                            try:
                                if(has_key):
                                    target='xterm -hold -e \"sshpass -i '+UNIQUE_PASS+' ssh -o \'UserKnownHostsFile=/dev/null\' -o \'StrictHostKeyChecking=no\' ssh://'+UNIQUE_USER+'@'+server.strip()+'\" '
                                else:
                                    target='xterm -hold -e \"sshpass -p '+UNIQUE_PASS+' ssh -o \'UserKnownHostsFile=/dev/null\' -o \'StrictHostKeyChecking=no\' ssh://'+UNIQUE_USER+'@'+server.strip()+'\" '
                                os.system(target)
                            except:
                                stdscr.addstr(1,1,'xterm command not found.')
                        else:
                            stdscr.addstr(1, 1, '.env Variable PLATFORM is not set correctly.')  
                        found = True
                    else:
                        pass

            #For servers with the default password
            if found == False:
                if PLATFORM == 'gnome-terminal':
                    try:
                        target="gnome-terminal -- sshpass -p " + SSH_PASS +" ssh -o 'UserKnownHostsFile=/dev/null' -o 'StrictHostKeyChecking=no' ssh://"+SSH_USER+"@"+server.strip()
                        os.system(target)
                    except:
                        stdscr.addstr(1,1,'gnome-terminal command not found.')
                elif PLATFORM == 'putty-linux':
                    try:
                        os.system('putty -ssh -l '+SSH_USER+' -pw '+SSH_PASS+' '+server+' &')
                    except:
                        stdscr.addstr(1,1,'putty command not found.')
                elif PLATFORM == 'putty-windows':
                    try:
                        os.system('START /B putty.exe -ssh -l '+SSH_USER+' -pw '+SSH_PASS+' '+server)
                    except:
                        stdscr.addstr(1,1,'putty.exe not found in ssm folder. Please add it.')
                elif PLATFORM == 'xterm-terminal':
                    try:
                        target='xterm -hold -e \"sshpass -p '+SSH_PASS+' ssh -o \'UserKnownHostsFile=/dev/null\' -o \'StrictHostKeyChecking=no\' ssh://'+SSH_USER+'@'+server.strip()+'\" '
                        os.system(target)
                    except:
                        stdscr.addstr(1,1,'xterm command not found')

                else:
                    stdscr.addstr(3, 30, '.env Variable PLATFORM is not set correctly.')  
                    pass
        elif key == 'n':
            #new host function
            curses.curs_set(1)
            stdscr.clear()
            new_host_screen(stdscr)
            curses.curs_set(0)
            my_list, SSH_USER, SSH_PASS, unique_hosts_dict, PLATFORM = initiate_vars()

        elif key == 'd':
            #delete host
            stdscr.addstr(1,2,'DELETE host?(y/n) '+selected_item[1:], curses.A_STANDOUT)
            ans = stdscr.getkey()
            if(ans in ['y', 'Y']):
                #delete_host(selected_item[1:])
                hosts_csv.deleteLineWhere(selected_item[1:])
                #refresh
            else:
                stdscr.addstr(1,2,'Not deleted'+selected_item[1:]+' '+ans, curses.A_STANDOUT)
                ans = stdscr.getch()



        elif key == 'p':
            # Ping function
            stdscr.addstr(1, 1, selected_item + ' pinging . . . ', curses.color_pair(2))
            stdscr.refresh()
            if PLATFORM != 'putty-windows':
                ping_result = subprocess.run(['ping', '-c', '1', selected_item.strip()], stdout=subprocess.PIPE)
            else:
                ping_result = subprocess.run(['ping', '-n', '1', selected_item.strip()], stdout=subprocess.PIPE)

            if ping_result.returncode == 0:
                #if up then green
                stdscr.addstr(1, 1, selected_item + ' is up!\t\t', curses.color_pair(1))
            else:
                #if down then red
                stdscr.addstr(1, 1, selected_item + ' is down!\t\t', curses.color_pair(3))
            stdscr.getch()
        elif key == 't':
            #Toggle, temporarily remove host from list.
            if selected_item in my_list:
                my_list.remove(selected_item)
            else:
                my_list.append(selected_item)
        #Search function
        elif key == '/':
            stdscr.addstr(1,2,'Search: ', curses.A_STANDOUT)
            word=''
            #Prints search list as you type
            while True:
                key = stdscr.getkey()

                if key == "q":
                    break
                elif key == "j":
                    if word == '':
                        continue
                    #Check list to see if there is a valid host. Prevents infinite loop if no valid host IP in searched list.
                    valid=False
                    for i in filtered_list:
                        if i.find('\t') != -1:
                            valid=True
                            break
                        else:
                            pass


                    if filtered_list == [] and valid == True:
                        #SSH to device if no matching IP
                        #target="gnome-terminal -- sshpass -p " + SSH_PASS +" ssh -o 'UserKnownHostsFile=/dev/null' -o 'StrictHostKeyChecking=no' "+SSH_USER+"@"+word.strip()
                        #os.system(target)


                        pass
                    #Elif list not empty and valid host found jumped down
                    elif valid == True:
                        stdscr.addstr(1,2,'Search: '+word)
                        queue(stdscr, filtered_list)

                elif key == "KEY_BACKSPACE" and word != '':
                    word = word[:len(word)-1]
                elif key == "\r" or key == "\n":
                    pass
                elif len(key) > 1:
                    #Stops extra keys from printing on line.
                    pass
                else:
                    word += key

                #stdscr.addstr(30,40,word)
                #The list of hosts generated when you search
                filtered_list=[]
                
                #Adds hosts that match your search to the rendered list.
                for i in my_list:
                    if i.find(word) != -1 or i.find('\t') == -1:
                        filtered_list.append(i)
                    else:
                        pass
                stdscr.clear()
                try:
                    rectangle(stdscr, 2,2,max_y-2,40)
                    extra_text(stdscr)
                except:
                    pass

                if filtered_list != []:
                    print_list(stdscr, filtered_list, list_y, list_x)
                stdscr.addstr(1,2,'Search: '+word, curses.A_STANDOUT)

            stdscr.clear()

        elif key == 'q':
            #q to quit
            break
        elif key == '?':
            help_options = [('Movement', curses.A_STANDOUT), 'j - down', 'k - up', 'l - open selected session.', 'J - Move down by 5', 'K - Move up by 5',
                            ('Searching', curses.A_STANDOUT), '/ - To begin search.', 'j - To select an option.', 'q - Go back/quit', 'Note: you can search within lists. q to break out.',
                            ('Config Files', curses.A_STANDOUT), f'Stored at: {datastore}','n - create a new host',
                            ('Host manipulation', curses.A_STANDOUT), 't - Toggle, temporarily removes selected host from list.', 'p - pings the selected host.', 'd - delete the host(deletes first IP match in hosts.csv)']

            #Generate side menu from options list.
            side_menu(stdscr, help_options)

        else:
            pass

        stdscr.refresh()
        stdscr.clear()

        #Try to render the list
        try:
            print_list(stdscr, my_list, list_y, list_x)
        except:
            pass


def read_csv(csv_file):
    unique_hosts=defaultdict(list)
    hosts = defaultdict(list)
    with open(csv_file, newline='') as hosts_file:
        reader = csv.DictReader(hosts_file)
        for row in reader:
            if row['username'] != None and row['password'] != None:
                unique_hosts[row['location']].append((row['ip'], row['username'], row['password'], row['ssh_key']))

            hosts[row['location']].append(row['ip'])

    return dict(hosts), dict(unique_hosts)

def read_csv_make_string(csv_file):
    #Returns the csv file data as a formatted string.
    #Currently, not used in the program but may be useful.

    with open(csv_file, newline='') as hosts_file:
        comma_sep_string = ''
        reader=csv.reader(hosts_file)
        for row in reader:
            comma_sep_string += ','.join(row)
            comma_sep_string +='\n'

    #print(comma_sep_string)
    return comma_sep_string

def dict_to_list(data: dict):
    #generates a list from csv dictinoary.
    data_list=[]

    for folder, hosts in data.items():
        data_list.append(folder)
        for host in hosts:
            data_list.append('\t'+str(host))
    return data_list

def initiate_vars():
    #Grabs credentials and host dict as defined in hosts.csv and .env
    PATH = config('HOST_PATH')
    SSH_USER = config('SSH_USER')
    SSH_PASS = config('SSH_PASS')
    PLATFORM = config('PLATFORM')

    # CMD Check - CMD line args for runtime variables.
    for i, arg in enumerate(sys.argv):
        if arg == '-h':
            print("""Usage: ssm [OPTIONS] Value [-u] [-p] [-c] [-h] [-t]
            Usage to temporarily change default user and password: python3 nframes.py -u [SSH_USER] -p
                    OR if alias set:  ssm -u [SSH_USER] -p
            [-u] SSH_USER
            [-p] SSH_PASS
            [-c] HOST_PATH
            [-h] Help
            [-t] Terminal emulator for SSH sessions. [Default: gnome-terminal] [Options: xterm-terminal, putty-windows, putty-linux]

                    """)
            sys.exit()
        elif arg == '-c':
            #Specify hosts.csv file path
            PATH = sys.argv[i+1]
        elif arg == '-u':
            #Specify .env SSH_USER variable
            SSH_USER = sys.argv[i+1]
        elif arg == '-p' and SSH_PASS == config('SSH_PASS'):
            #Specify .env SSH_PASS variable
            SSH_PASS = getpass.getpass('Temp default session password: ')
            print(config('SSH_PASS'))
        elif arg == '-t':
            #Specify a terminal emulator
            PLATFORM = sys.argv[i+1]
        else:
            pass

    #Create dictionary
    hosts_dict, unique_hosts_dict = read_csv(PATH)
    #hosts_dict -- {'location': [ip, ip]}
    #unique_hosts_dct -- {'location': [(ip, usr, pass, T/F)]}

    hosts_list = dict_to_list(hosts_dict)
    #print(unique_hosts_dict)

    return hosts_list, SSH_USER, SSH_PASS, dict(unique_hosts_dict), PLATFORM

def side_menu(stdscr, option_list):
    #Generates a menu beside the rectangle from a list.  Headers can be created by tuple(str, curses.FONT_TYPE)
    for i in range(len(option_list)):
        option=option_list[i]
        if type(option) == tuple:
            stdscr.addstr(i+2, 42, option[0], option[1])
        else:
            stdscr.addstr(i+2, 42, '  '+option)
    stdscr.getch()
    stdscr.clear()

if __name__ == "__main__":
    initiate_vars()
    wrapper(queue)

