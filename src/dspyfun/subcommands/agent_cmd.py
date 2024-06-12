"""agent"""
import typer


app = typer.Typer()


@app.command(name="code")
def agent_code():
    """code"""
    typer.echo("Running code subcommand.")
    # coder =