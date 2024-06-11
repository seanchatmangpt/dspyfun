"""Kubernetes (k8s) operations."""

import typer

from dspyfun.utils.cli_tools import run_command


app = typer.Typer()


@app.command(name="install")
def k8_install():
    """Install kubectl"""
    print("Installing kubectl...")
    run_command("gcloud components install kubectl")


@app.command(name="fix")
def fix_dashboard() -> None:
    """Fix Kubernetes dashboard permissions"""
    print("Fixing Kubernetes dashboard permissions...")
    run_command("kubectl create clusterrolebinding kubernetes-dashboard -n kube-system --clusterrole=cluster-admin --serviceaccount=kube-system:kubernetes-dashboard")
