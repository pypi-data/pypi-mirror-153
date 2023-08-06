from typing import Any, Dict

from kelvin.sdk.lib.models.apps.ksdk_app_configuration import ProjectType
from kelvin.sdk.lib.models.apps.ksdk_app_setup import ProjectCreationParametersObject
from kelvin.sdk.lib.models.factories.project.bridge import BridgeProject
from kelvin.sdk.lib.models.factories.project.docker import DockerProject
from kelvin.sdk.lib.models.factories.project.kelvin import KelvinProject
from kelvin.sdk.lib.models.factories.project.project import ProjectBase


class ProjectFactory:
    """The factory class for creating projects"""

    registry: Dict[ProjectType, Any] = {
        ProjectType.kelvin: KelvinProject,
        ProjectType.bridge: BridgeProject,
        ProjectType.docker: DockerProject,
    }

    @classmethod
    def create_project(cls, project_creation_parameters: ProjectCreationParametersObject, **kwargs: Any) -> ProjectBase:
        """Factory command to create the project instance"""

        project_class = cls.registry[project_creation_parameters.app_type]
        project: ProjectBase = project_class(project_creation_parameters, **kwargs)
        return project
