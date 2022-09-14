# DependencyDingo

DependencyDingo is a Python library for helping Liberty Reach engineers resolve deployment and dependency locating ussues.

## Installation

```bash
pip install -i requirements.txt
```

## Usage

```bash
cd vguide\Application\Executable
python Dingo.py --bin "D:\3rdparty" --dest "dependency" "plugins"
```
```bash
usage: Dingo.py [-h] [--bin BIN] [--dest DEST] folder

positional arguments:
  folder       Plugins folder for which direct dependencies will be loaded

options:
  -h, --help   show this help message and exit
  --bin BIN    Location of .dlls
  --dest DEST  Folder location to copy dependency .dlls into
```