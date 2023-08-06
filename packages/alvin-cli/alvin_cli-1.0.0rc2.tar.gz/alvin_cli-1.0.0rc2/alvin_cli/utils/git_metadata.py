import os
import re
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Optional

from git import Git
from git import Repo

from alvin_cli.config import settings
from alvin_cli.schemas.models import FileGitHistory
from alvin_cli.schemas.models import GitChangeType

DBT_ALIAS_REGEX = re.compile(r"^(?s:.)*config\(alias='(?P<alias>.*)'\).*", re.MULTILINE)


def load_git_history(repo: Repo, node: Any) -> Optional[FileGitHistory]:
    """Return git metadata for a file in the git repo."""
    try:
        original_file_path = node["original_file_path"]
        path = get_file_path(original_file_path)

        file_name = Path(path).stem

        # Initialize with default values, we begin assuming
        # new model name and previous model names were the same
        file_git_history = FileGitHistory(
            path=path,
            file_name=file_name,
            model_name=file_name,
            previous_path=path,
            previous_file_name=file_name,
            previous_model_name=file_name,
            change_type=GitChangeType.NONE,
        )

        revlist = (
            (commit, (commit.tree / path).data_stream.read())
            for commit in repo.iter_commits(paths=path)
        )

        # fetch current commit
        current_commit, current_file_contents = next(revlist)

        # Compare with source branch
        diff_items = current_commit.diff(f"origin/{settings.git_compare_branch}")
        # Check first if it's a file rename
        for diff_item in diff_items:
            a_path = diff_item.a_path
            if a_path == path:
                # The rename_to is actually the older name
                rename_to = diff_item.rename_to
                if rename_to:
                    previous_path = diff_item.rename_to
                    previous_file_name = Path(previous_path).stem
                    file_git_history.previous_path = previous_path
                    file_git_history.previous_file_name = previous_file_name
                    file_git_history.previous_model_name = previous_file_name

        # Now check if the alias changed
        commit = repo.commit(settings.git_compare_branch)

        if file_git_history.previous_file_name != file_git_history.file_name:
            path = file_git_history.previous_path

        compare_file_contents = (commit.tree / path).data_stream.read()
        current_file_as_str = current_file_contents.decode("utf-8")
        compare_file_as_str = compare_file_contents.decode("utf-8")
        current_file_alias = __get_alias(current_file_as_str)
        old_file_alias = __get_alias(compare_file_as_str)

        file_git_history.file_alias = current_file_alias
        if current_file_alias:
            file_git_history.model_name = current_file_alias
        file_git_history.previous_file_alias = old_file_alias
        if old_file_alias:
            file_git_history.previous_model_name = old_file_alias

        # We don't have aliases
        if not current_file_alias and not old_file_alias:
            # It's a file rename, so this will generate a new model name
            if file_git_history.file_name != file_git_history.previous_file_name:
                file_git_history.change_type = GitChangeType.MODEL_FILE_RENAME
                return file_git_history

        # This means the alias didn't change so nothing happened
        if current_file_alias == old_file_alias:
            file_git_history.change_type = GitChangeType.NONE
            return file_git_history

        # This means the old file alias was used as the model name
        if old_file_alias != current_file_alias:
            file_git_history.change_type = GitChangeType.MODEL_ALIAS_RENAME
            return file_git_history

        return file_git_history

    except Exception as err:
        # e.g.: Ignore all errors if we are unable to use the repo metadata
        if settings.debug:
            print(f"Unable to process git history: {err}")

    return None


def get_file_path(file_path: str) -> str:
    if settings.dbt_root_dir:
        path = os.path.join(settings.dbt_root_dir, file_path)
    else:
        path = file_path
    return path


def __get_alias(file_contents: str) -> Optional[str]:
    match = re.match(pattern=DBT_ALIAS_REGEX, string=file_contents)
    if match:
        alias = match.group("alias")
        return alias
    return None


def get_git_history(node: Dict[str, Any]) -> Optional[FileGitHistory]:
    # Get git repo object for git metadata
    try:
        if settings.debug:
            print(f"GITHUB_HEAD_REF: {os.environ.get('GITHUB_HEAD_REF')}")
            print(Git().version())

        repo: Repo = Repo(settings.root_dir, search_parent_directories=True)
        try:
            active_branch: Optional[str] = repo.active_branch.name
        except Exception as err:
            # [TODO] add logic for GitLab PR branch
            github_pr_branch = os.environ.get("GITHUB_HEAD_REF")

            if settings.debug:
                print(f"Exception getting active_branch: {err}")
                print(f"GitHub PR Branch: {github_pr_branch}")

            print("Start fetching branches/commits for diff comparison")
            repo.git.fetch()
            repo.git.checkout(settings.git_compare_branch)
            repo.git.checkout(github_pr_branch)
            active_branch = github_pr_branch
            print("Done fetching branches/commits for diff comparison")
        if settings.debug:
            print(
                f"active_branch: {active_branch} target_branch: {settings.git_compare_branch}"
            )
        file_git_history = load_git_history(repo, node)
        if settings.debug:
            print(file_git_history)
        return file_git_history
    except Exception as err:
        # e.g.: Ignore all errors if we are unable to load the repository
        if settings.debug:
            print(f"Exception loading git history: {err}")
    return None
