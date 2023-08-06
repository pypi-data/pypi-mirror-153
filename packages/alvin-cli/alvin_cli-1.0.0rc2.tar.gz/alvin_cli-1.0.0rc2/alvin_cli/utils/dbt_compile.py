import argparse
from typing import List
from typing import Optional
from typing import Sequence

from alvin_cli.utils.utils_dbt import add_dbt_cmd_args
from alvin_cli.utils.utils_dbt import add_dbt_cmd_model_args
from alvin_cli.utils.utils_dbt import add_filenames_args
from alvin_cli.utils.utils_dbt import get_flags
from alvin_cli.utils.utils_dbt import run_dbt_cmd


def prepare_cmd(
    global_flags: Optional[Sequence[str]] = None,
    cmd_flags: Optional[Sequence[str]] = None,
    models: Optional[Sequence[str]] = None,
) -> List[str]:
    global_flags = get_flags(global_flags)
    cmd_flags = get_flags(cmd_flags)
    if models:
        dbt_models = models
        cmd = ["dbt", *global_flags, "compile", "-m", *dbt_models, *cmd_flags]
    else:
        cmd = ["dbt", *global_flags, "compile", *cmd_flags]
    return cmd


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    add_filenames_args(parser)
    add_dbt_cmd_args(parser)
    add_dbt_cmd_model_args(parser)

    args = parser.parse_args(argv)

    cmd = prepare_cmd(
        args.global_flags,
        args.cmd_flags,
        args.models,
    )
    return run_dbt_cmd(cmd)


if __name__ == "__main__":
    exit(main())
