import configparser
import os.path

import typer

from alvin_cli.config.loader import CORE_SECTION
from alvin_cli.config.loader import USER_CONFIG
from alvin_cli.config.loader import current_active_project_name
from alvin_cli.schemas.models import OutputFormat

CHECK_ENTITY_VALID_TEXT = "Check the entity type is valid!"
COLUMN_NOT_RENDERING_TEXT = (
    "If the columns are not fully rendering, try out '-o yaml' format"
)
ARGUMENTS_INVALID_TEXT = "Check all the arguments are valid"
BRIGHT_GREEN_COLOR_TYPER = typer.colors.BRIGHT_GREEN
BRIGHT_CYAN_COLOR_TYPER = typer.colors.BRIGHT_CYAN
BRIGHT_YELLOW_COLOR_TYPER = typer.colors.YELLOW

current_config_items = {}
# by default the active profile is [ALVIN]
current_active_profile = CORE_SECTION
if os.path.exists(USER_CONFIG):
    # this config would have all the values from read
    config_read = configparser.ConfigParser()
    config_read.read(USER_CONFIG)
    # current active project
    current_active_profile = current_active_project_name(config_read)
    for k, v in config_read[current_active_profile].items():
        if current_active_profile:
            current_config_items.update({k: v})


CONFIG_FILE_PATH = (
    current_config_items["config_file_path"]
    if "config_file_path" in current_config_items
    else typer.Option(
        "",
        "--config-file-path",
        "-cfp",
        help=typer.style("Config file path", fg=BRIGHT_CYAN_COLOR_TYPER, bold=True),
    )
)

NAME = (
    current_config_items["name"]
    if "name" in current_config_items
    else typer.Option(
        ...,
        "--name",
        "-n",
        help=typer.style("Name", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True),
    )
)


DISPLAY_NAME = typer.Option(
    ...,
    "--display-name",
    "-dn",
    help=typer.style("Display Name", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True),
)

PASSWORD = typer.Option(
    ...,
    "--password",
    "-pass",
    help=typer.style("Password", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True),
)


HOST = typer.Option(
    ...,
    "--host",
    "-h",
    help=typer.style("Host", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True),
)


PORT = typer.Option(
    ...,
    "--port",
    "-p",
    help=typer.style("Port", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True),
)

USERNAME = typer.Option(
    ...,
    "--username",
    "-u",
    help=typer.style("username", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True),
)


BASE_URL = typer.Option(
    ...,
    "--base-url",
    "-burl",
    help=typer.style("Base URL", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True),
)


ONLY_VALIDATE = (
    current_config_items["only_validate"]
    if "only_validate" in current_config_items
    else typer.Option(
        False,
        help=typer.style("Test the connection", fg=BRIGHT_CYAN_COLOR_TYPER, bold=True),
    )
)
DATABASE = typer.Option(
    ...,
    "--database",
    "-d",
    help=typer.style("Database", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True),
)


OUTPUT = (
    current_config_items["output"]
    if "output" in current_config_items
    else typer.Option(
        OutputFormat.yaml,
        "--output",
        "-o",
        help=typer.style(
            "Format to receive output in, default is yaml",
            fg=BRIGHT_YELLOW_COLOR_TYPER,
        ),
    )
)

SAVE_TO_FILE = (
    current_config_items["save_to_file"]
    if "save_to_file" in current_config_items
    else typer.Option(
        False, help=typer.style("Save data to a file?", fg=BRIGHT_YELLOW_COLOR_TYPER)
    )
)

FILE_NAME = typer.Option(
    "",
    "--file-name",
    "-fn",
    help=typer.style(
        "File Name if file save selected. By default it's the command name",
        fg=BRIGHT_YELLOW_COLOR_TYPER,
    ),
)

PLATFORM_ID = (
    current_config_items["platform_id"]
    if "platform_id" in current_config_items
    else typer.Option(
        ...,
        "--platform-id",
        "-pid",
        help=typer.style("Platform ID", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True),
    )
)

FROM_ENTITY_PLATFORM_ID = (
    current_config_items["from_entity_platform_id"]
    if "from_entity_platform_id" in current_config_items
    else typer.Option(
        ...,
        "--from-entity-platform-id",
        "-from-pid",
        help=typer.style("From Platform ID", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True),
    )
)

TO_ENTITY_PLATFORM_ID = (
    current_config_items["to_entity_platform_id"]
    if "to_entity_platform_id" in current_config_items
    else typer.Option(
        ...,
        "--to-entity-platform-id",
        "-to-pid",
        help=typer.style("To Platform ID", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True),
    )
)

ENTITY_ID = (
    current_config_items["entity_id"]
    if "entity_id" in current_config_items
    else typer.Option(
        ...,
        "--entity-id",
        "-eid",
        help=typer.style("Entity ID", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True),
    )
)

FROM_ENTITY_ID = (
    current_config_items["from_entity_id"]
    if "from_entity_id" in current_config_items
    else typer.Option(
        ...,
        "--from-entity-id",
        "-from-eid",
        help=typer.style("From Entity ID", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True),
    )
)

TO_ENTITY_ID = (
    current_config_items["to_entity_id"]
    if "to_entity_id" in current_config_items
    else typer.Option(
        ...,
        "--to-entity-id",
        "-to-eid",
        help=typer.style("To Entity ID", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True),
    )
)

ENTITY_TYPE = (
    current_config_items["entity_type"]
    if "entity_type" in current_config_items
    else typer.Option(
        ...,
        "--entity-type",
        "-etype",
        help=typer.style("Entity Type", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True),
    )
)

FROM_ENTITY_TYPE = (
    current_config_items["from_entity_type"]
    if "from_entity_type" in current_config_items
    else typer.Option(
        ...,
        "--from-entity-type",
        "-from-etype",
        help=typer.style("From Entity Type", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True),
    )
)

TO_ENTITY_TYPE = (
    current_config_items["to_entity_type"]
    if "to_entity_type" in current_config_items
    else typer.Option(
        ...,
        "--to-entity-type",
        "-to-etype",
        help=typer.style("To Entity Type", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True),
    )
)

LIMIT = typer.Option(
    10,
    "--limit",
    "-l",
    help=typer.style("Limit, 10 by default", fg=BRIGHT_YELLOW_COLOR_TYPER),
)

OFFSET = typer.Option(
    0,
    "--offset",
    "-off",
    help=typer.style("Offset, 0 by default", fg=BRIGHT_YELLOW_COLOR_TYPER),
)

RULE_TYPE = typer.Option(
    ...,
    "--rule_type",
    "-rty",
    help=typer.style("Rule Type", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True),
)

DOMAIN = (
    current_config_items["domain"]
    if "domain" in current_config_items
    else typer.Option(
        ...,
        "--domain",
        "-d",
        help=typer.style(
            "Domain (Case Sensitive)", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True
        ),
    )
)

RULE_TEXT = typer.Option(
    ...,
    "--rule_text",
    "-rte",
    help=typer.style("Rule Text", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True),
)

TAG_NAME = typer.Option(
    ...,
    "--tag_name",
    "-tn",
    help=typer.style(
        "What Tag to apply? (Case Sensitive)", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True
    ),
)

TAG_TYPE = (
    current_config_items["tag_type"]
    if "tag_type" in current_config_items
    else typer.Option(
        ...,
        "--tag_type",
        "-tt",
        help=typer.style(
            "Tag Type: Business_Term or Tag", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True
        ),
    )
)

IGNORED_DATABASES = (
    current_config_items["ignored_databases"]
    if "ignored_databases" in current_config_items
    else typer.Option(
        "",
        "--ignored-databases",
        "-igdb",
        help=typer.style(
            "Ignored databases values as comma separated string",
            fg=BRIGHT_YELLOW_COLOR_TYPER,
        ),
    )
)

IGNORED_SCHEMAS = (
    current_config_items["ignored_schemas"]
    if "ignored_schemas" in current_config_items
    else typer.Option(
        "",
        "--ignored-schemas",
        "-igschemas",
        help=typer.style(
            "Ignored schemas values as comma separated string",
            fg=BRIGHT_YELLOW_COLOR_TYPER,
        ),
    )
)

IGNORED_QUERY_TYPES = (
    current_config_items["ignored_query_types"]
    if "ignored_query_types" in current_config_items
    else typer.Option(
        "",
        "--ignored-query-types",
        "-igqtypes",
        help=typer.style(
            "Ignored query types values as comma separated string",
            fg=BRIGHT_YELLOW_COLOR_TYPER,
        ),
    )
)


IGNORED_USERS = (
    current_config_items["ignored_users"]
    if "ignored_users" in current_config_items
    else typer.Option(
        "",
        "--ignored-users",
        "-igusers",
        help=typer.style(
            "Ignored users values as comma separated string",
            fg=BRIGHT_YELLOW_COLOR_TYPER,
        ),
    )
)

IGNORED_QUERY_STATUSES = (
    current_config_items["ignored_query_statuses"]
    if "ignored_query_statuses" in current_config_items
    else typer.Option(
        "",
        "--ignored-query-statuses",
        "-igqstatuses",
        help=typer.style(
            "Ignored query statuses values as comma separated string",
            fg=BRIGHT_YELLOW_COLOR_TYPER,
        ),
    )
)

IGNORED_PROJECTS = (
    current_config_items["ignored_projects"]
    if "ignored_projects" in current_config_items
    else typer.Option(
        "",
        "--ignored-projects",
        "-igprojects",
        help=typer.style(
            "Ignored projects values as comma separated string",
            fg=BRIGHT_YELLOW_COLOR_TYPER,
        ),
    )
)
