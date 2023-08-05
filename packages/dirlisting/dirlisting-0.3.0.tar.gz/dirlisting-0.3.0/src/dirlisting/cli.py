import sys

import click

from dirlisting import __version__
from dirlisting.dirlisting import Dirlisting


@click.command()
@click.version_option(version=__version__)
@click.option(
    "-s",
    "--sort",
    "is_sort",
    is_flag=True,
    default=False,
    help="Sort the directory entries.",
)
@click.option(
    "-d",
    "--dirsfirst",
    "is_dirsfirst",
    is_flag=True,
    default=False,
    help="List directories before files.",
)
@click.option(
    "-o", "--output", type=click.File("w"), default=None, help="Output to this file."
)
@click.argument("file", type=click.File())
def app(is_sort, is_dirsfirst, output, file):
    """Create a directory listing given an input FILE.

    The input should be a yaml file with directories having a colon
    after them and files without.

    Example:
        This is a very simple input file.::

            \b
            - topdir:
              - file1.txt
              - somedir:
                - another_file.txt
    """
    listing = Dirlisting(file, out=output)
    listing.print(is_sort=is_sort, is_dirsfirst=is_dirsfirst)


if __name__ == "__main__":
    app()
