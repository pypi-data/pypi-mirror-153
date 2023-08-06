import time

import typer

from alvin_cli.platforms import add as add_methods
from alvin_cli.schemas.models import OutputFormat
from alvin_cli.utils import default_api
from alvin_cli.utils.common_arguments import FILE_NAME
from alvin_cli.utils.common_arguments import OUTPUT
from alvin_cli.utils.common_arguments import PLATFORM_ID
from alvin_cli.utils.common_arguments import SAVE_TO_FILE
from alvin_cli.utils.helper_functions import extract_dict
from alvin_cli.utils.helper_functions import format_response_data
from alvin_cli.utils.helper_functions import handle_print_exception
from alvin_cli.utils.helper_functions import print_output_format
from alvin_cli.utils.helper_functions import typer_secho_raise

app = typer.Typer(add_completion=False)

app.add_typer(add_methods.app, name="add")

fields_to_print = [
    "id",
    "name",
    "platform_type",
    "created",
    "last_updated",
    "is_syncing",
    "additional_config",
]


@app.command()
def list(
    output: OutputFormat = OUTPUT,
    save_to_file: bool = SAVE_TO_FILE,
    file_name: str = FILE_NAME,
) -> None:
    """List all platforms"""

    if file_name == "":
        file_name = "platform_list"
    try:
        table_title = "List Of Platforms"
        platforms_list = default_api.get_platforms_api_v1_platforms_get()
        structured_data = format_response_data(fields_to_print, platforms_list)
        print_output_format(
            structured_data, table_title, output, save_to_file, file_name
        )

    except Exception as e:
        exception = e.__str__()
        handle_print_exception(extract_dict(exception), exception[:5])
        return


@app.command()
def get(
    platform_id: str = PLATFORM_ID,
    output: OutputFormat = OUTPUT,
    save_to_file: bool = SAVE_TO_FILE,
    file_name: str = FILE_NAME,
) -> None:
    """Get platform details"""

    if file_name == "":
        file_name = "platform_get"

    try:
        platform_response = default_api.get_platform_api_v1_platforms_platform_id_get(
            platform_id
        )

        if platform_response:
            table_title = f"{platform_id} Details"
            structured_data = format_response_data(fields_to_print, [platform_response])
            print_output_format(
                structured_data, table_title, output, save_to_file, file_name
            )
        else:
            typer_secho_raise("Check arguments are valid", "RED")

    except Exception as e:
        exception = e.__str__()
        handle_print_exception(extract_dict(exception), exception[:5])
        return


@app.command()
def delete(platform_id: str = PLATFORM_ID) -> None:
    """Delete platform"""

    try:
        typer_secho_raise(
            f"You are about to delete platform '{platform_id}' \U0001f62e ", "MAGENTA"
        )
        action = typer.prompt(
            f"Are you sure you want to proceed? This will delete {platform_id} and corresponding data from Alvin and you will have to connect the platform again to use. Type 'delete' to continue \U0001f630"
        )

        if action in ["delete", "Delete", "DELETE"]:

            typer_secho_raise(f"Deleting {platform_id}.......", "CYAN")
            with typer.progressbar(range(100)) as progress:
                for i in range(4):
                    time.sleep(0.1)
                    progress.update(25)

            default_api.delete_platform_api_v1_platforms_platform_id_delete(platform_id)
            typer_secho_raise(
                f"Platform {platform_id} deleted! \U0001f62d",
                "RED",
            )

        else:
            typer_secho_raise("Action not completed \U0001f60c", "BLUE")

    except Exception as e:
        exception = e.__str__()
        handle_print_exception(extract_dict(exception), exception[:5])
        return


@app.command()
def sync(platform_id: str = PLATFORM_ID) -> None:
    """Sync platform"""

    try:
        default_api.sync_platform_rpc_api_v1_platforms_platform_id_rpc_sync_get(
            platform_id
        )

        typer_secho_raise(f"{platform_id} sync scheduled! \u23f1\ufe0f", "CYAN")

    except Exception as e:
        exception = e.__str__()
        handle_print_exception(extract_dict(exception), exception[:5])
        return
