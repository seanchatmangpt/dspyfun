import subprocess

import pytest
from typer.testing import CliRunner
from dspyfun.cli import app
from tests.mocks.subprocess_mock import SubprocessMock

# Initialize the CLI runner
runner = CliRunner()

# Initialize the subprocess mock
subprocess_mock = SubprocessMock()


# Patch subprocess.run with the mock
@pytest.fixture(autouse=True)
def patch_subprocess_run(monkeypatch):
    monkeypatch.setattr(subprocess, "run", subprocess_mock.run)
    yield
    subprocess_mock.run.reset_mock()  # Reset mock after each test


def test_install_kubectl():
    result = runner.invoke(app, ["k8", "install"])
    assert result.exit_code == 0
    subprocess_mock.run.assert_called_once_with("gcloud components install kubectl", check=True, shell=True)


def test_install_gcloud_sdk():
    result = runner.invoke(app, ["gc", "install"])
    assert result.exit_code == 0
    subprocess_mock.run.assert_any_call("curl https://sdk.cloud.google.com | bash", check=True, shell=True)
    subprocess_mock.run.assert_any_call("exec -l $SHELL", check=True, shell=True)
    subprocess_mock.run.assert_any_call("gcloud init", check=True, shell=True)


def test_create_cluster():
    result = runner.invoke(app, ["gc", "create", "test-cluster", "us-central1", "test-project"])
    assert result.exit_code == 0
    subprocess_mock.run.assert_any_call("gcloud services enable container.googleapis.com", check=True, shell=True)
    subprocess_mock.run.assert_any_call(
        "gcloud container clusters create test-cluster --zone us-central1 --project test-project", check=True,
        shell=True)


def test_setup_firewall(monkeypatch):
    # Mock subprocess.check_output to return a fake firewall rule name
    monkeypatch.setattr(subprocess, "check_output", lambda x, shell: b"fake-firewall-rule")

    result = runner.invoke(app, ["gc", "firewall", "test-cluster"])
    assert result.exit_code == 0
    subprocess_mock.run.assert_called_once_with(
        "gcloud compute firewall-rules update fake-firewall-rule --allow tcp:10250,tcp:443,tcp:4000", check=True,
        shell=True)


def test_get_credentials():
    result = runner.invoke(app, ["gc", "creds", "test-cluster", "us-central1", "test-project"])
    assert result.exit_code == 0
    subprocess_mock.run.assert_called_once_with(
        "gcloud container clusters get-credentials test-cluster --zone us-central1 --project test-project", check=True,
        shell=True)


def test_install_helm():
    result = runner.invoke(app, ["helm", "install"])
    assert result.exit_code == 0
    subprocess_mock.run.assert_called_once_with(
        "curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash", check=True, shell=True)


def test_fix_dashboard():
    result = runner.invoke(app, ["k8", "fix"])
    assert result.exit_code == 0
    subprocess_mock.run.assert_called_once_with(
        "kubectl create clusterrolebinding kubernetes-dashboard -n kube-system --clusterrole=cluster-admin --serviceaccount=kube-system:kubernetes-dashboard",
        check=True, shell=True)
