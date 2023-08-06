import configparser
import logging
import os

import typer

from alvin_cli.config.loader import GLOBAL
from alvin_cli.config.loader import USER_CONFIG
from alvin_cli.config.loader import set_current_config_context
from alvin_cli.config.loader import set_key_value_in_cfg
from alvin_cli.schemas.models import OutputFormat
from alvin_cli.utils.common_arguments import BRIGHT_GREEN_COLOR_TYPER
from alvin_cli.utils.common_arguments import BRIGHT_YELLOW_COLOR_TYPER
from alvin_cli.utils.common_arguments import current_active_profile
from alvin_cli.utils.helper_functions import print_output_format
from alvin_cli.utils.helper_functions import typer_secho_raise

app = typer.Typer(add_completion=False)

ACTIVE_CONTEXT = current_active_profile


def __setup_logging() -> None:
    logging.basicConfig(level=logging.INFO)


@app.command("activate")
def set_current_context(
    section: str = typer.Argument(
        ...,
        help=typer.style("Which config section to use?", fg=BRIGHT_GREEN_COLOR_TYPER),
    )
) -> None:
    """Set current active context in configuration"""
    section = section.upper()
    set_context_exists = set_current_config_context(section)
    if set_context_exists:
        typer_secho_raise(f"Updated current active section to {[section]}", "GREEN")
    else:
        typer_secho_raise(
            f"{[section]} doesnt' exist, create the section first using `alvin config set` command",
            "MAGENTA",
        )


@app.command("list-current")
def current_context() -> None:
    """List config values set under current active section"""
    config_read = configparser.ConfigParser()

    if not os.path.isfile(USER_CONFIG):
        typer_secho_raise("Config not found", "CYAN")

    config_read.read(USER_CONFIG)

    config_data_per_section_in_list = []

    # get name of section from active project
    section = config_read[GLOBAL]["active_profile"]

    typer_secho_raise(f"Your active configuration is {[section]}", "MAGENTA")

    config_data_per_section_in_dict = {}
    # iterate through key and value pairs of current project section and print them out
    for key, value in config_read[section].items():
        config_data_per_section_in_dict.update({key: value})
    config_data_per_section_in_list.append(config_data_per_section_in_dict)

    print_output_format(
        data=config_data_per_section_in_list,
        table_title="",
        output=OutputFormat.yaml,
        save_to_file=False,
        file_name="",
    )


@app.command(name="list-all")
def config_list() -> None:
    """List all the sections and corresponding values in configuration file"""
    config_read = configparser.ConfigParser()

    if not os.path.isfile(USER_CONFIG):
        typer_secho_raise("Config not found", "CYAN")

    config_read.read(USER_CONFIG)

    config_data_per_section_in_list = []

    for section in config_read.sections():
        config_data_per_section_in_dict = {}
        config_data_per_section_in_dict.update({"section": section})
        for key, value in config_read[section].items():
            config_data_per_section_in_dict.update({key: value})
        config_data_per_section_in_list.append(config_data_per_section_in_dict)

    print_output_format(
        data=config_data_per_section_in_list,
        table_title="",
        output=OutputFormat.yaml,
        save_to_file=False,
        file_name="",
    )


@app.command("set")
def add_and_update_section(
    section: str = typer.Option(
        ACTIVE_CONTEXT,
        help=typer.style(
            "Which section to update? By default current activated section is updated",
            fg=BRIGHT_YELLOW_COLOR_TYPER,
        ),
    ),
    key: str = typer.Argument(
        ..., help=typer.style("Add or update a key", fg=BRIGHT_GREEN_COLOR_TYPER)
    ),
    value: str = typer.Argument(
        ..., help=typer.style("Add or update a value", fg=BRIGHT_GREEN_COLOR_TYPER)
    ),
) -> None:
    """Set keys and values to context in configuration. Also creates inputted section if it doesn't exist"""
    if set_key_value_in_cfg(section, key, value):
        typer_secho_raise(
            f"Updated {section.upper()}/{key} to be {value}", color="GREEN"
        )

    else:
        typer_secho_raise(
            "Something went wrong, run the command with root privileges or check the input format",
            "RED",
        )
