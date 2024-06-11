"""Google Cloud (gc) operations."""
import subprocess
import inquirer

import typer

from dspyfun.utils.cli_tools import run_command

from dspyfun import DspyfunConfig

app = typer.Typer()
config = DspyfunConfig()


@app.command(name="install")
def install_gcloud_sdk() -> None:
    """Install Google Cloud SDK"""
    print("Installing Google Cloud SDK...")
    run_command("curl https://sdk.cloud.google.com | bash")
    run_command("exec -l $SHELL")
    run_command("gcloud init")


@app.command(name="create")
def create_cluster(name: str = typer.Argument(config.cluster_name),
                   zone: str = typer.Argument(config.zone),
                   project: str = typer.Argument(config.project_id)) -> None:
    """Create a new GKE cluster"""
    print(f"Creating GKE cluster: {name} {zone} {project}...")
    run_command("gcloud services enable container.googleapis.com")
    run_command(f"gcloud container clusters create {name} --zone {zone} --project {project}")


@app.command(name="firewall")
def setup_firewall(name: str = typer.Argument(config.cluster_name)) -> None:
    """Setup firewall rules for sidecar injection"""
    print(f"Setting up firewall rules for cluster: {name}...")
    firewall_rule_name = subprocess.check_output(
        f"gcloud compute firewall-rules list --filter=name~gke-{name}-[0-9a-z]*-master --format=value(name)",
        shell=True
    ).decode("utf-8").strip()
    run_command(f"gcloud compute firewall-rules update {firewall_rule_name} --allow tcp:10250,tcp:443,tcp:4000")


@app.command(name="creds")
def get_credentials(name: str = typer.Argument(config.cluster_name),
                    zone: str = typer.Argument(config.zone),
                    project: str = typer.Argument(config.project_id)) -> None:
    """Retrieve credentials for kubectl"""
    print(f"Retrieving credentials for cluster: {name}...")
    run_command(f"gcloud container clusters get-credentials {name} --zone {zone} --project {project}")


@app.command(name="proj")
def check_current_project() -> None:
    """Check the current Google Cloud project"""
    print("Checking current Google Cloud project...")
    run_command("gcloud config get-value project")


@app.command(name="set-proj")
def set_project(project: str = typer.Argument(config.project_id)) -> None:
    """Set the Google Cloud project"""
    print(f"Setting Google Cloud project to: {project}...")
    run_command(f"gcloud config set project {project}")


@app.command(name="perm")
def check_user_permissions(project: str = typer.Argument(config.project_id)) -> None:
    """Check the user's permissions for the specified project"""
    print(f"Checking user permissions for project: {project}...")
    run_command(f"gcloud projects get-iam-policy {project}")


@app.command(name="login")
def login() -> None:
    """Login to Google Cloud"""
    print("Logging into Google Cloud...")
    run_command("gcloud auth login")


@app.command(name="net")
def check_network_connectivity() -> None:
    """Check network connectivity to Google Cloud services"""
    print("Checking network connectivity to Google Cloud services...")
    run_command("ping googleapis.com")


@app.command(name="quota")
def check_service_quotas() -> None:
    """Check the service quotas for the current project"""
    print("Checking service quotas for the current project...")
    run_command("gcloud services list --available")
    run_command("gcloud services list --enabled")


@app.command(name="retry")
def retry_enable_service() -> None:
    """Retry enabling the container.googleapis.com service"""
    print("Retrying enabling the container.googleapis.com service...")
    run_command("gcloud services enable container.googleapis.com")

@app.command(name="list")
def list_projects() -> None:
    """List available Google Cloud projects"""
    print("Listing available Google Cloud projects...")
    run_command("gcloud projects list")


@app.command(name="set")
def set_project() -> None:
    """Set the Google Cloud project using an interactive menu"""
    print("Fetching list of available Google Cloud projects...")
    result = subprocess.run(
        "gcloud projects list --format='value(projectId)'",
        shell=True,
        check=True,
        capture_output=True,
        text=True
    )

    projects = result.stdout.strip().split("\n")

    if not projects:
        print("No projects found.")
        return

    questions = [
        inquirer.List(
            'project',
            message="Select a Google Cloud project",
            choices=projects
        )
    ]

    answers = inquirer.prompt(questions)
    selected_project = answers['project']

    print(f"Setting Google Cloud project to: {selected_project}...")
    run_command(f"gcloud config set project {selected_project}")