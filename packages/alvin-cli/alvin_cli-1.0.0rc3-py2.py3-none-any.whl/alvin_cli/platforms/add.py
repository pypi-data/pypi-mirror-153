import json
from pathlib import Path

import typer
from alvin_api_client.model.big_query_account_details import BigQueryAccountDetails
from alvin_api_client.model.big_query_additional_config import BigQueryAdditionalConfig
from alvin_api_client.model.data_platform_big_query_create import (
    DataPlatformBigQueryCreate,
)
from alvin_api_client.model.data_platform_looker_create import DataPlatformLookerCreate
from alvin_api_client.model.data_platform_mode_create import DataPlatformModeCreate
from alvin_api_client.model.data_platform_my_sql_create import DataPlatformMySQLCreate
from alvin_api_client.model.data_platform_postgres_create import (
    DataPlatformPostgresCreate,
)
from alvin_api_client.model.data_platform_power_bi_create import (
    DataPlatformPowerBICreate,
)
from alvin_api_client.model.data_platform_redshift_create import (
    DataPlatformRedshiftCreate,
)
from alvin_api_client.model.data_platform_snowflake_create import (
    DataPlatformSnowflakeCreate,
)
from alvin_api_client.model.data_platform_tableau_create import (
    DataPlatformTableauCreate,
)
from alvin_api_client.model.hive_account_details import HiveAccountDetails
from alvin_api_client.model.hive_additional_config import HiveAdditionalConfig
from alvin_api_client.model.looker_additional_config import LookerAdditionalConfig
from alvin_api_client.model.looker_credentials import LookerCredentials
from alvin_api_client.model.mode_additional_config import ModeAdditionalConfig
from alvin_api_client.model.mode_credentials import ModeCredentials
from alvin_api_client.model.my_sql_account_details import MySQLAccountDetails
from alvin_api_client.model.my_sql_additional_config import MySQLAdditionalConfig
from alvin_api_client.model.postgres_account_details import PostgresAccountDetails
from alvin_api_client.model.postgres_additional_config import PostgresAdditionalConfig
from alvin_api_client.model.power_bi_additional_config import PowerBIAdditionalConfig
from alvin_api_client.model.power_bi_credentials import PowerBICredentials
from alvin_api_client.model.redshift_account_details import RedshiftAccountDetails
from alvin_api_client.model.redshift_additional_config import RedshiftAdditionalConfig
from alvin_api_client.model.snowflake_account_details import SnowflakeAccountDetails
from alvin_api_client.model.snowflake_additional_config import SnowflakeAdditionalConfig
from alvin_api_client.model.tableau_additional_config import TableauAdditionalConfig
from alvin_api_client.model.tableau_credentials import TableauCredentials

from alvin_cli.utils.api_client import default_api
from alvin_cli.utils.common_arguments import BASE_URL
from alvin_cli.utils.common_arguments import BRIGHT_GREEN_COLOR_TYPER
from alvin_cli.utils.common_arguments import BRIGHT_YELLOW_COLOR_TYPER
from alvin_cli.utils.common_arguments import CONFIG_FILE_PATH
from alvin_cli.utils.common_arguments import DATABASE
from alvin_cli.utils.common_arguments import DISPLAY_NAME
from alvin_cli.utils.common_arguments import HOST
from alvin_cli.utils.common_arguments import IGNORED_DATABASES
from alvin_cli.utils.common_arguments import IGNORED_PROJECTS
from alvin_cli.utils.common_arguments import IGNORED_QUERY_STATUSES
from alvin_cli.utils.common_arguments import IGNORED_QUERY_TYPES
from alvin_cli.utils.common_arguments import IGNORED_SCHEMAS
from alvin_cli.utils.common_arguments import IGNORED_USERS
from alvin_cli.utils.common_arguments import NAME
from alvin_cli.utils.common_arguments import ONLY_VALIDATE
from alvin_cli.utils.common_arguments import PASSWORD
from alvin_cli.utils.common_arguments import PORT
from alvin_cli.utils.common_arguments import USERNAME
from alvin_cli.utils.helper_functions import extract_dict
from alvin_cli.utils.helper_functions import format_response_data
from alvin_cli.utils.helper_functions import handle_print_exception
from alvin_cli.utils.helper_functions import print_output_format
from alvin_cli.utils.helper_functions import read_config_from_json
from alvin_cli.utils.helper_functions import typer_progress_bar
from alvin_cli.utils.helper_functions import typer_secho_raise

app = typer.Typer(help="Connect Data Platforms with Alvin")

fields_to_print = [
    "id",
    "name",
    "platform_type",
    "created",
    "last_updated",
    "is_syncing",
    "additional_config",
]

testing_text = "TESTING THE CONNECTION......"
test_successful_text = "TEST SUCCESSFUL"
connection_failed_text = "CONNECTION FAILED"
creating_connection_text = "CREATING NEW CONNECTION....."
connection_created_text = "CONNECTION SUCCESSFULLY CREATED"


@app.command()
def bigquery(
    name: str = NAME,
    display_name: str = DISPLAY_NAME,
    service_account_json: Path = CONFIG_FILE_PATH,
    ignored_databases: str = IGNORED_DATABASES,
    ignored_schemas: str = IGNORED_SCHEMAS,
    ignored_query_types: str = IGNORED_QUERY_TYPES,
    ignored_users: str = IGNORED_USERS,
    ignored_query_statuses: str = IGNORED_QUERY_STATUSES,
    only_validate: bool = ONLY_VALIDATE,
) -> None:
    """Add bigquery platform"""

    credentials = json.dumps(read_config_from_json(service_account_json))
    request_in = DataPlatformBigQueryCreate(
        name=name,
        display_name=display_name,
        credentials=BigQueryAccountDetails(credentials),
        additional_config=BigQueryAdditionalConfig(
            ignored_databases=ignored_databases.split(","),
            ignored_schemas=ignored_schemas.split(","),
            ignored_query_types=ignored_query_types.split(","),
            ignored_users=ignored_users.split(","),
            ignored_query_statuses=ignored_query_statuses.split(","),
        ),
    )

    try:
        create_response = (
            default_api.create_bigquery_platform_api_v1_platforms_bigquery_post(
                request_in
            )
        )

        if only_validate:
            typer_secho_raise(testing_text, "GREEN")
            typer_progress_bar()
            default_api.test_bigquery_platform_api_v1_platforms_bigquery_test_post(
                request_in
            )

            typer_secho_raise(test_successful_text, "GREEN")

    except Exception as e:

        typer_secho_raise(connection_failed_text, "RED")

        exception = e.__str__()

        handle_print_exception(extract_dict(exception), exception[:5])

        return

    typer_secho_raise(creating_connection_text, "CYAN")
    typer_progress_bar()
    structured_data = format_response_data(fields_to_print, [create_response])

    print_output_format(structured_data, f"{name} platform", "yaml", False, "")

    typer_secho_raise(connection_created_text, "MAGENTA")


@app.command()
def looker(
    name: str = NAME,
    display_name: str = DISPLAY_NAME,
    client_id: str = typer.Option(
        ..., help=typer.style("Client Id", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True)
    ),
    client_secret: str = typer.Option(
        ...,
        help=typer.style(
            "Client Secret/Password", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True
        ),
    ),
    base_url: str = BASE_URL,
    ignored_projects: str = IGNORED_PROJECTS,
    ignored_models: str = typer.Option(
        "",
        help=typer.style(
            "Ignored models values as comma separated string",
            fg=BRIGHT_YELLOW_COLOR_TYPER,
        ),
    ),
    ignored_folders: str = typer.Option(
        "",
        help=typer.style(
            "Ignored folders values as comma separated string",
            fg=BRIGHT_YELLOW_COLOR_TYPER,
        ),
    ),
    data_source_platform_id: str = typer.Option(
        "", help=typer.style("Data Source Platform ID", fg=BRIGHT_YELLOW_COLOR_TYPER)
    ),
    only_validate: bool = ONLY_VALIDATE,
) -> None:
    """Add looker platform"""

    request_in = DataPlatformLookerCreate(
        name=name,
        display_name=display_name,
        credentials=LookerCredentials(
            base_url=base_url, client_id=client_id, client_secret=client_secret
        ),
        additional_config=LookerAdditionalConfig(
            ignored_projects=ignored_projects.split(","),
            ignored_models=ignored_models.split(","),
            ignored_folders=ignored_folders.split(","),
            data_source_platform_id=data_source_platform_id,
        ),
    )

    try:
        create_response = (
            default_api.create_looker_platform_api_v1_platforms_looker_post(request_in)
        )

        if only_validate:
            typer_secho_raise(testing_text, "GREEN")
            typer_progress_bar()
            default_api.test_looker_platform_api_v1_platforms_looker_test_post(
                request_in
            )

            typer_secho_raise(test_successful_text, "GREEN")

    except Exception as e:
        typer_secho_raise(connection_failed_text, "RED")
        exception = e.__str__()
        handle_print_exception(extract_dict(exception), exception[:5])
        return

    typer_secho_raise(creating_connection_text, "CYAN")
    typer_progress_bar()
    structured_data = format_response_data(fields_to_print, [create_response])
    print_output_format(structured_data, f"{name} platform", "yaml", False, "")
    typer_secho_raise(connection_created_text, "MAGENTA")


@app.command()
def mode(
    name: str = NAME,
    display_name: str = DISPLAY_NAME,
    access_token: str = typer.Option(
        ..., help=typer.style("Access Token", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True)
    ),
    password: str = PASSWORD,
    workspace_username: str = typer.Option(
        "",
        help=typer.style("Workspace Username", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True),
    ),
    ignored_spaces_tokens: str = typer.Option(
        "",
        help=typer.style(
            "Ignored space tokens values as comma separated string",
            fg=BRIGHT_YELLOW_COLOR_TYPER,
        ),
    ),
    ignore_private_spaces: bool = typer.Option(
        False,
        help=typer.style("Ignore private spaces", fg=BRIGHT_YELLOW_COLOR_TYPER),
    ),
    only_validate: bool = ONLY_VALIDATE,
) -> None:
    """Add Mode platform"""

    request_in = DataPlatformModeCreate(
        name=name,
        display_name=display_name,
        credentials=ModeCredentials(access_token=access_token, password=password),
        additional_config=ModeAdditionalConfig(
            workspace_username=workspace_username,
            ignored_spaces_tokens=ignored_spaces_tokens.split(","),
            ignore_private_spaces=ignore_private_spaces,
        ),
    )

    try:
        create_response = default_api.create_mode_platform_api_v1_platforms_mode_post(
            request_in
        )

        if only_validate:
            typer_secho_raise(testing_text, "GREEN")
            typer_progress_bar()
            default_api.test_mode_platform_api_v1_platforms_mode_test_post(request_in)

            typer_secho_raise(test_successful_text, "GREEN")

    except Exception as e:

        typer_secho_raise(connection_failed_text, "RED")

        exception = e.__str__()

        handle_print_exception(extract_dict(exception), exception[:5])

        return

    typer_secho_raise(creating_connection_text, "CYAN")
    typer_progress_bar()
    structured_data = format_response_data(fields_to_print, [create_response])

    print_output_format(structured_data, f"{name} platform", "yaml", False, "")

    typer_secho_raise(connection_created_text, "MAGENTA")


@app.command()
def redshift(
    name: str = NAME,
    display_name: str = DISPLAY_NAME,
    host: str = HOST,
    port: int = PORT,
    username: str = USERNAME,
    password: str = PASSWORD,
    database: str = DATABASE,
    ignored_databases: str = IGNORED_DATABASES,
    ignored_schemas: str = IGNORED_SCHEMAS,
    ignored_query_types: str = IGNORED_QUERY_TYPES,
    ignored_users: str = IGNORED_USERS,
    ignored_query_statuses: str = IGNORED_QUERY_STATUSES,
    only_validate: bool = ONLY_VALIDATE,
) -> None:
    """Add Redshift platform"""

    request_in = DataPlatformRedshiftCreate(
        name=name,
        display_name=display_name,
        credentials=RedshiftAccountDetails(
            host=host,
            port=port,
            username=username,
            password=password,
            database=database,
        ),
        additional_config=RedshiftAdditionalConfig(
            ignored_databases=ignored_databases.split(","),
            ignored_schemas=ignored_schemas.split(","),
            ignored_query_types=ignored_query_types.split(","),
            ignored_users=ignored_users.split(","),
            ignored_query_statuses=ignored_query_statuses.split(","),
        ),
    )

    try:
        create_response = (
            default_api.create_redshift_platform_api_v1_platforms_redshift_post(
                request_in
            )
        )

        if only_validate:
            typer_secho_raise(testing_text, "GREEN")
            typer_progress_bar()
            default_api.test_redshift_platform_api_v1_platforms_redshift_test_post(
                request_in
            )

            typer_secho_raise(test_successful_text, "GREEN")

    except Exception as e:

        typer_secho_raise(connection_failed_text, "RED")

        exception = e.__str__()

        handle_print_exception(extract_dict(exception), exception[:5])

        return

    typer_secho_raise(creating_connection_text, "CYAN")
    typer_progress_bar()

    structured_data = format_response_data(fields_to_print, [create_response])

    print_output_format(structured_data, f"{name} platform", "yaml", False, "")

    typer_secho_raise(connection_created_text, "MAGENTA")


@app.command()
def snowflake(
    name: str = NAME,
    display_name: str = DISPLAY_NAME,
    account: str = typer.Option(
        ..., help=typer.style("Account", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True)
    ),
    username: str = USERNAME,
    password: str = PASSWORD,
    role: str = typer.Option(
        ..., help=typer.style("Role", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True)
    ),
    warehouse: str = typer.Option(
        ..., help=typer.style("Warehouse", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True)
    ),
    ignored_databases: str = IGNORED_DATABASES,
    ignored_schemas: str = IGNORED_SCHEMAS,
    ignored_query_types: str = IGNORED_QUERY_TYPES,
    ignored_users: str = IGNORED_USERS,
    ignored_query_statuses: str = IGNORED_QUERY_STATUSES,
    ignored_roles: str = typer.Option(
        "",
        help=typer.style(
            "Ignored roles values as comma separated string",
            fg=BRIGHT_YELLOW_COLOR_TYPER,
        ),
    ),
    only_validate: bool = ONLY_VALIDATE,
) -> None:
    """Add Snowflake platform"""

    request_in = DataPlatformSnowflakeCreate(
        name=name,
        display_name=display_name,
        credentials=SnowflakeAccountDetails(
            account=account,
            region=account.split(".")[-1],
            username=username,
            password=password,
            role=role,
            warehouse=warehouse,
        ),
        additional_config=SnowflakeAdditionalConfig(
            ignored_roles=ignored_roles.split(","),
            ignored_databases=ignored_databases.split(","),
            ignored_schemas=ignored_schemas.split(","),
            ignored_query_types=ignored_query_types.split(","),
            ignored_users=ignored_users.split(","),
            ignored_query_statuses=ignored_query_statuses.split(","),
        ),
    )
    try:
        create_response = (
            default_api.create_snowflake_platform_api_v1_platforms_snowflake_post(
                request_in
            )
        )

        if only_validate:
            typer_secho_raise(testing_text, "GREEN")
            typer_progress_bar()
            default_api.test_snowflake_platform_api_v1_platforms_snowflake_test_post(
                request_in
            )
            typer_secho_raise(test_successful_text, "GREEN")

    except Exception as e:

        typer_secho_raise(connection_failed_text, "RED")

        exception = e.__str__()

        handle_print_exception(extract_dict(exception), exception[:5])

        return

    typer_secho_raise(creating_connection_text, "CYAN")
    typer_progress_bar()
    structured_data = format_response_data(fields_to_print, [create_response])

    print_output_format(structured_data, f"{name} platform", "yaml", False, "")

    typer_secho_raise(connection_created_text, "MAGENTA")


@app.command()
def tableau(
    name: str = NAME,
    display_name: str = DISPLAY_NAME,
    base_url: str = BASE_URL,
    api_base_url: str = typer.Option(
        ..., help=typer.style("API Base URL", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True)
    ),
    api_version: str = typer.Option(
        ..., help=typer.style("API Version", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True)
    ),
    site_name: str = typer.Option(
        ..., help=typer.style("Site Name", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True)
    ),
    access_token_name: str = typer.Option(
        ...,
        help=typer.style("Access Token Name", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True),
    ),
    access_token_secret: str = typer.Option(
        ...,
        help=typer.style("Access Token Secret", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True),
    ),
    ignored_projects: str = IGNORED_PROJECTS,
    only_validate: bool = ONLY_VALIDATE,
) -> None:
    """Add Tableau platform"""
    request_in = DataPlatformTableauCreate(
        name=name,
        display_name=display_name,
        credentials=TableauCredentials(
            base_url=base_url,
            api_base_url=api_base_url,
            api_version=api_version,
            site_name=site_name,
            access_token_name=access_token_name,
            access_token_secret=access_token_secret,
        ),
        additional_config=TableauAdditionalConfig(
            ignored_projects=ignored_projects.split(",")
        ),
    )
    try:
        create_response = (
            default_api.create_tableau_platform_api_v1_platforms_tableau_post(
                request_in
            )
        )

        if only_validate:
            typer_secho_raise(testing_text, "GREEN")
            typer_progress_bar()
            default_api.test_tableau_platform_api_v1_platforms_tableau_test_post(
                request_in
            )

            typer_secho_raise(test_successful_text, "GREEN")

    except Exception as e:

        typer_secho_raise(connection_failed_text, "RED")

        exception = e.__str__()

        handle_print_exception(extract_dict(exception), exception[:5])

        return

    typer_secho_raise(creating_connection_text, "CYAN")
    typer_progress_bar()

    structured_data = format_response_data(fields_to_print, [create_response])

    print_output_format(structured_data, f"{name} platform", "yaml", False, "")

    typer_secho_raise(connection_created_text, "MAGENTA")


@app.command()
def postgres(
    name: str = NAME,
    display_name: str = DISPLAY_NAME,
    host: str = HOST,
    port: int = PORT,
    username: str = USERNAME,
    password: str = PASSWORD,
    database: str = DATABASE,
    ignored_databases: str = IGNORED_DATABASES,
    ignored_schemas: str = IGNORED_SCHEMAS,
    ignored_query_types: str = IGNORED_QUERY_TYPES,
    ignored_users: str = IGNORED_USERS,
    ignored_query_statuses: str = IGNORED_QUERY_STATUSES,
    default_schema: str = typer.Option(
        "",
        help=typer.style(
            "Ignored default schema values as comma separated string",
            fg=BRIGHT_YELLOW_COLOR_TYPER,
        ),
    ),
    only_validate: bool = ONLY_VALIDATE,
) -> None:
    """Add Postgres platform"""
    print(ignored_schemas.split(","))
    request_in = DataPlatformPostgresCreate(
        name=name,
        display_name=display_name,
        credentials=PostgresAccountDetails(
            host=host,
            port=port,
            username=username,
            password=password,
            database=database,
        ),
        additional_config=PostgresAdditionalConfig(
            ignored_databases=ignored_databases.split(","),
            ignored_schemas=ignored_schemas.split(","),
            ignored_query_types=ignored_query_types.split(","),
            ignored_users=ignored_users.split(","),
            ignored_query_statuses=ignored_query_statuses.split(","),
            default_schema=default_schema,
        ),
    )

    try:
        create_response = (
            default_api.create_postgres_platform_api_v1_platforms_postgres_post(
                request_in
            )
        )

        if only_validate:
            typer_secho_raise(testing_text, "GREEN")
            typer_progress_bar()
            default_api.test_postgres_platform_api_v1_platforms_postgres_test_post(
                request_in
            )

            typer_secho_raise(test_successful_text, "GREEN")

    except Exception as e:

        typer_secho_raise(connection_failed_text, "RED")

        exception = e.__str__()

        handle_print_exception(extract_dict(exception), exception[:5])

        return

    typer_secho_raise(creating_connection_text, "CYAN")
    typer_progress_bar()

    structured_data = format_response_data(fields_to_print, [create_response])

    print_output_format(structured_data, f"{name} platform", "yaml", False, "")

    typer_secho_raise(connection_created_text, "MAGENTA")


@app.command()
def hive(
    name: str = NAME,
    display_name: str = DISPLAY_NAME,
    host: str = HOST,
    port: str = PORT,
    username: str = USERNAME,
    password: str = PASSWORD,
    database: str = DATABASE,
    dialect: str = typer.Option(
        ...,
        help=typer.style("Dialect", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True),
    ),
    cluster_key: str = typer.Option(
        ...,
        help=typer.style("Cluster Key", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True),
    ),
    ignored_databases: str = IGNORED_DATABASES,
    ignored_schemas: str = IGNORED_SCHEMAS,
    ignored_query_types: str = IGNORED_QUERY_TYPES,
    ignored_users: str = IGNORED_USERS,
    ignored_query_statuses: str = IGNORED_QUERY_STATUSES,
    only_validate: bool = ONLY_VALIDATE,
) -> None:
    """Add Hive platform"""

    request_in = HiveAccountDetails(
        name=name,
        display_name=display_name,
        credentials=HiveAccountDetails(
            host=host,
            port=port,
            username=username,
            password=password,
            database=database,
            dialect=dialect,
            cluster_key=cluster_key,
        ),
        additional_config=HiveAdditionalConfig(
            ignored_databases=ignored_databases.split(","),
            ignored_schemas=ignored_schemas.split(","),
            ignored_query_types=ignored_query_types.split(","),
            ignored_users=ignored_users.split(","),
            ignored_query_statuses=ignored_query_statuses.split(","),
        ),
    )

    try:
        create_response = default_api.create_hive_platform_api_v1_platforms_hive_post(
            request_in
        )

        if only_validate:
            typer_secho_raise(testing_text, "GREEN")
            typer_progress_bar()
            default_api.test_hive_platform_api_v1_platforms_hive_test_post(request_in)

            typer_secho_raise(test_successful_text, "GREEN")

    except Exception as e:

        typer_secho_raise(connection_failed_text, "RED")

        exception = e.__str__()

        handle_print_exception(extract_dict(exception), exception[:5])

        return

    typer_secho_raise(creating_connection_text, "CYAN")
    typer_progress_bar()

    structured_data = format_response_data(fields_to_print, [create_response])

    print_output_format(structured_data, f"{name} platform", "yaml", False, "")

    typer_secho_raise(connection_created_text, "MAGENTA")


@app.command()
def mysql(
    name: str = NAME,
    display_name: str = DISPLAY_NAME,
    host: str = HOST,
    port: str = PORT,
    username: str = USERNAME,
    password: str = PASSWORD,
    database: str = DATABASE,
    ignored_databases: str = IGNORED_DATABASES,
    ignored_schemas: str = IGNORED_SCHEMAS,
    ignored_query_types: str = IGNORED_QUERY_TYPES,
    ignored_users: str = IGNORED_USERS,
    ignored_query_statuses: str = IGNORED_QUERY_STATUSES,
    only_validate: bool = ONLY_VALIDATE,
) -> None:
    """Add MySQL platform"""

    request_in = DataPlatformMySQLCreate(
        name=name,
        display_name=display_name,
        credentials=MySQLAccountDetails(
            host=host,
            port=port,
            username=username,
            password=password,
            database=database,
        ),
        additional_config=MySQLAdditionalConfig(
            ignored_databases=ignored_databases.split(","),
            ignored_schemas=ignored_schemas.split(","),
            ignored_query_types=ignored_query_types.split(","),
            ignored_users=ignored_users.split(","),
            ignored_query_statuses=ignored_query_statuses.split(","),
        ),
    )

    try:
        create_response = default_api.create_mysql_platform_api_v1_platforms_mysql_post(
            request_in
        )

        if only_validate:
            typer_secho_raise(testing_text, "GREEN")
            typer_progress_bar()
            default_api.test_mysql_platform_api_v1_platforms_mysql_test_post(request_in)

            typer_secho_raise(test_successful_text, "GREEN")

    except Exception as e:

        typer_secho_raise(connection_failed_text, "RED")

        exception = e.__str__()

        handle_print_exception(extract_dict(exception), exception[:5])

        return

    typer_secho_raise(creating_connection_text, "CYAN")
    typer_progress_bar()

    structured_data = format_response_data(fields_to_print, [create_response])

    print_output_format(structured_data, f"{name} platform", "yaml", False, "")

    typer_secho_raise(connection_created_text, "MAGENTA")


@app.command()
def powerbi(
    name: str = NAME,
    display_name: str = DISPLAY_NAME,
    client_id: str = typer.Option(
        ..., help=typer.style("Site Name", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True)
    ),
    client_secret: str = typer.Option(
        ...,
        help=typer.style("Access Token Name", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True),
    ),
    ignored_workspaces_names: str = typer.Option(
        "",
        help=typer.style(
            "Ignored databases values as comma separated string",
            fg=BRIGHT_YELLOW_COLOR_TYPER,
        ),
    ),
    ignore_private_workspaces: bool = typer.Option(
        False,
        help=typer.style(
            "Ignored schemas as single quotes enclosed list of strings",
            fg=BRIGHT_YELLOW_COLOR_TYPER,
        ),
    ),
    only_validate: bool = ONLY_VALIDATE,
) -> None:
    """Add PowerBI platform"""

    request_in = DataPlatformPowerBICreate(
        name=name,
        display_name=display_name,
        credentials=PowerBICredentials(
            client_id=client_id, client_secret=client_secret
        ),
        additional_config=PowerBIAdditionalConfig(
            ignored_workspaces_names=ignored_workspaces_names.split(","),
            ignore_private_workspaces=ignore_private_workspaces,
        ),
    )

    try:
        create_response = (
            default_api.create_powerbi_platform_api_v1_platforms_powerbi_post(
                request_in
            )
        )

        if only_validate:
            typer_secho_raise(testing_text, "GREEN")
            typer_progress_bar()
            default_api.test_powerbi_platform_api_v1_platforms_powerbi_test_post_endpoint(
                request_in
            )

            typer_secho_raise(test_successful_text, "GREEN")

    except Exception as e:

        typer_secho_raise(connection_failed_text, "RED")

        exception = e.__str__()

        handle_print_exception(extract_dict(exception), exception[:5])

        return

    typer_secho_raise(creating_connection_text, "CYAN")
    typer_progress_bar()

    structured_data = format_response_data(fields_to_print, [create_response])

    print_output_format(structured_data, f"{name} platform", "yaml", False, "")

    typer_secho_raise(connection_created_text, "MAGENTA")
