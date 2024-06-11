"""dspyfun CLI."""

import typer

from dspyfun.utils.cli_tools import load_commands

app = typer.Typer()

if __name__ == "__main__":
    load_commands()
    app()
else:
    load_commands()
