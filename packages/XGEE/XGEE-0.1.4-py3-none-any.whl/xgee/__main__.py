from .xgee import DEFAULT_PATH,start
import sys

def main():
    path2apps=DEFAULT_PATH
    if len(sys.argv)>1:
        path2apps=sys.argv[1]
    start(path2apps)     

if __name__ == "__main__":
    main()
