from dlldiag.common import ModuleHeader, OutputFormatting, StringUtils, WindowsApi
from termcolor import colored
import argparse, os, sys
import shutil
import itertools
import logging as log

def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))


def search(plugins_folder, source_folders, destination_folder, verbose = False)
    try:
        log.info("Locating dependencies, please wait...")
        # Ensure the module path is an absolute path
        plugins = [
            os.path.join(plugins_folder, f)
            for f in os.listdir(plugins_folder)
            if os.path.isfile(os.path.join(plugins_folder, f)) and ".dll" in f
        ]

        dependencies = []
        for plugin in plugins:
            log.info("Finding dependencies for" + plugin)
            # Parse the PE header for the module
            header = ModuleHeader(plugin)
            architecture = header.getArchitecture()
            imports = header.listAllImports()
            dependencies += imports
            dependencies = StringUtils.uniqueCaseInsensitive(dependencies, sort=True)

        # walk and search
        copy_from = []
        copy_to = []
        for folder in source_folders:
            log.info("Searching in" ,folder,"for dependencies.")
            for (
                root,
                dirs,
                files,
            ) in os.walk(folder):
                here = intersection(files, dependencies)
                for item in here:
                    if "Qt" not in item:
                        copy_from.append(os.path.join(root, item))
                        copy_to.append(os.path.join(destination_folder, item))
            log.info("Copying into", destination_folder)
        for src, dst in zip(copy_from, copy_to):
            shutil.copy(src, dst)
            log.info(src, "->", dst)

    except RuntimeError as e:
        log.error("Error: {}".format(e))
        sys.exit(1)

def main():
    # Our supported command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "folder",
        default="D:/plugins",
        help="Plugins folder for which direct dependencies will be loaded, typically plugins folder",
    )
    parser.add_argument("-v", dest="verbose", default=False,help="Print verbose output")
    parser.add_argument(
        "-s",
        dest = "search",
        default="D:/3rdparty",
        help="Location of .dlls, typically 3rdparty folder",
    )
    parser.add_argument(
        "--dest",
        default="dependency",
        help="Folder location to copy dependency .dlls into, typically dependency",
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
    if args.verbose:
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
        log.info("Verbose output.")
    else:
        log.basicConfig(format="%(levelname)s: %(message)s")
    
    args.folder = os.path.abspath(args.folder)
    args.dest = os.path.abspath(args.dest)
    args.bin = os.path.abspath(args.bin)
    sys.path.insert(0, args.dest)
    sys.path.insert(0, args.dest + "/..")

    search(args.folder, args.search, args.dest, args.verbose)




if __name__ == "__main__":
    main()
