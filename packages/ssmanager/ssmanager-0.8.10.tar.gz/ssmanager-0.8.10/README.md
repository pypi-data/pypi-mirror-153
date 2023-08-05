
## Simple SSH Manager (SSM)  
SSM is a lightweight Python ncurses based SSH manager.

### Requirements  
OS: Windows, Linux, MacOS
Python: Python version >=3
Terminal: Putty installed and callable from CLI.(Default, can be changed.)


## Startup  
1. To install run: `pip install -r requirements.txt`
2. To install run: `pip install ssmanager`
3. Type `ssm` in a new terminal to start the app.

## Interpreting from source(Optional)

### Installation  
For installation, you essentially just need to clone the repository and define a few variables.

1. Clone the repo into a directory of your choosing.  
   `git clone https://github.com/Lonestar137/ssm.git`

2. Download the python dependencies: curses(ncurses), python-decouple.   
   **Windows** 
   Example:
   `pip3 install -r requirements.txt`  
   or just
   `pip install` for Windows/Other distros.
   NOTE: For Windows, you will need to run `pip install windows-curses` instead.

   Install a supported SSH terminal handler for your OS:

   **Ubuntu(Linux)**  
   Make sure you have gnome-terminal, putty, or xterm installed.  
   `sudo apt install putty` or `xterm`
   gnome-terminal should be installed by default on standard Ubuntu/GNOME based distros.

   Defining which terminal to use is covered lower in the file, there are a variety to select from.

   **Windows**  
   Download [putty](https://www.putty.org/).  Make sure that putty is callable from the command line, meaning the putty.exe is on the system PATH.

By default `SSH_USER` and `SSH_PASS` will be used on all sessions unless you specify a different variable in the `hosts.csv` username and password fields.  
You can define unique username and password for each host if you wish, otherwise `SSH_USER` and `SSH_PASS` will be used on that host.

3. Afterward, you can start the application from that directory by typing in a terminal:
   `python3 ssm/main.py`


## Configuration  
Location of configuration files can be found by typing `?` in the application.  
There are two files to take into account.  The `.env` file which contains session passwords and configuration options and the `hosts.csv`.  
The `hosts.csv` file is your database of session information.  You can manually edit either file if preferred, or use the built in functionality to automatically edit the files.

### Support for ssh-keys  
Support for SSH_KEYS can be enabled on a host by setting the ssh_key column value = to `True` and the path to the key equal to the password column variable.  

#### Example manually creating a host:   
Inside Hosts.csv:  `HostFolder,10.1.1.1,MYUSER,MYKEYFILE,True`
Inside .env: `MYUSER=genericUser123`
Inside .env: `MYKEYFILE=path/to/keyfile.pem`

The advantage is that hosts.csv can easily be distributed to other systems, user/password columns merely reference a variable in .env so there is no risk of accidentally exposing sensitive information as long as the .env file is not also shared.

### Defining a different port      
Note: currently, all terminals support variable port assignment EXCEPT Putty.

To use a different port simply define it in your hosts.csv like so: `Home,10.1.1.1:9999`  

### Changing the SSH terminal  
By default, putty is used for Windows and Unix-like systemds.  
In the `.env` file, set `PLATFORM` equal to one of the supported SSH terminals.
For example:  `PLATFORM=putty-windows` or `PLATFORM=gnome-terminal`  
Options:
    putty-linux, putty-windows, gnome-terminal, xterm-terminal

### Keybinds  
You can see a list of keybinds if you press  `?` from the main SSM menus.  
`j, k` - down, up 
`J, K` - down+5, up+5 
`d` - On a host to delete it. Note that deleting a host does not delete the password variable stored in `.env`.  
`p` - Ping the host.  
`l` - Open a shell to the selected host.  
`/` - Search the hosts using regex.  

### Troubleshooting  
1. `_curses` not found.  
This is a Windows issue where the Python `curses` module uses a different package name.  You simply need to run `pip install windows-curses`

2. `putty.exe` not found.  
You need to make sure that `putty` was installed correctly.  The `putty.exe` needs to be stored in a location on your systems PATH. To see currently avail folders type: `echo $PATH`.  Putty should be stored in one of those folders or added to the PATH.

