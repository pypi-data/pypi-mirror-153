# git_project_status

Real simple, just iterates through the first-level subdirectories and does the equivalent of git status, only uglier.

If you want more logs, set an environment variable of `LOGURU_LOG_LEVEL=DEBUG`.

Installation: `pip install git-project-status`

Which will create a console script `git_project_status`.

## Changelog

 * 0.0.6 - Fixed handling detached heads.
 * 0.0.7 - 2022-01-08 - Updated build tooling, broke the script name. Whoops! Pulled.
 * 0.0.8 - 2022-01-08 - Fixed the script name. Whoops! Pulled.
 * 0.0.9 - 2022-01-08 - Fixed the script config.
 * 0.0.10 - 2022-01-08 - Added the option to specify a directory.
 * 0.0.11 - 2022-01-08 - Cleaned up some formatting, using pathlib for checking.
 * 0.0.12 - 2022-06-02 - Shaved the yak, moved packaging tools, added more type-checking.
