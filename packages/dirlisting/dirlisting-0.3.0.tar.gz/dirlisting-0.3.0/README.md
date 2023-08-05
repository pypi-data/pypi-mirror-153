# dirlisting

Create a directory tree listing from a text file for use in documentation.

There are plenty of good tools out there to produce directory tree listings from an
existing directory structure. This tool handles the situation when you don't have and
don't want to create a directory structure for the sole purpose of producing a directory
tree listing for a document or email.

## Installation

```bash
$ pip install dirlisting
```

## Usage

`dirlisting` can be used to create a directory tree listing that looks like those
created with the `tree` command, but from a text file instead of walking an actual
directory tree.

### From code

```python
from dirlisting.dirlisting import Dirlisting
with open("input.yaml") as f:
    listing = Dirlisting(f)
listing.print()
```

### From the command line

Just use `dirlisting <filename>`.

``` none
dirlisting [OPTIONS] FILE

  Create a directory listing given an input FILE.

Options:
  --version    Show the version and exit.
  --sort       Sort the directory entries.
  --dirsfirst  List directories before files.
  --help       Show this message and exit.
```

### File format

The input file is a [yaml](https://yaml.org/) file. The contents of a directory are
sequences, files are final strings (`- filename`), and directories are mappings (`-
dirname:`). A listing would look like the following.

:::::{grid} 2
::::{grid-item-card} YAML File
```yaml
- topdir:
  - emptydir:
  - file1.txt
  - file2.txt
  - subdir:
    - file3.txt
```
::::
::::{grid-item-card} Output
```
topdir
├── emptydir
├── file1.txt
├── file2.txt
└── subdir
    └── file3.txt
```
::::
:::::

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this
project is released with a Code of Conduct. By contributing to this project, you agree
to abide by its terms.

## License

`dirlisting` was created by Stephan Poole. It is licensed under the terms of the MIT
license.

## Credits

`dirlisting` was created with
[`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the
`py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
