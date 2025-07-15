import argparse
from importlib.metadata import version


def get_version():
    return version('gh-testing')

def main():
    parser = argparse.ArgumentParser(description="gh-testing CLI")
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    args = parser.parse_args()

    if args.version:
        print(f"gh-testing version {get_version()}")
    else:
        print("Hello from gh-testing!")


if __name__ == "__main__":
    main()
