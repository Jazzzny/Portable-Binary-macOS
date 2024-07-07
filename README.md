# Portable Binary
Turn macOS binaries installed by package managers (Macports, Homebrew) into portable binaries.

## Usage (GUI)
Download the latest release from the [releases page](https://github.com/Jazzzny/Portable-Binary-macOS/releases) for your platform:
- Mac OS X 10.4-10.5 PowerPC (or Rosetta)
- Mac OS X 10.6+ Intel 32-bit/64-bit
- macOS 11.0+ Apple silicon/Intel 64-bit

Alternatively, run the following command in the terminal:
```bash
$ python3 ./PortableBinaryGUI.py
```
Note that Python 3.6 or later is required (Python 2 is not supported).


## Usage (CLI)
```bash
$ python3 ./PortableBinary.py /path/to/binary /path/to/output/directory
```