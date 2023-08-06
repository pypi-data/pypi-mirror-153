import logging

import typer
from alvin_api_client.model.data_entity_type import DataEntityType
from alvin_api_client.model.manual_lineage_data_request import ManualLineageDataRequest

from alvin_cli.schemas.models import OutputFormat
from alvin_cli.utils import default_api
from alvin_cli.utils.common_arguments import BRIGHT_YELLOW_COLOR_TYPER
from alvin_cli.utils.common_arguments import FILE_NAME
from alvin_cli.utils.common_arguments import FROM_ENTITY_ID
from alvin_cli.utils.common_arguments import FROM_ENTITY_PLATFORM_ID
from alvin_cli.utils.common_arguments import FROM_ENTITY_TYPE
from alvin_cli.utils.common_arguments import LIMIT
from alvin_cli.utils.common_arguments import OFFSET
from alvin_cli.utils.common_arguments import OUTPUT
from alvin_cli.utils.common_arguments import SAVE_TO_FILE
from alvin_cli.utils.common_arguments import TO_ENTITY_ID
from alvin_cli.utils.common_arguments import TO_ENTITY_PLATFORM_ID
from alvin_cli.utils.common_arguments import TO_ENTITY_TYPE
from alvin_cli.utils.helper_functions import extract_dict
from alvin_cli.utils.helper_functions import format_response_data
from alvin_cli.utils.helper_functions import handle_print_exception
from alvin_cli.utils.helper_functions import print_output_format
from alvin_cli.utils.helper_functions import typer_progress_bar
from alvin_cli.utils.helper_functions import typer_secho_raise

app = typer.Typer(add_completion=False)


def __setup_logging() -> None:
    logging.basicConfig(level=logging.INFO)


fields_to_print = [
    "connection_created_time",
    "from_entity_id",
    "from_entity_platform_id",
    "from_entity_platform_type",
    "from_entity_type",
    "to_entity_id",
    "to_entity_platform_id",
    "to_entity_platform_type",
    "to_entity_type",
    "connection_type",
    "created_by",
    "description",
]


@app.command()
def list(
    limit: int = LIMIT,
    offset: int = OFFSET,
    output: OutputFormat = OUTPUT,
    save_to_file: bool = SAVE_TO_FILE,
    file_name: str = FILE_NAME,
) -> None:
    """List Manual Lineage Data"""
    try:
        response = default_api.list_manual_lineage_api_v1_lineage_manual_get(
            limit=limit, offset=offset
        )
        structured_data = format_response_data(fields_to_print, response["items"])
        print_output_format(
            structured_data,
            output=output,
            table_title="Manual Lineage Data",
            save_to_file=save_to_file,
            file_name=file_name,
        )

    except Exception as e:
        exception = e.__str__()
        handle_print_exception(extract_dict(exception), exception[:5])
        return


@app.command()
def add(
    from_entity_id: str = FROM_ENTITY_ID,
    from_entity_type: str = FROM_ENTITY_TYPE,
    from_entity_platform_id: str = FROM_ENTITY_PLATFORM_ID,
    to_entity_id: str = TO_ENTITY_ID,
    to_entity_type: str = TO_ENTITY_TYPE,
    to_entity_platform_id: str = TO_ENTITY_PLATFORM_ID,
    description: str = typer.Option(
        ...,
        "--description",
        "-des",
        help=typer.style(
            "Description for this connection", fg=BRIGHT_YELLOW_COLOR_TYPER, bold=True
        ),
    ),
) -> None:
    """Add Manual Lineage Data"""
    from_entity_type = from_entity_type.upper()
    to_entity_type = to_entity_type.upper()

    try:
        response = default_api.add_manual_lineage_api_v1_lineage_manual_post(
            ManualLineageDataRequest(
                from_entity_id=from_entity_id,
                from_entity_type=DataEntityType(from_entity_type),
                from_entity_platform_id=from_entity_platform_id,
                to_entity_id=to_entity_id,
                to_entity_type=DataEntityType(to_entity_type),
                to_entity_platform_id=to_entity_platform_id,
                description=description,
            )
        )

        # the api reponse contains a response code and string message, so checking the size of the response
        if response and len(response) > 1:
            message_str = response[1].get("strMessage")
            if message_str == "invalid platform_id":
                typer_secho_raise(
                    "Platform ID is invalid, check both from and to platform IDs",
                    "MAGENTA",
                )
                return
            if message_str == "invalid entity_type":
                typer_secho_raise(
                    "Entity Type is invalid, check both from and to entity types",
                    "MAGENTA",
                )
                return
            if message_str == "entity_id not found":
                typer_secho_raise(
                    "Entity ID not found, check both from and to Entity IDs", "MAGENTA"
                )
                return
            if message_str == "invalid entity_id":
                typer_secho_raise(
                    "Entity ID is invalid, check both from and to Entity IDs ",
                    "MAGENTA",
                )
                return
            else:
                typer_secho_raise("Manual Lineage Data Saved!", "GREEN")

        else:
            typer_secho_raise("Action not completed", "BLUE")

    except Exception as e:
        exception = e.__str__()
        handle_print_exception(extract_dict(exception), exception[:5])
        return


@app.command()
def delete(
    from_entity_id: str = FROM_ENTITY_ID,
    from_entity_type: str = FROM_ENTITY_TYPE,
    from_entity_platform_id: str = FROM_ENTITY_PLATFORM_ID,
    to_entity_id: str = TO_ENTITY_ID,
    to_entity_type: str = TO_ENTITY_TYPE,
    to_entity_platform_id: str = TO_ENTITY_PLATFORM_ID,
) -> None:
    """Delete Manuanl Lineage Data"""
    from_entity_type = from_entity_type.upper()
    to_entity_type = to_entity_type.upper()

    try:
        typer_secho_raise(
            f"You are about to delete manual lineage data from entity {from_entity_id} to entity {to_entity_id} \U0001f62e",
            "MAGENTA",
        )
        action = typer.prompt(
            "Are you sure you want to proceed? Type 'delete' to continue \U0001f630"
        )

        if action in ["delete", "Delete", "DELETE"]:
            typer_secho_raise("Finding Matching Data.....", "MAGENTA")
            typer_progress_bar()

            response = default_api.delete_manual_lineage_api_v1_lineage_manual_delete(
                ManualLineageDataRequest(
                    from_entity_id=from_entity_id,
                    from_entity_type=DataEntityType(from_entity_type),
                    from_entity_platform_id=from_entity_platform_id,
                    to_entity_id=to_entity_id,
                    to_entity_type=DataEntityType(to_entity_type),
                    to_entity_platform_id=to_entity_platform_id,
                )
            )

            # the api reponse contains a response code and string message, so checking the size of the response
            if response and len(response) > 1:
                message_str = response[1].get("strMessage")

                if message_str == "invalid platform_id":
                    typer_secho_raise(
                        "Platform ID is invalid, check both from and to platform IDs",
                        "MAGENTA",
                    )
                    return
                if message_str == "invalid entity_type":
                    typer_secho_raise(
                        "Entity Type is invalid, check both from and to entity types",
                        "MAGENTA",
                    )
                    return
                if message_str == "entity_id not found":
                    typer_secho_raise(
                        "Entity ID not found, check both from and to Entity IDs",
                        "MAGENTA",
                    )
                    return
                if message_str == "invalid entity_id":
                    typer_secho_raise(
                        "Entity ID is invalid, check both from and to Entity IDs ",
                        "MAGENTA",
                    )
                    return
                if message_str == "manual lineage data not found":
                    typer_secho_raise("Manual Lineage Data Not Found! ", "MAGENTA")
                    return
                else:
                    typer_secho_raise(
                        f"Delete Manual Lineage Data from {from_entity_id} to {to_entity_id}! \U0001f62d",
                        "RED",
                    )
        else:
            typer_secho_raise("Action not completed \U0001f60c", "BLUE")

    except Exception as e:
        exception = e.__str__()
        handle_print_exception(extract_dict(exception), exception[:5])
        return
