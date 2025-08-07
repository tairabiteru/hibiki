from hibiki import Tab
import sys


def main() -> int:
    if len(sys.argv) == 1:
        print("Missing argument: file path\nUsage: hibiki /path/to/file.hb")
        return 1
    
    try:
        tab = Tab.from_path(sys.argv[1])
        print(tab.render())
        return 0
    except FileNotFoundError:
        print(f"'{sys.argv[1]}' file does not exist.")
        return 2
    except PermissionError:
        print(f"Permission denied when opening '{sys.argv[1]}'")
        return 3


if __name__ == "__main__":
    main()