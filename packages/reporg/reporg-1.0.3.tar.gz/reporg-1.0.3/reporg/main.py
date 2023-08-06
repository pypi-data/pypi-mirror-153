# See LICENSE for details

"""CLI for reporg."""

import click

from reporg.org import org
from reporg.__init__ import __version__

@click.command()
@click.version_option(version=__version__)
@click.option('--dir', '-d', default='', type=click.Path(), help='Work directory path')
@click.option('--clean','-c', is_flag='True', help='Clean builds')
@click.option('--list', default='list.yaml', help='List of repos')
def cli(dir, clean, list):
    org(dir, clean, list)

if __name__ == '__main__':
    cli()
