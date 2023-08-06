# QUANTCONNECT.COM - Democratizing Finance, Empowering Individuals.
# Lean CLI v1.0. Copyright 2021 QuantConnect Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
import re
import subprocess
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, List

from pkg_resources import Requirement

from ablean.components.module_manager import ModuleManager
from ablean.components.config.lean_config_manager import LeanConfigManager
from ablean.components.config.output_config_manager import OutputConfigManager
from ablean.components.config.project_config_manager import ProjectConfigManager
from ablean.components.util.logger import Logger
from ablean.components.util.project_manager import ProjectManager
from ablean.components.util.temp_manager import TempManager
from ablean.components.util.xml_manager import XMLManager
from ablean.constants import MODULES_DIRECTORY, TERMINAL_LINK_PRODUCT_ID, PROJECT_CONFIG_FILE_NAME
from ablean.models.utils import DebuggingMethod


class LeanRunner:
    """The LeanRunner class contains the code that runs the LEAN engine locally."""

    def __init__(
        self,
        logger: Logger,
        project_config_manager: ProjectConfigManager,
        lean_config_manager: LeanConfigManager,
        output_config_manager: OutputConfigManager,
        module_manager: ModuleManager,
        project_manager: ProjectManager,
        temp_manager: TempManager,
        xml_manager: XMLManager,
    ) -> None:
        """Creates a new LeanRunner instance.

        :param logger: the logger that is used to print messages
        :param project_config_manager: the ProjectConfigManager instance to retrieve project configuration from
        :param lean_config_manager: the LeanConfigManager instance to retrieve Lean configuration from
        :param output_config_manager: the OutputConfigManager instance to retrieve backtest/live configuration from
        :param docker_manager: the DockerManager instance which is used to interact with Docker
        :param module_manager: the ModuleManager instance to retrieve the installed modules from
        :param project_manager: the ProjectManager instance to use for copying source code to output directories
        :param temp_manager: the TempManager instance to use for creating temporary directories
        :param xml_manager: the XMLManager instance to use for reading/writing XML files
        """
        self._logger = logger
        self._project_config_manager = project_config_manager
        self._lean_config_manager = lean_config_manager
        self._output_config_manager = output_config_manager
        self._module_manager = module_manager
        self._project_manager = project_manager
        self._temp_manager = temp_manager
        self._xml_manager = xml_manager

    def run_lean(
        self,
        lean_config: Dict[str, Any],
        environment: str,
        algorithm_file: Path,
        output_dir: Path
    ) -> None:
        """Runs the LEAN engine locally in Docker.

        Raises an error if something goes wrong.

        :param lean_config: the LEAN configuration to use
        :param environment: the environment to run the algorithm in
        :param algorithm_file: the path to the file containing the algorithm
        :param output_dir: the directory to save output data to
        :param debugging_method: the debugging method if debugging needs to be enabled, None if not
        """
        project_dir = algorithm_file.parent

        # Copy the project's code to the output directory
        self._project_manager.copy_code(algorithm_file.parent, output_dir / "code")

        cli_root_dir = self._lean_config_manager.get_cli_root_directory()
        relative_project_dir = project_dir.relative_to(cli_root_dir)
        relative_output_dir = output_dir.relative_to(cli_root_dir)
        
        # Save config.json to ouput
        config_path = output_dir / PROJECT_CONFIG_FILE_NAME
        with config_path.open("w+", encoding="utf-8") as file:
            file.write(json.dumps(lean_config, indent=4))
        
        cwd = str(cli_root_dir.joinpath("launcher"))
        subprocess.run(["dotnet", "QuantConnect.Lean.Launcher.dll", "--config", f"{str(config_path)}"], cwd=cwd)

        self._logger.info(
            f"Successfully ran '{relative_project_dir}' in the '{environment}' environment and stored the output in '{relative_output_dir}'"
        )