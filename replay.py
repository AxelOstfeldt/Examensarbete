import sys
import os

command = "udpreplay -i lo " + sys.argv[1]
os.system(command)