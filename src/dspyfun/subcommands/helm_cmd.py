"""Helm operations."""
import typer

from dspyfun.utils.cli_tools import run_command

app = typer.Typer()


@app.command(name="install")
def install_helm() -> None:
    """Install Helm v3"""
    print("Installing Helm v3...")
    run_command("curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash")
