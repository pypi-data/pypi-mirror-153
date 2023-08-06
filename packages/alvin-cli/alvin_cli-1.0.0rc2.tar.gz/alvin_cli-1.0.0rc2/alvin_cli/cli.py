import logging
import os.path

import typer

from alvin_cli import config_management
from alvin_cli import entity
from alvin_cli import impact_analysis
from alvin_cli import manual_lineage
from alvin_cli.config.loader import USER_CONFIG_DIR
from alvin_cli.config.loader import create_cfg_file
from alvin_cli.platforms import platform
from alvin_cli.utils import default_api
from alvin_cli.utils.helper_functions import console
from alvin_cli.utils.helper_functions import typer_secho_raise

app = typer.Typer(add_completion=False)
app.add_typer(platform.app, name="platform", help="Connect platforms with Alvin")
app.add_typer(
    entity.app, name="entity", help="Get entity details along with lineage and usage"
)

app.add_typer(impact_analysis.app, name="impact-analysis", help="Get Impact Analysis")

app.add_typer(config_management.app, name="config", help="Manage Alvin config")
app.add_typer(
    manual_lineage.app, name="manual-lineage", help="Add and Delete Manual Lineage Data"
)


def __setup_logging() -> None:
    logging.basicConfig(level=logging.INFO)


@app.command()
def setup() -> None:
    """Set up configuration file and input your alvin credentials"""
    directory = USER_CONFIG_DIR
    if not os.path.isdir(directory):
        os.makedirs(directory)

    is_file_present = create_cfg_file(directory)

    if is_file_present:
        typer_secho_raise(
            f"File in {directory}/alvin.cfg already exists. Fill your credentials to start using other commands!",
            "CYAN",
        )

    else:

        typer_secho_raise(
            f"Created file 'alvin.cfg'. Set up your credentials in {directory}/alvin.cfg to start using other commands!",
            "GREEN",
        )


@app.command()
def current_user() -> None:
    """Get current authenticated user details"""
    user = default_api.get_user_info_api_v1_me_get()
    console.print(f'[bold cyan]User ID: {user["id"]}[/bold cyan]')
    if user["first_name"]:
        console.print(f'[bold yellow]User Name: {user["first_name"]}[/bold yellow]')


def run() -> None:
    app()


if __name__ == "__main__":
    run()  # pragma: no cover
