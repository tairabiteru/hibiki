from hibiki import HibikiRenderer
import sys


def main() -> int:
    if len(sys.argv) == 1:
        print("Missing argument: file path\nUsage: hibiki /path/to/file.hb")
        return 1

    try:
        with open(sys.argv[1], "r") as source_file:
            source = source_file.read()

        output = HibikiRenderer().render(source)
        print(output)
        return 0
    except FileNotFoundError:
        print(f"'{sys.argv[1]}' file does not exist.")
        return 2
    except PermissionError:
        print(f"Permission denied when opening '{sys.argv[1]}'")
        return 3


if __name__ == "__main__":
    main()
