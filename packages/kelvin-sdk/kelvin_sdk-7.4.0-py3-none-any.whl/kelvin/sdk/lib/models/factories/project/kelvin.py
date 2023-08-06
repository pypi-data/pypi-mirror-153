import pathlib
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from kelvin.sdk.lib.configs.general_configs import GeneralConfigs
from kelvin.sdk.lib.models.apps.ksdk_app_configuration import ApplicationFlavour
from kelvin.sdk.lib.models.apps.ksdk_app_setup import Directory
from kelvin.sdk.lib.models.factories.project.project import ProjectBase, ProjectFileTree
from kelvin.sdk.lib.models.generic import KPath
from kelvin.sdk.lib.models.types import FileType
from kelvin.sdk.lib.utils.general_utils import camel_name, standardize_string


class ProjectKelvinAppFileTree(ProjectFileTree):
    app: Optional[Directory]
    build: Optional[Directory]
    data: Optional[Directory]
    datatype: Optional[Directory]
    docs: Optional[Directory]
    tests: Optional[Directory]
    wheels: Optional[Directory]

    @staticmethod
    def get_tree_dict(app_root: KPath, **kwargs: Any) -> Dict:
        build_dir_path = app_root / GeneralConfigs.default_build_dir
        data_dir_path: KPath = app_root / GeneralConfigs.default_data_dir
        datatype_dir_path: KPath = app_root / GeneralConfigs.default_datatype_dir
        docs_dir_path = app_root / GeneralConfigs.default_docs_dir
        tests_dir_path = app_root / GeneralConfigs.default_tests_dir
        wheels_dir_path = app_root / GeneralConfigs.default_wheels_dir

        return {
            FileType.ROOT.value: {"file_type": FileType.CONFIGURATION, "directory": app_root},
            FileType.APP.value: {"file_type": FileType.APP, "directory": kwargs.get("app_source")},
            FileType.BUILD.value: {"file_type": None, "directory": build_dir_path},
            FileType.DATA.value: {"file_type": FileType.DATA, "directory": data_dir_path},
            FileType.DATATYPE.value: {"file_type": FileType.DATATYPE, "directory": datatype_dir_path},
            FileType.DOCS.value: {"file_type": FileType.DOCS, "directory": docs_dir_path},
            FileType.TESTS.value: {"file_type": FileType.TESTS, "directory": tests_dir_path},
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
                self.data,
                self.datatype,
                self.docs,
                self.tests,
                self.wheels,
            ]
            if directory
        ]


@dataclass
class KelvinProject(ProjectBase):
    flavour_registry: Any = field(
        default_factory=lambda: {
            ApplicationFlavour.default: ProjectKelvinAppFileTree,
            ApplicationFlavour.pubsub: ProjectKelvinAppFileTree,
        }
    )

    def get_template_parameters(self) -> Dict:
        """Dict used to fill the templates

        Returns
        -------
        Dict
            A dictionary containing the required parameters to fill the project templates
        """
        app_name = self.creation_parameters.app_name
        dir_path = self.creation_parameters.app_dir
        app_type = self.creation_parameters.app_type
        app_flavour = self.creation_parameters.app_flavour
        kelvin_app_lang = self.creation_parameters.kelvin_app_lang

        app_config_file = GeneralConfigs.default_app_config_file
        app_file_system_name = standardize_string(value=app_name)
        class_name = camel_name(app_name)

        app_root_dir_path: KPath = KPath(dir_path) / app_name
        app_source_dir_path: KPath = app_root_dir_path / app_file_system_name
        app_file_path: KPath = app_source_dir_path / f"{app_file_system_name}{kelvin_app_lang.get_extension()}"

        relative_source_app_file_path: KPath = app_file_path.relative_to(app_root_dir_path)
        app_entry_point = str(pathlib.PurePosixPath(relative_source_app_file_path))

        # 1 - Configuration files, app dir and files
        parameters: dict = {
            "app_root": app_root_dir_path,
            "app_source": app_source_dir_path,
            "app_name": app_name,
            "app_title": app_name,
            "app_lang": kelvin_app_lang.value,
            "app_description": GeneralConfigs.default_app_description,
            "app_version": GeneralConfigs.default_app_version,
            "app_file_system_name": app_file_system_name,
            "app_lang_extension": kelvin_app_lang.get_extension(),
            "app_type": app_type.value,
            "app_flavour": app_flavour.value,
            "kelvin_app_lang": kelvin_app_lang.value,
            "app_entry_point": app_entry_point,
            "app_config_file": app_config_file,
            "class_name": class_name,
        }

        return parameters

    def _build_file_tree(self) -> ProjectFileTree:
        parameters = self.get_template_parameters()
        app_root_dir_path = parameters.get("app_root", "")
        app_source_dir_path = parameters.get("app_source", "")
        app_config_file = parameters.get("app_config_file", "")

        project_file_tree_class = self.get_flavour_class()

        # directory file tree required for a docker project
        project_type = self.creation_parameters.app_type
        kelvin_app_lang = self.creation_parameters.kelvin_app_lang
        kelvin_app_flavour = self.creation_parameters.app_flavour

        file_tree: ProjectFileTree = project_file_tree_class.from_tree(
            app_root=app_root_dir_path,
            app_source=app_source_dir_path,
            template_parameters=parameters,
            project_type=project_type,
            kelvin_app_lang=kelvin_app_lang,
            kelvin_app_flavour=kelvin_app_flavour,
        )

        # append app config file
        app_config_file_path: KPath = app_root_dir_path / app_config_file
        file = self._build_app_config_file(app_config_file_path=app_config_file_path)
        file_tree.root.files.append(file)

        return file_tree
