from hibiki import render_file
import sys


def main() -> int:
    if len(sys.argv) == 1:
        print("Missing argument: file path\nUsage: hibiki /path/to/file.hb")
        return 1

    try:
        print(render_file(sys.argv[1]))
        return 0
    except FileNotFoundError:
        print(f"'{sys.argv[1]}' file does not exist.")
        return 2
    except PermissionError:
        print(f"Permission denied when opening '{sys.argv[1]}'")
        return 3


if __name__ == "__main__":
    main()
