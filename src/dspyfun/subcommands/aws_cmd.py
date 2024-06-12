"""AWS operations."""
import subprocess
import inquirer

import typer

from dspyfun.utils.cli_tools import run_command

from dspyfun import DspyfunConfig

app = typer.Typer()
config = DspyfunConfig()


@app.command(name="install")
def install_aws_cli() -> None:
    """Install AWS CLI"""
    print("Installing AWS CLI...")
    run_command("curl \"https://awscli.amazonaws.com/AWSCLIV2.pkg\" -o \"AWSCLIV2.pkg\"")
    run_command("sudo installer -pkg AWSCLIV2.pkg -target /")
    run_command("aws configure")


@app.command(name="create")
def create_cluster(name: str = typer.Argument(config.cluster_name),
                   region: str = typer.Argument(config.region),
                   profile: str = typer.Argument(config.profile)) -> None:
    """Create a new EKS cluster"""
    print(f"Creating EKS cluster: {name} {region} {profile}...")
    run_command(f"aws eks create-cluster --name {name} --region {region} --profile {profile} --role-arn <role-arn> --resources-vpc-config subnetIds=<subnet-ids>,securityGroupIds=<security-group-ids>")


@app.command(name="firewall")
def setup_firewall(cluster_name: str = typer.Argument(config.cluster_name),
                   region: str = typer.Argument(config.region),
                   profile: str = typer.Argument(config.profile)) -> None:
    """Setup firewall rules for sidecar injection"""
    print(f"Setting up firewall rules for cluster: {cluster_name} in region: {region}...")
    run_command(f"aws ec2 authorize-security-group-ingress --group-id <security-group-id> --protocol tcp --port 10250 --cidr 0.0.0.0/0 --region {region} --profile {profile}")
    run_command(f"aws ec2 authorize-security-group-ingress --group-id <security-group-id> --protocol tcp --port 443 --cidr 0.0.0.0/0 --region {region} --profile {profile}")
    run_command(f"aws ec2 authorize-security-group-ingress --group-id <security-group-id> --protocol tcp --port 4000 --cidr 0.0.0.0/0 --region {region} --profile {profile}")


@app.command(name="creds")
def get_credentials(name: str = typer.Argument(config.cluster_name),
                    region: str = typer.Argument(config.region),
                    profile: str = typer.Argument(config.profile)) -> None:
    """Retrieve credentials for kubectl"""
    print(f"Retrieving credentials for cluster: {name}...")
    run_command(f"aws eks update-kubeconfig --name {name} --region {region} --profile {profile}")


@app.command(name="proj")
def check_current_project(profile: str = typer.Argument(config.profile)) -> None:
    """Check the current AWS profile"""
    print("Checking current AWS profile...")
    run_command(f"aws configure list --profile {profile}")


@app.command(name="set-proj")
def set_profile(profile: str = typer.Argument(config.profile)) -> None:
    """Set the AWS profile"""
    print(f"Setting AWS profile to: {profile}...")
    run_command(f"aws configure set profile {profile}")


@app.command(name="perm")
def check_user_permissions(profile: str = typer.Argument(config.profile)) -> None:
    """Check the user's permissions for the specified profile"""
    print(f"Checking user permissions for profile: {profile}...")
    run_command(f"aws iam get-user --profile {profile}")


@app.command(name="login")
def login() -> None:
    """Login to AWS"""
    print("Logging into AWS...")
    run_command("aws configure")


@app.command(name="net")
def check_network_connectivity() -> None:
    """Check network connectivity to AWS services"""
    print("Checking network connectivity to AWS services...")
    run_command("ping amazonaws.com")


@app.command(name="quota")
def check_service_quotas(profile: str = typer.Argument(config.profile)) -> None:
    """Check the service quotas for the current profile"""
    print("Checking service quotas for the current profile...")
    run_command(f"aws service-quotas list-service-quotas --profile {profile}")


@app.command(name="retry")
def retry_enable_service(profile: str = typer.Argument(config.profile)) -> None:
    """Retry enabling the EKS service"""
    print("Retrying enabling the EKS service...")
    run_command(f"aws eks list-clusters --profile {profile}")


@app.command(name="list")
def list_profiles() -> None:
    """List available AWS profiles"""
    print("Listing available AWS profiles...")
    run_command("aws configure list-profiles")


@app.command(name="set")
def set_profile_interactive() -> None:
    """Set the AWS profile using an interactive menu"""
    print("Fetching list of available AWS profiles...")
    result = subprocess.run(
        "aws configure list-profiles",
        shell=True,
        check=True,
        capture_output=True,
        text=True
    )

    profiles = result.stdout.strip().split("\n")

    if not profiles:
        print("No profiles found.")
        return

    questions = [
        inquirer.List(
            'profile',
            message="Select an AWS profile",
            choices=profiles
        )
    ]

    answers = inquirer.prompt(questions)
    selected_profile = answers['profile']

    print(f"Setting AWS profile to: {selected_profile}...")
    run_command(f"aws configure set profile {selected_profile}")
