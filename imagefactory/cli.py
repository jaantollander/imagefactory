# -*- coding: utf-8 -*-

import click

from imagefactory.imagefactory import create_image


# TODO: confirm for overwriting file is exists
# TODO: Verbosity


@click.command()
@click.version_option()
@click.option('--name', '-n', default='untitled')
@click.option('--width', '-w', default=48)
@click.option('--height', '-h', default=48)
@click.option('--filetype', '-ft', default='png')
@click.option('--text', '-t', default=None)
@click.option('--savedir', '-d', default=None)
def main(name, width, height, filetype, text, savedir):
    """Console script for imagefactory"""
    create_image(name, width, height, filetype, text, savedir)


if __name__ == "__main__":
    main()
