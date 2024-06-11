import os
import subprocess
from importlib import import_module

import dspy
import openai
from rich import print

from dspyfun.utils.path_tools import subcommand_dir

from rich.markdown import Markdown


def run_command(command: str) -> None:
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Command '{command}' failed with exit code {e.returncode}")
        diagnose_error(str(e))
        # Kill the script if the command fails
        raise SystemExit


class CLIErrorDiagnosis(dspy.Signature):
    """
    Diagnose CLI errors and provide recommended CLI commands from a Google Cloud Systems Architect's perspective.
    """
    error_message = dspy.InputField(desc="The error message from the failed CLI command.")

    diagnosis = dspy.OutputField(desc="Detailed diagnosis of the error.")
    recommended_commands = dspy.OutputField(desc="List of recommended CLI commands to resolve or further investigate the error.")


def diagnose_error(error_message: str) -> str:
    from dspyfun.utils.dspy_tools import init_dspy
    init_dspy(model="gpt-4o", max_tokens=2000)
    print(f"Diagnosing error with DSPy...")
    response = dspy.ChainOfThought(CLIErrorDiagnosis).forward(error_message=error_message)
    md = Markdown(response.diagnosis)
    print(md)
    md = Markdown(response.recommended_commands)
    print(md)
    # return f"Diagnosis: {response.diagnosis}\nRecommendations: {response.recommended_commands}"


def load_commands():
    cmd_dir = subcommand_dir()

    for filename in os.listdir(cmd_dir):
        if filename.endswith("_cmd.py"):
            module_name = f'{__name__.split(".")[0]}.subcommands.{filename[:-3]}'
            module = import_module(module_name)
            if hasattr(module, "app"):
                from dspyfun.cli import app
                app.add_typer(module.app, name=filename[:-7], help=module.__doc__)
