import json
import os
from difflib import Differ
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple

from alvin_api_client.model.impact_analysis_platform_request import (
    ImpactAnalysisPlatformRequest,
)
from alvin_api_client.model.impact_analysis_query_request import (
    ImpactAnalysisQueryRequest,
)
from alvin_api_client.model.impact_analysis_request import ImpactAnalysisRequest
from alvin_api_client.model.impact_analysis_sidebar_data_node import (
    ImpactAnalysisSidebarDataNode,
)
from alvin_api_client.model.impact_analysis_v2_response import ImpactAnalysisV2Response
from rich.console import Console
from sqlfluff.core import FluffConfig
from sqlfluff_templater_dbt.templater import DbtTemplater
from tabulate import tabulate

from alvin_cli.config import settings
from alvin_cli.schemas.models import FileGitHistory
from alvin_cli.schemas.models import GitChangeType
from alvin_cli.schemas.models import ImpactAnalysisCLIReport
from alvin_cli.schemas.models import Model
from alvin_cli.utils import default_api
from alvin_cli.utils.dbt_compile import main as dbt_compile
from alvin_cli.utils.git_metadata import get_git_history
from alvin_cli.utils.utils_dbt import get_json
from alvin_cli.utils.utils_dbt import get_model_sqls
from alvin_cli.utils.utils_dbt import get_models
from alvin_cli.utils.utils_dbt import num_of_days_from_now

console = Console()
wide_console = Console(width=350)


def check_sql_impact_analysis(paths: Sequence[str], manifest: Dict[str, Any]) -> int:
    report = ImpactAnalysisCLIReport(
        markdown_text=f"[![ALVIN](https://alvin-public-assets.s3.eu-central-1.amazonaws.com/"
        f"black-color-icon-xsmall.svg)"
        f"]({settings.alvin_ui_host})\n---\n",
        status_code=0,
    )

    # Gitlab CI handles the file changes as a str with newlines
    processed_newlines = []
    for path in paths:
        processed_newlines.extend(path.splitlines())

    # If we have an argument with spaces instead of the processed list
    processed_paths = []
    for path in processed_newlines:
        processed_paths.extend(path.split(" "))

    status_code = 0
    sqls = get_model_sqls(processed_paths, manifest)

    filenames = set(sqls.keys())
    # get manifest nodes that pre-commit found as changed
    models = get_models(manifest, filenames)

    header_text = (
        f"{len(filenames)} SQL {'File' if len(filenames) <= 1 else 'Files'} detected:\n"
    )
    report.markdown_text = report.markdown_text + f"<h4>{header_text}</h4>\n"
    for sql_path in sqls.values():
        header_text = header_text + f"{sql_path}\n"
        report.markdown_text = report.markdown_text + f"\n- {sql_path}"

    console.print(header_text, style="bold yellow")

    all_status_code = 0
    for model in models:
        # We run all, but we need to store if
        # any model execution failed
        status_code = __process_model(model, status_code, report)
        if status_code:
            all_status_code = status_code

    report.status_code = all_status_code

    with open("report.json", "w") as f:
        json.dump(report.dict(), f, ensure_ascii=False)

    return all_status_code


def __process_model(
    model: Model, status_code: int, report: ImpactAnalysisCLIReport
) -> int:
    node = model.node
    if node:
        file_git_history: Optional[FileGitHistory] = get_git_history(node)

        original_file_path = node["original_file_path"]
        relation_name = node.get("relation_name")

        # If we don't have the relation name, calculate on the fly
        if relation_name is None:
            relation_name = f"{node['database']}.{node['schema']}.{node['name']}"

        dbt_create_as_str = __resolve_dbt_query(
            original_file_path, relation_name, node["config"]
        )

        response = __call_impact_analysis_api(dbt_create_as_str, node, file_git_history)

        console.print(f"Changed Entity: [underline]{relation_name}", style="bold")

        query_report = response.query_report

        report.markdown_text = report.markdown_text + f"\n## {relation_name}"

        if query_report:
            query_report_url_code = query_report.query_report_url_code
            report_url = __create_report_url(query_report_url_code)
            wide_console.print(f"└──FULL REPORT: {report_url}", overflow="ellipsis")
            report.markdown_text = (
                report.markdown_text
                + f"\n[![RUN](https://alvin-public-assets.s3.eu-central-1.amazonaws.com/run.svg)]"
                f"({report_url})\n"
            )
        else:
            report.markdown_text = report.markdown_text + "\n\n"

        hierarchy: Dict[str, ImpactAnalysisSidebarDataNode] = response.hierarchy

        total_changed_columns = 0
        total_impacted_entities = 0
        if hierarchy:
            for entity_id, value in hierarchy.items():
                # Here we map the amount of columns deleted for each entity, right now
                # we only iterate on this once, since it processes only 1 table, on DBT
                # we do impact analysis only on table level, so parent here is always Tables.
                total_changed_children = (
                    len(value.children.keys()) if value.children else 0
                )
                total_changed_columns = total_changed_columns + total_changed_children
                total_impacted_entities = total_impacted_entities + value.num_entities

        rows = [
            ["Columns Deleted", total_changed_columns],
            ["Impacted Entities", total_impacted_entities],
        ]

        report.markdown_text = (
            report.markdown_text
            + f"\n {tabulate(rows, headers=['Metric', 'Total'], tablefmt='github')}"
        )

        console.print("Impact Summary")
        console.print("----------------------------")
        console.print(
            f"[{'yellow' if total_changed_columns > 0 else 'default'}] "
            f"Columns Deleted: {total_changed_columns}"
        )
        console.print(
            f"[{'yellow' if total_impacted_entities > 0 else 'default'}] "
            f"Impacted Entities: {total_impacted_entities}"
        )
        console.print("----------------------------")

        entity_mapping: Dict[str, List[str]] = response.entity_mapping
        entities: Dict[str, Dict[str, Any]] = response.entities

        console.print("")

        if entity_mapping:
            for entity_id, affected_entities_id in entity_mapping.items():
                entity_impact_data: Dict[str, Any] = entities.get(entity_id, {})
                entity_id_data = entity_impact_data.get("entityId", {})
                platform_id = entity_id_data.get("platformId")
                entity_type = entity_id_data.get("entityType")
                entity_id = entity_id_data.get("entityId")
                entity_url = __create_entity_url(entity_id, platform_id, entity_type)

                usage_data = entity_impact_data.get("usageStats", {})
                usage_count = usage_data.get("usageCount", 0)

                wide_console.print(
                    f"[{'red' if usage_count > 0 else 'yellow'} bold]DIRECT Impact"
                    f"[default bold] -> {entity_type} - {entity_id} - {usage_count} usage in last 30 days",
                    overflow="ellipsis",
                )

                formatted_impact_status = (
                    "![DIRECT]("
                    "https://alvin-public-assets.s3.eu-central-1.amazonaws.com/direct.svg)"
                )

                wide_console.print(f"└──URL: {entity_url}", overflow="ellipsis")

                rows = []

                report.markdown_text = (
                    report.markdown_text
                    + f"\n\n**{entity_type}** {entity_id} **DELETED**\n"
                )

                report.markdown_text = (
                    report.markdown_text
                    + "\n<details>\n<summary>Impact Report</summary>\n"
                )

                last_used_date = usage_data.get("lastUsedDate")
                rows.append(
                    [
                        0,
                        formatted_impact_status,
                        f"[{platform_id} - {entity_id}]({entity_url})",
                        entity_type,
                        num_of_days_from_now(last_used_date),
                        usage_count,
                    ]
                )

                entities_rows, status_code_sub = process_affected_entities(
                    affected_entities_id,
                    entities,
                )

                rows.extend(entities_rows)

                if status_code_sub == 1:
                    status_code = status_code_sub

                report.markdown_text = (
                    report.markdown_text
                    + f"\n\n{tabulate(rows, headers=['Depth', 'Impact', 'Name', 'Type', 'Last Used', '30 Day Usage'], tablefmt='github')}"
                )
                report.markdown_text = report.markdown_text + "\n</details>\n"

                console.print("")

    else:
        status_code = 1
        print(f"Invalid model `{model.model_id}` in manifest file. ")
    return status_code


def process_affected_entities(
    affected_entities_id: List[str],
    entities: Dict[str, Dict[str, Any]],
) -> Tuple[List, int]:
    status_code = 0
    rows = []
    if affected_entities_id:
        status_code = 1
        affected_entity_count = 0

        console.print("   └──Downstream ENTITIES", style="bold")

        for affected_entity_id in affected_entities_id:
            entity_impact_data: Dict[str, Any] = entities.get(affected_entity_id, {})
            impact_status = entity_impact_data.get("impactStatus")

            # Ignore Direct Impact, since its reported as a summary
            # Otherwise its duplicated.
            if impact_status == "DIRECT":
                continue

            entity_id_data = entity_impact_data.get("entityId", {})
            platform_id = entity_id_data.get("platformId")
            entity_type = entity_id_data.get("entityType")
            entity_id = entity_id_data.get("entityId")
            entity_url = __create_entity_url(entity_id, platform_id, entity_type)

            usage_data = entity_impact_data.get("usageStats", {}) or {}
            usage_count = usage_data.get("usageCount", 0)

            affected_entity_color = ""

            if impact_status == "STALE":
                affected_entity_color = "yellow"
            elif impact_status == "BREAKING":
                affected_entity_color = "red"
            elif impact_status == "QUALITY":
                affected_entity_color = "yellow"

            # We use len(affected_entities_id) - 2
            # since the count is zero based and we have to remove one item for the
            # summary entity.
            is_last_reported_entity = (
                affected_entity_count == len(affected_entities_id) - 2
            )
            tree_char = "      └──" if is_last_reported_entity else "      ├──"

            wide_console.print(
                f"{tree_char}"
                f"[{affected_entity_color} bold]{impact_status} Impact"
                f"[default bold] -> {platform_id} - {entity_type} - {entity_id} - "
                f"{usage_count} usage in last 30 days",
                overflow="ellipsis",
            )

            formatted_impact_status = ""
            if impact_status == "BREAKING":
                formatted_impact_status = (
                    "![BREAKING]("
                    "https://alvin-public-assets.s3.eu-central-1.amazonaws.com/breaking-g.svg)"
                )
            elif impact_status == "STALE":
                formatted_impact_status = (
                    "![STALE]("
                    "https://alvin-public-assets.s3.eu-central-1.amazonaws.com/stale.svg)"
                )
            elif impact_status == "QUALITY":
                formatted_impact_status = (
                    "![QUALITY]("
                    "https://alvin-public-assets.s3.eu-central-1.amazonaws.com/quality.svg)"
                )

            level = entity_impact_data.get("level")
            last_used_date = usage_data.get("lastUsedDate")

            rows.append(
                [
                    level,
                    formatted_impact_status,
                    f"[{platform_id} - {entity_id}]({entity_url})"
                    if entity_type == "COLUMN"
                    else f"{platform_id} - {entity_id}",
                    entity_type,
                    num_of_days_from_now(last_used_date),
                    usage_count,
                ]
            )

            tree_char = "         └──" if is_last_reported_entity else "      │  └──"

            if entity_type == "COLUMN":
                wide_console.print(f"{tree_char}URL: {entity_url}", overflow="ellipsis")

            affected_entity_count += 1

    return rows, status_code


def __create_report_query_diff(
    previous_query: str, query: str, report: ImpactAnalysisCLIReport
) -> None:
    d = Differ()
    report.markdown_text = (
        report.markdown_text + "\n<details>\n<summary>Query Diff</summary>\n"
    )
    query_compare_diff = "\n".join(
        list(d.compare(query.splitlines(), previous_query.splitlines()))
    )
    report.markdown_text = report.markdown_text + f"```diff\n{query_compare_diff}\n```"
    report.markdown_text = report.markdown_text + "\n</details>\n"


def __create_report_url(query_report_url_code: str) -> str:
    report_url = f"{settings.alvin_ui_host}/tinyurl?code={query_report_url_code}"
    return report_url


def __create_entity_url(
    entity_id: str, entity_platform_id: str, entity_type: str
) -> str:
    entity_url = f"{settings.alvin_ui_host}/entity/{entity_platform_id}/{entity_type}/{entity_id}"
    return entity_url


def __resolve_dbt_query(
    original_file_path: str, relation_name: str, node_config: Dict[str, Any]
) -> str:
    dbt_templater = DbtTemplater()
    fluff_config = FluffConfig.from_root()
    template_result, _ = dbt_templater.process(
        fname=original_file_path, config=fluff_config
    )
    # [fixme] load platformId based on profile
    # we can get the profile_name at dbt_templater.config.profile_name
    # we probably should do a simple mapping between dbt profile and platformId
    # and also the credentials in case we need it, dbt_templater.config.credentials
    templated_str = template_result.templated_str

    entity_type = "table"

    # [fixme] look at types of materialization are possible
    # and which ones make sense to handle here
    materialized = node_config.get("materialized")
    if materialized:
        if materialized == "view":
            entity_type = materialized

    # [fixme] we simulate the statement DBT will use to create the relation
    # we can use the DBT macro, to create exactly the same statement later.
    dbt_create_as_str = f"""create or replace {entity_type} {relation_name}
              as (
                {templated_str}
              )
            """
    return dbt_create_as_str


def __call_impact_analysis_api(
    dbt_create_as_str: str,
    node: Dict[str, Any],
    file_git_history: Optional[FileGitHistory],
) -> ImpactAnalysisV2Response:

    impact_analysis_query_request = ImpactAnalysisQueryRequest(
        source_text=dbt_create_as_str
    )
    impact_analysis_platform_request = ImpactAnalysisPlatformRequest(
        id=settings.alvin_platform_id
    )
    impact_analysis_request = ImpactAnalysisRequest(
        query=impact_analysis_query_request, platform=impact_analysis_platform_request
    )

    if file_git_history:
        change_type = file_git_history.change_type
        if (
            change_type == GitChangeType.MODEL_FILE_RENAME
            or change_type == GitChangeType.MODEL_ALIAS_RENAME
        ):
            model_name = file_git_history.model_name
            previous_model_name = file_git_history.previous_model_name
            if model_name != previous_model_name:
                renamed_entity_id = (
                    f"{node['database']}.{node['schema']}.{previous_model_name}"
                )
                impact_analysis_query_request.renamed_entity_id = renamed_entity_id

    response: ImpactAnalysisV2Response = (
        default_api.get_impact_by_query_api_v2_impact_analysis_query_post(
            impact_analysis_request
        )
    )
    return response


def run_check_sql_impact_analysis(file_names: List, manifest_file: str) -> None:
    root_dir = os.getcwd()
    if settings.debug:
        print(root_dir)
    settings.root_dir = root_dir
    if settings.dbt_root_dir:
        os.chdir(settings.dbt_root_dir)
        if settings.debug:
            print(os.getcwd())

    manifest = None
    try:
        print("Executing DBT compile to update manifest file.")
        dbt_compile()
        manifest = get_json(manifest_file)
    except Exception as e:
        print(f"Unable to load manifest file ({e})")
        exit(1)

    if manifest:
        exit(check_sql_impact_analysis(paths=file_names, manifest=manifest))
