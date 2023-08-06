# Copyright (c) 2017-2021, NVIDIA CORPORATION.  All rights reserved.

"""Simple script to launch TAO Toolkit commands."""

import argparse
import logging
import os
import sys

from tlt.components.instance_handler.base_instance import INSTANCE_HANDLER_TASKS as CLI_TASKS
from tlt.components.instance_handler.local_instance import LocalInstance
from tlt.components.instance_handler.utils import (
    get_config_file
)

logger = logging.getLogger(__name__)

PYTHON_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def build_command_line_parser(parser=None, supported_tasks=None):
    """Build command line parser for the TAO Toolkit launcher."""
    if parser is None:
        parser = argparse.ArgumentParser(
            prog="tao", description="Launcher for TAO Toolkit.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
    module_subparser = parser.add_subparsers(title="tasks")

    # Parser for tlt subtasks.
    for task in supported_tasks:
        subparser = module_subparser.add_parser(
            task,
            parents=[parser],
            add_help=False
        )
        if task not in CLI_TASKS:
            subparser.add_argument(
                "script_args",
                nargs=argparse.REMAINDER,
                type=str,
                default=None,
            )
        else:
            if task == "stop":
                # List of container id's to be closed.
                subparser.add_argument(
                    "--container_id",
                    type=str,
                    nargs="+",
                    required=False,
                    default=None,
                    help="Ids of the containers to be stopped."
                )
                # Force shutdown all containers.
                subparser.add_argument(
                    "--all",
                    action="store_true",
                    default=False,
                    help="Kill all running TAO Toolkit containers.",
                    required=False
                )
            elif task == "info":
                subparser.add_argument(
                    "--verbose",
                    action="store_true",
                    default=False,
                    help="Print information about the TAO Toolkit instance."
                )
            else:
                pass
    return parser


def main(args=sys.argv[1:]):
    """TLT entrypoint script to the TAO Toolkit Launcher."""
    # TODO: @vpraveen: Logger config has been hardcoded. Do remember to fix this.
    verbosity = logging.INFO
    if os.getenv("TAO_LAUNCHER_DEBUG", "0") == "1":
        verbosity = logging.DEBUG

    # Configuring the logger.
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        level=verbosity
    )

    # Build the default list of tasks to be supported.
    launcher_config_file = get_config_file()
    local_instance = LocalInstance.from_config(launcher_config_file)

    supported_tasks = [*CLI_TASKS, *local_instance.dl_tasks]
    if not args:
        args = ["--help"]
    task = args[0]

    # Parse launcher command line arguments.
    parser = build_command_line_parser(parser=None, supported_tasks=supported_tasks)
    # parser.print_help()

    if task not in local_instance.dl_tasks:
        parsed_args, unknown_args = parser.parse_known_args(args)  # noqa pylint: disable=W0612
        # TODO: CLI related actions to be implemented
        # --> init  (to download the config, validate and place it at ~/.tlt/config.json)
        # --> update (to download the latest config and update the config in the default path.)
        # --> list (to list active TAO Toolkit container instances.)
        # run_cli_instruction(task, parsed_args)
        local_instance.launch_command(
            task,
            parsed_args
        )
    else:
        local_instance.launch_command(
            task,
            args[1:]
        )


if __name__ == "__main__":
    main(sys.argv[1:])
