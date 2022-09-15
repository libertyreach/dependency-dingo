# DependencyDingo

DependencyDingo is a Python library for helping Liberty Reach engineers resolve deployment and dependency locating ussues.

## Installation

```bash
pip install -i requirements.txt
```

## Usage

```bash
cd vguide\Application\Executable
python Dingo.py -s "D:\3rdparty" "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.1\bin" -v --dest dependency plugins

```
```
usage: Dingo.py [-h] [-v] [-s SEARCH [SEARCH ...]] [--dest DEST] folder

positional arguments:
  folder                Plugins folder for which direct dependencies will be loaded, typically plugins folder

options:
  -h, --help            show this help message and exit
  -v                    Print verbose output (default: False)
  -s SEARCH [SEARCH ...]
                        Location of .dlls, typically 3rdparty folder
  --dest DEST           Folder location to copy dependency .dlls into, typically dependency
```