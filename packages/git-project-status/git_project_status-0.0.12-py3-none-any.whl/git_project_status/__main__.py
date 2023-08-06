""" cli interface """

import os
from loguru import logger

from git import Repo  # type: ignore
from git.exc import InvalidGitRepositoryError


from . import get_dir_to_check, handle_diff


def cli() -> None:
    """ Checks for dirty repositories in sub-directories and reports their state. """
    dir_to_check = get_dir_to_check()
    found_repo = False
    logger.debug("Checking {}", dir_to_check)

    for filename in os.listdir(dir_to_check):
        dirpath = os.path.normpath(f"{dir_to_check}/{filename}")
        if os.path.isdir(dirpath):
            logger.debug(f"Found dir: {dirpath}")
            try:
                repo = Repo(dirpath)
            except InvalidGitRepositoryError as error_message:
                logger.debug(
                    "{} is not a repository, skipping ({})",
                    dirpath,
                    error_message,
                )
                continue
            if repo.bare:
                logger.info("{} is bare, ignoring.", dirpath)
                continue
            found_repo = True

            if repo.is_dirty():
                try:
                    logger.warning(
                        "{} ({}) dirty",
                        dirpath,
                        repo.active_branch,
                    )
                except TypeError as error_message:
                    if repo.head.is_detached:
                        logger.info(
                            "{} is detached from {}, can't process.",
                            dirpath,
                            repo.head.object,
                        )
                        continue
                    logger.error(
                        "dirpath({}) error: {}",
                        dirpath,
                        error_message,
                    )
                    continue
                if repo.untracked_files:
                    logger.info("Untracked files:")
                    for untracked_files in repo.untracked_files:
                        logger.info(f" {untracked_files}")
                handle_diff(
                    repo,
                    compare="HEAD",
                    message="Changes staged for commit",
                )
                handle_diff(
                    repo,
                    compare=None,
                    message="Changes not staged for commit",
                )

                logger.info("")
    if not found_repo:
        logger.warning("No repositories analysed.")

if __name__ == "__main__":
    cli()
