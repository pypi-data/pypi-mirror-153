import datetime
import logging
from typing import List

import typer
from alvin_api_client.model.data_entity_id import DataEntityID
from alvin_api_client.model.data_entity_lineage_v2_request import (
    DataEntityLineageV2Request,
)
from alvin_api_client.model.data_entity_type import DataEntityType
from alvin_api_client.model.data_tag_bulk_apply import DataTagBulkApply
from alvin_api_client.model.data_tag_bulk_delete import DataTagBulkDelete
from alvin_api_client.model.data_tag_classification_type import (
    DataTagClassificationType,
)
from alvin_api_client.model.data_tag_rule_type import DataTagRuleType
from alvin_api_client.model.data_tag_type import DataTagType

from alvin_cli.schemas.models import OutputFormat
from alvin_cli.utils import default_api
from alvin_cli.utils.common_arguments import ARGUMENTS_INVALID_TEXT
from alvin_cli.utils.common_arguments import CHECK_ENTITY_VALID_TEXT
from alvin_cli.utils.common_arguments import DOMAIN
from alvin_cli.utils.common_arguments import ENTITY_ID
from alvin_cli.utils.common_arguments import ENTITY_TYPE
from alvin_cli.utils.common_arguments import FILE_NAME
from alvin_cli.utils.common_arguments import LIMIT
from alvin_cli.utils.common_arguments import OFFSET
from alvin_cli.utils.common_arguments import OUTPUT
from alvin_cli.utils.common_arguments import PLATFORM_ID
from alvin_cli.utils.common_arguments import RULE_TEXT
from alvin_cli.utils.common_arguments import RULE_TYPE
from alvin_cli.utils.common_arguments import SAVE_TO_FILE
from alvin_cli.utils.common_arguments import TAG_NAME
from alvin_cli.utils.common_arguments import TAG_TYPE
from alvin_cli.utils.helper_functions import extract_dict
from alvin_cli.utils.helper_functions import format_response_data
from alvin_cli.utils.helper_functions import handle_print_exception
from alvin_cli.utils.helper_functions import print_output_format
from alvin_cli.utils.helper_functions import structure_data_usage_stats
from alvin_cli.utils.helper_functions import structure_lineage_node_data
from alvin_cli.utils.helper_functions import typer_progress_bar
from alvin_cli.utils.helper_functions import typer_secho_raise

app = typer.Typer(add_completion=False)

TAGGABLE_ENTITIES = {
    "COLUMN",
    "TABLE",
    "DASHBOARD",
    "DASHBOARD_ELEMENT",
    "REPORT",
    "CHART",
    "WORKBOOK",
    "SHEET",
}
check_entity_valid_text = "Check the entity type is valid!"
arguments_invalid_text = "Check all the arguments are valid"


def __setup_logging() -> None:
    logging.basicConfig(level=logging.INFO)


START_TIMESTAMP = datetime.datetime.now() - datetime.timedelta(30)
POSSIBLE_ENTITY_VALUES = [v for _, v in DataEntityType.allowed_values.items()][
    0
].values()
END_TIMESTAMP = datetime.datetime.now()
RULES = ["exact", "starts_with", "contains", "ends_with", "regex"]
RULES_MAPPING = {
    "exact": "ENTITY_NAME_EXACT_MATCH",
    "starts_with": "ENTITY_NAME_START_WITH_MATCH",
    "ends_with": "ENTITY_NAME_END_WITH_MATCH",
    "contains": "ENTITY_NAME_CONTAINS_MATCH",
    "regex": "ENTITY_NAME_REGEX_MATCH",
}
fields_to_print_entity_children_and_parent = [
    "id",
    "name",
    "data_type",
    "entity_type",
]


@app.command()
def get(
    platform_id: str = PLATFORM_ID,
    entity_id: str = ENTITY_ID,
    entity_type: str = ENTITY_TYPE,
    output: OutputFormat = OUTPUT,
    save_to_file: bool = SAVE_TO_FILE,
    file_name: str = FILE_NAME,
) -> None:
    """Get Entity Info"""

    title = "Entity Data"
    entity_type = entity_type.upper()
    if entity_type not in POSSIBLE_ENTITY_VALUES:
        typer_secho_raise(CHECK_ENTITY_VALID_TEXT, "MAGENTA")
        return

    else:

        if file_name == "":
            file_name = "get_entity"
        try:
            entity_response = default_api.get_entity_api_v1_entity_get(
                platform_id=platform_id,
                entity_id=entity_id,
                entity_type=DataEntityType(entity_type),
            )
            fields_to_print = [
                "id",
                "parent_id",
                "entity_type",
                "platform_id",
                "platform_created_time",
                "platform_updated_time",
                "entity_link_to_alvin",
            ]
            if entity_response:
                structured_data = format_response_data(
                    fields_to_print, [entity_response]
                )
                print_output_format(
                    structured_data, title, output, save_to_file, file_name
                )
            else:
                typer_secho_raise(ARGUMENTS_INVALID_TEXT, "RED")

        except Exception as e:
            exception = e.__str__()
            handle_print_exception(extract_dict(exception), exception[:5])
            return


@app.command()
def children(
    platform_id: str = PLATFORM_ID,
    entity_id: str = ENTITY_ID,
    entity_type: str = ENTITY_TYPE,
    has_connections: bool = typer.Option(
        False, help=typer.style("Does it have connections?", fg=typer.colors.YELLOW)
    ),
    limit: int = LIMIT,
    offset: int = OFFSET,
    output: OutputFormat = OUTPUT,
    save_to_file: bool = SAVE_TO_FILE,
    file_name: str = FILE_NAME,
) -> None:
    """Get Entity Children"""

    if file_name == "":
        file_name = "entity_children"
    entity_type = entity_type.upper()
    if entity_type not in POSSIBLE_ENTITY_VALUES:
        typer_secho_raise(CHECK_ENTITY_VALID_TEXT, "MAGENTA")
        return
    else:

        title = "Entity Children"
        try:
            entities_children = (
                default_api.get_entity_children_api_v1_entity_children_get(
                    platform_id=platform_id,
                    entity_id=entity_id,
                    entity_type=entity_type,
                    has_connections=has_connections,
                    limit=limit,
                    offset=offset,
                )
            )

            if entities_children and entities_children["items"]:
                structured_data = format_response_data(
                    fields_to_print_entity_children_and_parent,
                    entities_children["items"],
                )
                print_output_format(
                    structured_data, title, output, save_to_file, file_name
                )
            else:
                typer_secho_raise(ARGUMENTS_INVALID_TEXT, "RED")

        except Exception as e:
            exception = e.__str__()
            handle_print_exception(extract_dict(exception), exception[:5])
            return


@app.command()
def parent(
    platform_id: str = PLATFORM_ID,
    entity_id: str = ENTITY_ID,
    entity_type: str = ENTITY_TYPE,
    output: OutputFormat = OUTPUT,
    save_to_file: bool = SAVE_TO_FILE,
    file_name: str = FILE_NAME,
) -> None:
    """Get Entity Parent"""

    title = "Entity Parent"
    if file_name == "":
        file_name = "entity_parent"
    entity_type = entity_type.upper()
    if entity_type not in POSSIBLE_ENTITY_VALUES:
        typer_secho_raise(CHECK_ENTITY_VALID_TEXT, "MAGENTA")
        return

    else:

        try:
            entities_parent = default_api.get_entity_parents_api_v1_entity_parents_get(
                platform_id=platform_id,
                entity_id=entity_id,
                entity_type=entity_type,
            )

            if entities_parent:
                structured_data = format_response_data(
                    fields_to_print_entity_children_and_parent, entities_parent
                )
                print_output_format(
                    structured_data, title, output, save_to_file, file_name
                )
            else:
                typer_secho_raise(ARGUMENTS_INVALID_TEXT, "RED")

        except Exception as e:
            exception = e.__str__()
            handle_print_exception(extract_dict(exception), exception[:5])
            return


@app.command()
def lineage(
    platform_id: str = PLATFORM_ID,
    entity_id: str = ENTITY_ID,
    entity_type: str = ENTITY_TYPE,
    lineage_direction: str = typer.Option(
        "downstream",
        "--lineage_direction",
        "-ld",
        help=typer.style("Upstream or Downstream?", fg=typer.colors.YELLOW),
    ),
    limit: int = typer.Option(
        0, help=typer.style("Limit, 0 by default", fg=typer.colors.YELLOW)
    ),
    max_levels: int = typer.Option(
        10, help=typer.style("Max Levels, 10 by default", fg=typer.colors.YELLOW)
    ),
    output: OutputFormat = OUTPUT,
    save_to_file: bool = SAVE_TO_FILE,
    file_name: str = FILE_NAME,
) -> None:
    """Get Entity Lineage Node Data"""

    title = "Entity Lineage Node Data"
    entity_type = entity_type.upper()

    if entity_type not in POSSIBLE_ENTITY_VALUES:
        typer_secho_raise(CHECK_ENTITY_VALID_TEXT, "MAGENTA")
        return

    else:
        if file_name == "":
            file_name = "lineage"
        upstream_bool = True if lineage_direction == "upstream" else False

        request_in = DataEntityLineageV2Request(
            source_entities=[
                DataEntityID(
                    platform_id=platform_id,
                    entity_type=DataEntityType(entity_type),
                    entity_id=entity_id,
                )
            ],
            upstream=upstream_bool,
            limit=limit,
            max_levels=max_levels,
        )

        try:
            lineage_data = default_api.get_entity_lineage_api_v2_lineage_post(
                request_in
            )
            if lineage_data and lineage_data["nodes"]:
                (structured_node_data) = structure_lineage_node_data(
                    lineage_data["nodes"]
                )
                print_output_format(
                    structured_node_data, title, output, save_to_file, file_name
                )
            else:
                typer_secho_raise(ARGUMENTS_INVALID_TEXT, "RED")

        except Exception as e:
            exception = e.__str__()
            handle_print_exception(extract_dict(exception), exception[:5])
            return


@app.command()
def usage(
    platform_id: str = PLATFORM_ID,
    entity_type: str = ENTITY_TYPE,
    entity_id: str = ENTITY_ID,
    start: str = typer.Option(
        START_TIMESTAMP,
        "--start",
        "-s",
        help=typer.style(
            "Stats shown for 30 days by default, edit start for other time window",
            fg=typer.colors.YELLOW,
        ),
    ),
    end: str = typer.Option(
        END_TIMESTAMP,
        "--end",
        "-e",
        help=typer.style(
            "Stats shown for 30 days by default, edit stop for other time window",
            fg=typer.colors.YELLOW,
        ),
    ),
    usage_type: List[str] = typer.Option(
        [""], help=typer.style("Usage Types", fg=typer.colors.YELLOW)
    ),
    user_name: List[str] = typer.Option(
        [""], help=typer.style("User Name", fg=typer.colors.YELLOW)
    ),
    output: OutputFormat = typer.Option(
        OutputFormat.table,
        "--output",
        "-o",
        help=typer.style(
            "Format to receive output in, default is table", fg=typer.colors.YELLOW
        ),
    ),
    save_to_file: bool = SAVE_TO_FILE,
    file_name: str = FILE_NAME,
) -> None:
    """Entity Usage Stats for 30 days by default"""

    title = "Entity Usage Stats"

    if file_name == "":
        file_name = "usage"
    entity_type = entity_type.upper()
    if entity_type not in POSSIBLE_ENTITY_VALUES:
        typer_secho_raise(CHECK_ENTITY_VALID_TEXT, "MAGENTA")
        return

    else:
        try:
            entity_usage = (
                default_api.get_entity_usage_stats_api_v1_entity_usage_stats_get(
                    platform_id=platform_id,
                    entity_id=entity_id,
                    entity_type=[entity_type],
                    start_timestamp=start,
                    end_timestamp=end,
                    usage_type=usage_type,
                    user_name=user_name,
                )
            )

            if entity_usage:
                typer_secho_raise("Usage Stats Data with following details", "MAGENTA")
                (
                    usage_stats_in_list,
                    user_name_stats,
                ) = structure_data_usage_stats(entity_usage)
                print_output_format(
                    usage_stats_in_list, title, output, save_to_file, file_name
                )
                print_output_format(
                    user_name_stats, "User Stats", output, save_to_file, file_name
                )

            else:
                typer_secho_raise(ARGUMENTS_INVALID_TEXT, "RED")

        except Exception as e:
            exception = e.__str__()
            handle_print_exception(extract_dict(exception), exception[:5])
            return


@app.command()
def tag_batch_apply(
    platform_id: str = PLATFORM_ID,
    entity_type: str = ENTITY_TYPE,
    rule_type: str = RULE_TYPE,
    rule_text: str = RULE_TEXT,
    tag_name: str = TAG_NAME,
    tag_type: str = TAG_TYPE,
    domain: str = DOMAIN,
    classification_type: str = typer.Option(
        "DEFAULT",
        "--classification_type",
        "-ct",
        help=typer.style(
            "Classification Type, choose from PII, Sensitive and Default",
            fg=typer.colors.BRIGHT_YELLOW,
            bold=True,
        ),
    ),
) -> None:
    """Bulk apply tags to entities based on rule"""

    if rule_type not in RULES:
        typer_secho_raise(
            f"Rule type not valid, select a rule from {RULES}",
            "MAGENTA",
        )
        return

    entity_type = entity_type.upper()

    if entity_type not in TAGGABLE_ENTITIES:
        typer_secho_raise(
            f"This entity type is not taggable, permitted values are {TAGGABLE_ENTITIES}",
            "MAGENTA",
        )
        return

    if entity_type not in POSSIBLE_ENTITY_VALUES:
        typer_secho_raise(CHECK_ENTITY_VALID_TEXT, "MAGENTA")
        return

    else:
        try:
            typer_secho_raise("Finding Matching Entities.....", "MAGENTA")
            typer_progress_bar()
            response = default_api.bulk_apply_api_v1_tags_bulk_apply_post(
                DataTagBulkApply(
                    platform_id=platform_id,
                    entity_type=DataEntityType(entity_type),
                    rule_type=DataTagRuleType(RULES_MAPPING[rule_type]),
                    rule_text=rule_text,
                    tag_name=tag_name,
                    domain=domain,
                    tag_type=DataTagType(tag_type.upper()),
                    classification_type=DataTagClassificationType(
                        classification_type.upper()
                    ),
                )
            )

            if response == "entities not found":
                typer_secho_raise(
                    f"No matching entities found corresponding rule '{rule_type}' match with text '{rule_text}' \U0001f92d",
                    "CYAN",
                )

            else:
                typer_secho_raise(
                    f"Bulk Applied Tag '{tag_name}' to entities matching inputted attributes including rule '{rule_text}' \U0001f44c",
                    "GREEN",
                )

        except Exception as e:
            exception = e.__str__()
            handle_print_exception(extract_dict(exception), exception[:5])
            return


@app.command()
def tag_batch_delete(
    platform_id: str = PLATFORM_ID,
    is_delete_tag_and_rules: bool = typer.Option(
        False,
        "--is_delete_tag_and_rules",
        "-delete-tag",
        help=typer.style(
            "Delete Tag and Rules for matching entities",
            fg=typer.colors.BRIGHT_GREEN,
            bold=True,
        ),
    ),
    entity_type: str = ENTITY_TYPE,
    rule_type: str = RULE_TYPE,
    rule_text: str = RULE_TEXT,
    tag_name: str = TAG_NAME,
    tag_type: str = TAG_TYPE,
    domain: str = DOMAIN,
) -> None:
    """Bulk delete tags from entities based on rule"""

    if rule_type not in RULES:
        typer_secho_raise(
            f"Rule type not valid, select a rule from {RULES}",
            "MAGENTA",
        )
        return

    entity_type = entity_type.upper()

    if entity_type not in TAGGABLE_ENTITIES:
        typer_secho_raise(
            f"This entity type is not taggable, permitted values are {TAGGABLE_ENTITIES}",
            "MAGENTA",
        )
        return

    if entity_type not in POSSIBLE_ENTITY_VALUES:
        typer_secho_raise(CHECK_ENTITY_VALID_TEXT, "MAGENTA")
        return

    else:
        try:

            request_in = DataTagBulkDelete(
                platform_id=platform_id,
                is_delete_tag_and_rules=is_delete_tag_and_rules,
                entity_type=DataEntityType(entity_type),
                rule_type=DataTagRuleType(RULES_MAPPING[rule_type]),
                rule_text=rule_text,
                tag_name=tag_name,
                domain=domain,
                tag_type=DataTagType(tag_type.upper()),
            )

            typer_secho_raise(
                f"You are about to delete tag '{tag_name}' from entities matching '{rule_type}' match rule with text '{rule_text}' on platform '{platform_id}' \U0001f62e",
                "MAGENTA",
            )
            action = typer.prompt(
                "Are you sure you want to proceed? Type 'delete' to continue \U0001f630"
            )

            if action in ["delete", "Delete", "DELETE"]:

                typer_secho_raise("Finding Matching Entities.....", "MAGENTA")
                typer_progress_bar()
                response = default_api.bulk_delete_api_v1_tags_bulk_delete_delete(
                    request_in
                )

                # if the tag is found, delete and show a message else just show appropriate prompts
                if response == "tag not found":
                    typer_secho_raise(
                        f"Tag '{tag_name}' not found in existing tag list \U0001f92d",
                        "CYAN",
                    )
                elif response == "entities not found":
                    typer_secho_raise(
                        f"No matching entities found corresponding rule {rule_type} match with text '{rule_text}' \U0001f92d",
                        "CYAN",
                    )
                else:
                    typer_secho_raise(
                        f"Bulk deleted tag  '{tag_name}' to entities from '{platform_id}' matching inputted attributes including '{rule_type}' match rule with text '{rule_text}'! \U0001f62d",
                        "RED",
                    )
            else:
                typer_secho_raise("Action not completed \U0001f60c", "BLUE")

        except Exception as e:
            exception = e.__str__()
            handle_print_exception(extract_dict(exception), exception[:5])
            return
