from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from kelvin.sdk.lib.configs.general_configs import GeneralConfigs
from kelvin.sdk.lib.models.apps.ksdk_app_configuration import ApplicationFlavour
from kelvin.sdk.lib.models.apps.ksdk_app_setup import Directory
from kelvin.sdk.lib.models.factories.project.kelvin import KelvinProject
from kelvin.sdk.lib.models.factories.project.project import ProjectFileTree
from kelvin.sdk.lib.models.generic import KPath
from kelvin.sdk.lib.models.types import FileType


class ProjectBridgeAppFileTree(ProjectFileTree):
    app: Optional[Directory]
    build: Optional[Directory]
    datatype: Optional[Directory]
    wheels: Optional[Directory]

    @staticmethod
    def get_tree_dict(app_root: KPath, **kwargs: Any) -> Dict:
        build_dir_path = app_root / GeneralConfigs.default_build_dir
        datatype_dir_path: KPath = app_root / GeneralConfigs.default_datatype_dir
        wheels_dir_path = app_root / GeneralConfigs.default_wheels_dir

        return {
            FileType.ROOT.value: {"file_type": FileType.CONFIGURATION, "directory": app_root},
            FileType.APP.value: {"file_type": FileType.APP, "directory": kwargs.get("app_source")},
            FileType.BUILD.value: {"file_type": None, "directory": build_dir_path},
            FileType.DATATYPE.value: {"file_type": FileType.DATATYPE, "directory": datatype_dir_path},
            FileType.WHEELS.value: {"file_type": FileType.WHEELS, "directory": wheels_dir_path},
        }

    def fundamental_dirs(self) -> List[Directory]:
        return [self.root]

    def optional_dirs(self) -> List[Directory]:
        return [
            directory
            for directory in [
                self.app,
                self.build,
                self.datatype,
                self.wheels,
            ]
            if directory
        ]


@dataclass
class BridgeProject(KelvinProject):
    flavour_registry: Any = field(default_factory=lambda: {ApplicationFlavour.default: ProjectBridgeAppFileTree})
