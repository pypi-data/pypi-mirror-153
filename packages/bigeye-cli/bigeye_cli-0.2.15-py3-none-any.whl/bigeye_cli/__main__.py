import json
from dataclasses import asdict
from typing import Optional

import smart_open
import typer

from bigeye_cli import DEFAULT_CRED_FILE
from bigeye_sdk.functions.file_functs import create_subdir_if_not_exists

from bigeye_sdk.model.api_credentials import BasicAuthRequestLibApiConf

import bigeye_cli.__version__ as bigeye_cli_version
import bigeye_sdk.__version__ as bigeye_sdk_version
from bigeye_cli.deltas import deltas_commands
from bigeye_cli.functions import print_readme
from bigeye_cli.workspace import workspace_commands
from bigeye_sdk.log import get_logger

from bigeye_cli.catalog import catalog_commands
from bigeye_cli.sla import sla_commands
from bigeye_cli.metric import metric_commands
from bigeye_cli.issues import issue_commands

# create logger
log = get_logger(__file__)

app = typer.Typer(no_args_is_help=True, help="""Bigeye CLI""")
app.add_typer(sla_commands.app, name='sla')
app.add_typer(catalog_commands.app, name='catalog')
app.add_typer(metric_commands.app, name='metric')
app.add_typer(deltas_commands.app, name='deltas')
app.add_typer(workspace_commands.app, name='workspace')
app.add_typer(issue_commands.app, name='issues')


@app.callback(invoke_without_command=True)
def options_callback(
        version: Optional[bool] = typer.Option(
            None, "--version", help="Bigeye CLI and SDK Versions"),
        readme: Optional[bool] = typer.Option(
            None, "--readme", help="Prints Readme.")
):
    if version:
        typer.echo(f'Bigeye CLI Version: {bigeye_cli_version.version}\n'
                   f'Bigeye SDK Version: {bigeye_sdk_version.version}')
        raise typer.Exit()
    elif readme:
        print_readme()


@app.command()
def credential():
    """Create a default credential for Bigeye CLI."""
    from rich.prompt import Prompt
    base_url = Prompt.ask("Enter the Bigeye URL", default="https://app.bigeye.com")
    username = Prompt.ask("Enter the username")
    password = Prompt.ask("Enter the password", password=True)

    cred = BasicAuthRequestLibApiConf(base_url=base_url, user=username, password=password)
    create_subdir_if_not_exists(path=DEFAULT_CRED_FILE, includes_file=True)

    with smart_open.smart_open(DEFAULT_CRED_FILE, 'wb') as fout:
        s = json.dumps(asdict(cred))
        fout.write(s.encode())


if __name__ == '__main__':
    app()
