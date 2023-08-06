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

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from ablean.components.config.cli_config_manager import CLIConfigManager
from ablean.components.config.lean_config_manager import LeanConfigManager
from ablean.components.config.output_config_manager import OutputConfigManager
from ablean.components.config.project_config_manager import ProjectConfigManager
from ablean.components.config.storage import Storage
from ablean.components.util.logger import Logger
from ablean.components.util.name_generator import NameGenerator
from ablean.components.util.path_manager import PathManager
from ablean.components.util.platform_manager import PlatformManager
from ablean.components.util.project_manager import ProjectManager
from ablean.components.util.temp_manager import TempManager
from ablean.components.util.xml_manager import XMLManager
from ablean.components.module_manager import ModuleManager
from ablean.components.lean_runner import LeanRunner
from ablean.constants import CACHE_PATH, CREDENTIALS_CONFIG_PATH, GENERAL_CONFIG_PATH
from ablean.data_manager import DataManager

class Container(DeclarativeContainer):
    """The Container class wires all reusable components together."""

    logger = Singleton(Logger)
    xml_manager = Singleton(XMLManager)
    platform_manager = Singleton(PlatformManager)
    name_generator = Singleton(NameGenerator)
    path_manager = Singleton(PathManager, platform_manager)
    temp_manager = Singleton(TempManager)
    module_manager = Singleton(ModuleManager, logger)
    general_storage = Singleton(Storage, file=GENERAL_CONFIG_PATH)
    credentials_storage = Singleton(Storage, file=CREDENTIALS_CONFIG_PATH)
    cache_storage = Singleton(Storage, file=CACHE_PATH)
    cli_config_manager = Singleton(CLIConfigManager, general_storage, credentials_storage)
    project_config_manager = Singleton(ProjectConfigManager, xml_manager)
    lean_config_manager = Singleton(LeanConfigManager,
                                    logger,
                                    cli_config_manager,
                                    project_config_manager,
                                    module_manager,
                                    cache_storage)

    output_config_manager = Singleton(OutputConfigManager, lean_config_manager)
    project_manager = Singleton(ProjectManager,
                                project_config_manager,
                                lean_config_manager,
                                xml_manager,
                                platform_manager)    
    data_manager = Singleton(DataManager, lean_config_manager, logger)
    lean_runner = Singleton(LeanRunner,
                            logger,
                            project_config_manager,
                            lean_config_manager,
                            output_config_manager,
                            module_manager,
                            project_manager,
                            temp_manager,
                            xml_manager)
container = Container()
