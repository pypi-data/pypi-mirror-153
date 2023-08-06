import os

import click

from curses_playlist.controller import PlistController


@click.command
@click.option(
    "--playlist", "-p", help="specify location to write playlist to", required=True
)
@click.option(
    "--working-directory", "-w", help="Where to look for video files", default="."
)
def main(playlist: str, working_directory: str):
    if working_directory != ".":
        os.chdir(working_directory)

    PlistController(playlist)


if __name__ == "__main__":
    main()
