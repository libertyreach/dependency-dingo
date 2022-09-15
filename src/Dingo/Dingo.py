from dlldiag.common import ModuleHeader, OutputFormatting, StringUtils, WindowsApi
from termcolor import colored
import argparse, os, sys
import shutil
import itertools
import logging as log


def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))


def enumerateDependencies(plugin):
    log.info("ENUMERATE: " + plugin)
    # Parse the PE header for the module
    header = ModuleHeader(plugin)
    architecture = header.getArchitecture()
    imports = header.listAllImports()
    return imports


def findInFolders(folders, dependencies):
    copy_from = []
    for folder in folders:
        f = findInFolder(folder, dependencies)
        copy_from += f
    return copy_from


def findInFolder(folder, dependencies):
    copy_from = []
    log.info("SEARCH: " + folder)
    for (
        root,
        dirs,
        files,
    ) in os.walk(folder):
        here = intersection(files, dependencies)
        for item in here:
            if "Qt5" not in item and "api-ms" not in item:
                log.info("  FOUND: " + item)
                item_path = os.path.join(root, item)
                copy_from.append(item_path)
    return copy_from


def search(
    plugins_folder, source_folders, destination_folder, search_depth, verbose=False
):
    try:
        log.info("Locating dependencies, please wait...")
        # Ensure the module path is an absolute path
        plugins = [
            os.path.join(plugins_folder, f)
            for f in os.listdir(plugins_folder)
            if os.path.isfile(os.path.join(plugins_folder, f)) and ".dll" in f
        ]

        dependencies = []
        enumerated_ignore = []
        for plugin in plugins:
            dependencies += enumerateDependencies(plugin)
            dependencies = StringUtils.uniqueCaseInsensitive(dependencies, sort=True)
            # walk and search
        copy_from = findInFolders(source_folders, dependencies)
        t_deps = copy_from
        # begin recursive search

        for iteration in range(search_depth):
            if not t_deps:
                log.info(
                    "Depends list is empty, exiting early on iteration {}".format(
                        iteration
                    )
                )
                break
            t_deps = StringUtils.uniqueCaseInsensitive(t_deps, sort=True)
            t_deps = [x for x in t_deps if x not in enumerated_ignore]
            for d in t_deps:
                if d not in enumerated_ignore:
                    e = enumerateDependencies(d)
                    enumerated_ignore.append(d)
                    found = findInFolders(source_folders, e)
                    for f in found:
                        if f not in enumerated_ignore and f not in copy_from:
                            t_deps.append(f)
                t_deps.remove(d)

        copy_from = StringUtils.uniqueCaseInsensitive(enumerated_ignore, sort=True)
        for src in copy_from:
            basename = os.path.basename(src)
            dst = os.path.join(destination_folder, basename)
            shutil.copy(src, dst)
            log.info(src + " -> " + dst)

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
    parser.add_argument(
        "-v",
        dest="verbose",
        default=False,
        help="Print verbose output",
        action=argparse.BooleanOptionalAction,
    )
    parser.add_argument(
        "-d",
        dest="depth",
        default=10,
        help="Depth of search for dependency dependencies",
        action=argparse.BooleanOptionalAction,
    )
    parser.add_argument(
        "-s",
        dest="search",
        help="Location of .dlls, typically 3rdparty folder",
        action="append",
        nargs="+",
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
    if not args.dest or not args.search or not args.folder:
        parser.print_help()
        sys.exit(0)
    if args.verbose:
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
    else:
        log.basicConfig(format="%(levelname)s: %(message)s")

    args.folder = os.path.abspath(args.folder)
    args.dest = os.path.abspath(args.dest)
    tmp_search = []
    for s in itertools.chain(*args.search):
        tmp_search.append(os.path.abspath(s))
    sys.path.insert(0, args.dest)
    sys.path.insert(0, args.dest + "/..")
    search(args.folder, tmp_search, args.dest, args.depth, args.verbose)


if __name__ == "__main__":
    main()
