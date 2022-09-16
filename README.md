# DependencyDingo

DependencyDingo is a Python library for helping Liberty Reach engineers resolve deployment and dependency locating ussues.

Given a directory to use, a list of directories to search, and a destination directory, it will gather a list of secondary dependencies for each .dll in the given folder, then it will proceed to search the `search` directories recursively for the required dependencies.

## Building and Installation

```bash
git clone https://github.com/libertyreach/dependency-dingo.git
cd dependency-dingo
pip install --upgrade pip
pip install --upgrade build 
pip install dll-diagnostics
python -m build
pip install dist\Dingo-0.0.2.tar.gz
```

## Usage

```bash
cd vguide\Application\Executable
dingo -s "D:\3rdparty" "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.1\bin" -v --dest dependency plugins

```

```python
import Dingo.Dingo as dingo
dingo.search("plugins", ["D:\\3rdparty", "C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v10.1\\bin"], "dependency", 15, True)
```
```
usage: Dingo.py [-h] [-v] [-d] [-s SEARCH [SEARCH ...]] [--dest DEST] folder

positional arguments:
  folder                Plugins folder for which direct dependencies will be loaded, typically plugins folder

options:
  -h, --help            show this help message and exit
  -v                    Print verbose output (default: False)
  -d                    Depth of search for dependency dependencies (default: 10)
  -s SEARCH [SEARCH ...]
                        Location of .dlls, typically 3rdparty folder
  --dest DEST           Folder location to copy dependency .dlls into, typically dependency
```
