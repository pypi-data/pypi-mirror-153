import time
import ssm.nframes
from ssm.nframes import queue
from ssm.nframes import initiate_vars
from curses import wrapper
from decouple import config, AutoConfig

from ssm.datastore import *


def main():
#The only relevant line of code if not using a monitor server.
    initiate_vars()
    wrapper(queue)

if __name__ == "__main__":
    main()





