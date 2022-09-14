from dlldiag.common import ModuleHeader, OutputFormatting, StringUtils, WindowsApi
from termcolor import colored
import argparse, os, sys
import shutil
import itertools


def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))


def main():
    # Our supported command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "folder", help="Plugins folder for which direct dependencies will be loaded"
    )

    parser.add_argument(
        "--bin", default="all", help="Location of .dlls, typically 3rdparty folder"
    )
    parser.add_argument(
        "--dest",
        default="dependency",
        help="Folder location to copy dependency .dlls into",
    )
    # If no command-line arguments were supplied, display the help message and exit
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(0)

    # Parse the supplied command-line arguments
    args = parser.parse_args()
    if not args.dest or not args.bin or not args.folder:
        parser.print_help()
        sys.exit(0)
    try:
        print("Locating dependencies, please wait...")
        # Ensure the module path is an absolute path
        args.folder = os.path.abspath(args.folder)
        args.dest = os.path.abspath(args.dest)
        args.bin = os.path.abspath(args.bin)
        sys.path.insert(0, args.dest)
        sys.path.insert(0, args.dest + "/..")
        plugins = [
            os.path.join(args.folder, f)
            for f in os.listdir(args.folder)
            if os.path.isfile(os.path.join(args.folder, f)) and ".dll" in f
        ]
        dependencies = []
        for plugin in plugins:
            print("\tFinding dependencies for", plugin)
            # Parse the PE header for the module
            header = ModuleHeader(plugin)
            architecture = header.getArchitecture()
            imports = header.listAllImports()
            dependencies += imports
            dependencies = StringUtils.uniqueCaseInsensitive(dependencies, sort=True)

        # walk and search
        copy_from = []
        copy_to = []
        print("Searching in", args.bin, "for dependencies.")
        for (
            root,
            dirs,
            files,
        ) in os.walk(args.bin):
            here = intersection(files, dependencies)
            for item in here:
                if "Qt" not in item:
                    copy_from.append(os.path.join(root, item))
                    copy_to.append(os.path.join(args.dest, item))
        print("Copying into", args.dest)
        for src, dst in zip(copy_from, copy_to):
            shutil.copy(src, dst)
            print(src, "->", dst)

    except RuntimeError as e:
        print("Error: {}".format(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
