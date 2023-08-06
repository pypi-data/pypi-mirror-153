# Copyright (c) 2017-2021, NVIDIA CORPORATION.  All rights reserved.

"""Base class for the TAO Toolkit instance."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from abc import abstractmethod

INSTANCE_HANDLER_TASKS = ["list", "stop", "info"]


class TLTInstance(object):
    """Simple class definition for a TLT instance."""

    def __init__(self, task_map, docker_images):
        """Intialize a base instance of the tlt instance handler."""
        self.task_map = task_map
        self.dl_tasks = sorted(list(task_map.keys()))
        self.docker_images = docker_images
        self.instance_handler_tasks = INSTANCE_HANDLER_TASKS

    @staticmethod
    @abstractmethod
    def load_config(config_path):
        """Load TAO Toolkit instance config file."""
        raise NotImplementedError("Base class doesn't have this method implemented.")

    @classmethod
    def from_config(cls, config_path):
        """Initialize an instance from config."""
        raise NotImplementedError("Base class doesn't have this method implemented.")

    @abstractmethod
    def launch_command(self, command, args):
        """Launch the TAO Toolkit command."""
        raise NotImplementedError("Base class doesn't have this method implemented.")
