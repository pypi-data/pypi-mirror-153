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

from pathlib import Path
from typing import Set, List, Dict

from ablean.components.util.logger import Logger
from ablean.constants import MODULES_DIRECTORY
from ablean.models.modules import NuGetPackage


class ModuleManager:
    """The ModuleManager class is responsible for downloading and updating modules."""

    def __init__(self, logger: Logger) -> None:
        """Creates a new ModuleManager instance.

        :param logger: the logger to use
        :param api_client: the APIClient instance to use when communicating with the cloud
        :param http_client: the HTTPClient instance to use when downloading modules
        """
        self._logger = logger
        self._installed_product_ids: Set[int] = set()
        self._installed_packages: Dict[int, List[NuGetPackage]] = {}

    def get_installed_packages(self) -> List[NuGetPackage]:
        """Returns a list of NuGet packages that were installed by install_module() calls.

        :return: a list of NuGet packages in the modules directory that should be made available when running LEAN
        """
        packages = []
        for package_list in self._installed_packages.values():
            packages.extend(package_list)
        return packages

    def get_installed_packages_by_module(self, product_id: int) -> List[NuGetPackage]:
        """Returns a list of NuGet packages that were installed by install_module() for a given product id.

        :param product_id: the product id to get the installed packages of
        :return: a list of NuGet packages in are available for the given product id
        """
        return self._installed_packages.get(product_id, []).copy()

    def is_module_installed(self, product_id: int) -> bool:
        """Returns whether a module with a given producti d has been installed with install_module().

        :param product_id: the product id to check the install status of
        :return: True if the product id has been registered with install_module(), False if not
        """
        return product_id in self._installed_product_ids
