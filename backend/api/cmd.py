import getopt
import sys

from func.db import db
from func.init import init
from func.utils import searchpath, update_database


def handle(argv):
    opts, args = getopt.getopt(argv, '-h-s:-v-i-u', ['help', 'searchpath=', 'version', 'init', 'update'])
    for opt_name, opt_value in opts:
        if opt_name in ('-h', '--help'):
            print("[*] Help info")
            print("-h, --help\tshow this help info.")
            print("-v, --version\tshow version info.")
            print("-s, --searchpath\tdefine the search path of videos.")
            print(
                "-i, --init\tinit database (This action will be auto executed later, but you should execute it before "
                "any other operation to prevent error.)")
            print("-u, --update\tupdate database to new format")
            sys.exit()
        if opt_name in ('-v', '--version'):
            print("[*] Version is 0.01 ")
            sys.exit()
        if opt_name in ('-i', '--init'):
            init(quiet=False)
            db.close()
            sys.exit()
        if opt_name in ('-s', '--searchpath'):
            searchpath(opt_value)
            sys.exit()
        if opt_name in ('-u', '--update'):
            update_database()
            sys.exit()


if __name__ == '__main__':
    handle(argv=sys.argv[1:])
