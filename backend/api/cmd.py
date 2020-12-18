import getopt
import sys
from pathlib import Path

from func.db import db
from func.init import init


def handle(argv):
    opts, args = getopt.getopt(argv, '-h-s:-v-i', ['help', 'searchpath=', 'version', 'init'])
    for opt_name, opt_value in opts:
        if opt_name in ('-h', '--help'):
            print("[*] Help info")
            print("-h, --help\tshow this help info.")
            print("-v, --version\tshow version info.")
            print("-s, --searchpath\tdefine the search path of videos.")
            print(
                "-i, --init\tinit database (This action will be auto executed later, but you should execute it before "
                "any other operation to prevent error.)")
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


def searchpath(path: str):
    basepath = Path(path)
    files_in_basepath = (entry for entry in basepath.iterdir() if entry.is_file())
    for item in files_in_basepath:
        if item.name.split(".")[-1] in ['mp4']:
            print(item.name)


if __name__ == '__main__':
    handle(argv=sys.argv[1:])
