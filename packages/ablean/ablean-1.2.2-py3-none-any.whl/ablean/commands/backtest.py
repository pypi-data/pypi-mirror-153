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

import os
import sys
import platform
import json5
from pathlib import Path
from datetime import datetime
from pathlib import Path
from typing import Optional

import click
from ablean.components.config.storage import Storage

from ablean.myclick import LeanCommand, PathParameter
from ablean.constants import DEFAULT_ENGINE_IMAGE
from ablean.container import container
from ablean.models.utils import DebuggingMethod
from ablean.models.pydantic import Option

def fix_ptvsd_signal_error():    
    if platform.system() == 'Windows':
        return
    for s in sys.path:
        if not s.endswith('site-packages'):
            continue
        file = Path(os.path.join(s, 'ptvsd', 'exit_handlers.py'))
        if not file.exists():
            continue
        content = file.read_text()
        if "# self._install_signal_handler()" in content:
            return
        content = content.replace("self._install_signal_handler()", "# self._install_signal_handler()")
        file.write_text(content, encoding='utf-8')
        return
            


# The _migrate_* methods automatically update launch configurations for a given debugging method.
#
# Occasionally we make changes which require updated launch configurations.
# Projects which are created after these update have the correct configuration already,
# but projects created before that need changes.
#
# These methods checks if the project has outdated configurations, and if so, update them to keep it working.


def _migrate_python_pycharm(project_dir: Path) -> None:
    workspace_xml_path = project_dir / ".idea" / "workspace.xml"
    if not workspace_xml_path.is_file():
        return

    xml_manager = container.xml_manager()
    current_content = xml_manager.parse(workspace_xml_path.read_text(encoding="utf-8"))

    config = current_content.find('.//configuration[@name="Debug with Lean CLI"]')
    if config is None:
        return

    path_mappings = config.find(
        './/PathMappingSettings/option[@name="pathMappings"]/list'
    )
    if path_mappings is None:
        return

    made_changes = False
    has_library_mapping = False

    library_dir = container.lean_config_manager().get_cli_root_directory() / "Library"
    if library_dir.is_dir():
        library_dir = (
            f"$PROJECT_DIR$/{os.path.relpath(library_dir, project_dir)}".replace(
                "\\", "/"
            )
        )
    else:
        library_dir = None

    for mapping in path_mappings.findall(".//mapping"):
        if (
            mapping.get("local-root") == "$PROJECT_DIR$"
            and mapping.get("remote-root") == "/Lean/Launcher/bin/Debug"
        ):
            mapping.set("remote-root", "/LeanCLI")
            made_changes = True

        if (
            library_dir is not None
            and mapping.get("local-root") == library_dir
            and mapping.get("remote-root") == "/Library"
        ):
            has_library_mapping = True

    if library_dir is not None and not has_library_mapping:
        library_mapping = xml_manager.parse("<mapping/>")
        library_mapping.set("local-root", library_dir)
        library_mapping.set("remote-root", "/Library")
        path_mappings.append(library_mapping)
        made_changes = True

    if made_changes:
        workspace_xml_path.write_text(
            xml_manager.to_string(current_content), encoding="utf-8"
        )

        logger = container.logger()
        logger.warn(
            "Your run configuration has been updated to work with the latest version of LEAN"
        )
        logger.warn("Please restart the debugger in PyCharm and run this command again")

        raise click.Abort()


def _migrate_python_vscode(project_dir: Path) -> None:
    launch_json_path = project_dir / ".vscode" / "launch.json"
    if not launch_json_path.is_file():
        return

    current_content = json5.loads(launch_json_path.read_text(encoding="utf-8"))
    if "configurations" not in current_content or not isinstance(
        current_content["configurations"], list
    ):
        return

    config = next(
        (
            c
            for c in current_content["configurations"]
            if c["name"] == "Debug with Lean CLI"
        ),
        None,
    )
    if config is None:
        return

    made_changes = False
    has_library_mapping = False

    library_dir = container.lean_config_manager().get_cli_root_directory() / "Library"
    if not library_dir.is_dir():
        library_dir = None

    for mapping in config["pathMappings"]:
        if (
            mapping["localRoot"] == "${workspaceFolder}"
            and mapping["remoteRoot"] == "/Lean/Launcher/bin/Debug"
        ):
            mapping["remoteRoot"] = "/LeanCLI"
            made_changes = True

        if (
            library_dir is not None
            and mapping["localRoot"] == str(library_dir)
            and mapping["remoteRoot"] == "/Library"
        ):
            has_library_mapping = True

    if library_dir is not None and not has_library_mapping:
        config["pathMappings"].append(
            {"localRoot": str(library_dir), "remoteRoot": "/Library"}
        )
        made_changes = True

    if made_changes:
        launch_json_path.write_text(
            json5.dumps(current_content, indent=4), encoding="utf-8"
        )


def _migrate_csharp_rider(project_dir: Path) -> None:
    made_changes = False
    xml_manager = container.xml_manager()

    for dir_name in [f".idea.{project_dir.stem}", f".idea.{project_dir.stem}.dir"]:
        workspace_xml_path = (
            project_dir / ".idea" / dir_name / ".idea" / "workspace.xml"
        )
        if not workspace_xml_path.is_file():
            continue

        current_content = xml_manager.parse(
            workspace_xml_path.read_text(encoding="utf-8")
        )

        run_manager = current_content.find(".//component[@name='RunManager']")
        if run_manager is None:
            continue

        config = run_manager.find(".//configuration[@name='Debug with Lean CLI']")
        if config is None:
            continue

        run_manager.remove(config)

        workspace_xml_path.write_text(
            xml_manager.to_string(current_content), encoding="utf-8"
        )
        made_changes = True

    if made_changes:
        container.project_manager().generate_rider_config()

        logger = container.logger()
        logger.warn(
            "Your run configuration has been updated to work with the .NET 5 version of LEAN"
        )
        logger.warn("Please restart Rider and start debugging again")
        logger.warn(
            "See https://www.lean.io/docs/lean-cli/backtesting/debugging#05-C-and-Rider for the updated instructions"
        )

        raise click.Abort()


def _migrate_csharp_vscode(project_dir: Path) -> None:
    launch_json_path = project_dir / ".vscode" / "launch.json"
    if not launch_json_path.is_file():
        return

    current_content = json.loads(launch_json_path.read_text(encoding="utf-8"))
    if "configurations" not in current_content or not isinstance(
        current_content["configurations"], list
    ):
        return

    config = next(
        (
            c
            for c in current_content["configurations"]
            if c["name"] == "Debug with Lean CLI"
        ),
        None,
    )
    if config is None:
        return

    if (
        config["type"] != "mono"
        and config["processId"] != "${command:pickRemoteProcess}"
    ):
        return

    config.pop("address", None)
    config.pop("port", None)

    config["type"] = "coreclr"
    config["processId"] = "1"

    config["pipeTransport"] = {
        "pipeCwd": "${workspaceRoot}",
        "pipeProgram": "docker",
        "pipeArgs": ["exec", "-i", "lean_cli_vsdbg"],
        "debuggerPath": "/root/vsdbg/vsdbg",
        "quoteArgs": False,
    }

    config["logging"] = {"moduleLoad": False}

    launch_json_path.write_text(json.dumps(current_content, indent=4), encoding="utf-8")


def _migrate_csharp_csproj(project_dir: Path) -> None:
    csproj_path = next((f for f in project_dir.rglob("*.csproj")), None)
    if csproj_path is None:
        return

    xml_manager = container.xml_manager()

    current_content = xml_manager.parse(csproj_path.read_text(encoding="utf-8"))
    if current_content.find(".//PropertyGroup/DefaultItemExcludes") is not None:
        return

    property_group = current_content.find(".//PropertyGroup")
    if property_group is None:
        property_group = xml_manager.parse("<PropertyGroup/>")
        current_content.append(property_group)

    default_item_excludes = xml_manager.parse(
        "<DefaultItemExcludes>$(DefaultItemExcludes);backtests/*/code/**;live/*/code/**;optimizations/*/code/**</DefaultItemExcludes>"
    )
    property_group.append(default_item_excludes)

    csproj_path.write_text(xml_manager.to_string(current_content), encoding="utf-8")


@click.command(cls=LeanCommand, requires_lean_config=True)
@click.argument(
    "project", type=PathParameter(exists=True, file_okay=True, dir_okay=True)
)
@click.option(
    "--config",
    type=PathParameter(exists=True, file_okay=True, dir_okay=False),
    help="用户指定的策略配置文件",
)
@click.option(
    "--output",
    type=PathParameter(exists=False, file_okay=False, dir_okay=True),
    help="Directory to store results in (defaults to PROJECT/backtests/TIMESTAMP)",
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Enable debugger",
)
@click.option(
    "--download-data",
    is_flag=True,
    default=False,
    help="Update the backtest data",
)
def backtest(
    project: Path,
    config: Optional[Path],
    output: Optional[Path],
    debug: bool,
    download_data: bool,
) -> None:
    """Backtest a project locally.

    \b
    If PROJECT is a directory, the algorithm in the main.py or Main.cs file inside it will be executed.
    If PROJECT is a file, the algorithm in the specified file will be executed.

    \b
    Go to the following url to learn how to debug backtests locally using the Lean CLI:
    https://www.lean.io/docs/lean-cli/backtesting/debugging

    By default the official LEAN engine image is used.
    You can override this using the --image option.
    Alternatively you can set the default engine image for all commands using `lean config set engine-image <image>`.
    """
    project_manager = container.project_manager()
    algorithm_file = project_manager.find_algorithm_file(Path(project))
    lean_config_manager = container.lean_config_manager()

    if output is None:
        output = (
            algorithm_file.parent
            / "backtests"
            / datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        )

    if not output.exists():
        output.mkdir(parents=True)

    debugging_method = None
    if debug:
        debugging_method = DebuggingMethod.PTVSD
        fix_ptvsd_signal_error()
        # _migrate_python_vscode(algorithm_file.parent)

    lean_config = lean_config_manager.get_complete_lean_config(
        "backtesting", algorithm_file, output, debugging_method
    )

    if config is not None:
        for k, v in Storage(str(config)).data.items():
            lean_config[k] = v

    if download_data:
        container.data_manager().update_data()

    output_config_manager = container.output_config_manager()
    lean_config["algorithm-id"] = str(output_config_manager.get_backtest_id(output))

    lean_runner = container.lean_runner()
    lean_runner.run_lean(lean_config, "backtesting", algorithm_file, output)
