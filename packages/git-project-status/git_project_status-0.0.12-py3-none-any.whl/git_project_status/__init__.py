#!/usr/bin/env python3


""" Scans the local directory for sub-directories that have
git repos in them, then does a git status on them """

import os
from pathlib import Path
import sys
from git import Repo  # type: ignore

__version__ = "0.0.11"

if not os.environ.get("LOGURU_LEVEL"):
    os.environ["LOGURU_LEVEL"] = "INFO"

if os.environ.get("LOGURU_LEVEL") == "INFO":
    os.environ[
        "LOGURU_FORMAT"
    ] = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{message}</level>"  # pylint: disable=line-too-long

from loguru import logger  # pylint: disable=wrong-import-position


def handle_diff(
    repo_object: Repo,
    compare: Repo=None,
    message: str="Changes",
    ) -> None:
    """ does the checking of the diffs, outputs information on what's changed """
    if repo_object.head.commit.diff(compare):
        logger.info(f"{message}:")
        for diff_added in repo_object.head.commit.diff(compare):
            if diff_added.renamed:
                logger.info(
                    "renamed : {} -> {}", diff_added.rename_from, diff_added.rename_to
                )
            elif diff_added.new_file:
                logger.info("new file: {}", diff_added.b_path)
            elif diff_added.change_type == "M":
                logger.info("modified: {}", diff_added.b_path)
            elif diff_added.change_type == "D":
                logger.info("deleted:  {}", diff_added.b_path)
            else:
                logger.error("Unknown change type: '{}'", diff_added.change_type)
                logger.error(diff_added)
                logger.debug(dir(diff_added))


def get_dir_to_check() -> Path:
    """ figures out which directory we're trying to check """
    if len(sys.argv) > 1:
        dir_to_check = Path(os.path.expanduser(sys.argv[1]))
        if not dir_to_check.exists():
            logger.error("Couldn't find specified directory: {}", dir_to_check)
            sys.exit(1)
    else:
        dir_to_check = Path("./")
    return dir_to_check
