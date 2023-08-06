"""
Copyright 2021 Kelvin Inc.

Licensed under the Kelvin Inc. Developer SDK License Agreement (the "License"); you may not use
this file except in compliance with the License.  You may obtain a copy of the
License at

http://www.kelvininc.com/developer-sdk-license

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OF ANY KIND, either express or implied.  See the License for the
specific language governing permissions and limitations under the License.
"""

from types import MappingProxyType
from typing import Dict, List

from jinja2 import Environment, PackageLoader, Template

from kelvin.sdk.lib.configs.general_configs import GeneralConfigs
from kelvin.sdk.lib.models.apps.common import ApplicationLanguage
from kelvin.sdk.lib.models.apps.ksdk_app_configuration import ApplicationFlavour, ProjectType
from kelvin.sdk.lib.models.apps.ksdk_app_setup import File, TemplateFile
from kelvin.sdk.lib.models.generic import KPath
from kelvin.sdk.lib.models.types import EmbeddedFiles, FileType


def get_file_templates(
    file_type: FileType,
    project_type: ProjectType,
    app_flavour: ApplicationFlavour,
    kelvin_app_lang: ApplicationLanguage = None,
) -> List[TemplateFile]:
    """When provided with a programming language and file type, retrieve all of the respective templates.

    Parameters
    ----------
    file_type: FileType
        the type of templates to retrieve (either app templates or configuration templates).
    project_type: ProjectType
    app_flavour: ApplicationFlavour
    kelvin_app_lang: ApplicationLanguage, optional

    Returns
    -------
    List[TemplateFile]
        a list of TemplateFiles
    """

    if kelvin_app_lang:
        templates = (
            project_templates.get(project_type, {}).get(kelvin_app_lang, {}).get(app_flavour, {}).get(file_type, [])
        )
    else:
        templates = project_templates.get(project_type, {}).get(app_flavour, {}).get(file_type, [])

    return [
        TemplateFile(
            name=item.get("name"),
            content=retrieve_template(template_name=item.get("content", "")),
            options=item.get("options", {}),
        )
        for item in templates
    ]


def get_files_from_templates(directory: KPath, templates: List[TemplateFile], render_params: Dict) -> List[File]:
    """
    When provided with a directory, a list of templates and additional parameters, render the templates with the render
    parameters and create File objects with the associated directory.

    Parameters
    ----------
    directory: KPath
        the directory to associate to each new File object.
    templates: List[TemplateFile]
        the templates to render.
    render_params: Dict
        the parameters to render the templates with.
    Returns
    -------
    List[File]
        a list of File objects

    """
    files_return_result = []

    for template in templates:
        render_params = render_params or {}
        file_name = template.name.format_map(render_params) if render_params else template.name
        file_content = template.content.render(render_params)
        file_path = directory / file_name
        files_return_result.append(File(file=file_path, content=file_content, **template.options))

    return files_return_result


def get_embedded_file(embedded_file: EmbeddedFiles) -> Template:
    """
    When provided with an embedded app type and file type, retrieve all of the respective templates.

    Parameters
    ----------
    embedded_file : EmbeddedFiles
         the type of the embedded app to retrieve the templates from

    Returns
    -------
    Template
        a single Template object for the targeted file

    """
    template = _embedded_files.get(embedded_file, {})

    return retrieve_template(template_name=template)


def retrieve_template(template_name: str) -> Template:
    """
    Retrieve the Jinja2 Template with the specified template name (path).

    Parameters
    ----------
    template_name : str
        the name of the template to retrieve.

    Returns
    -------
    Template
        a Jinja2 template.

    """

    templates_package_loader = PackageLoader(package_name="kelvin.sdk.lib", package_path="templates")
    templates_environment = Environment(
        loader=templates_package_loader, trim_blocks=True, lstrip_blocks=True, autoescape=True
    )
    return templates_environment.get_template(name=template_name)


class Templates:
    files_default_dockerignore: str = "files/default_dockerignore.jinja2"
    files_default_empty_file: str = "files/default_empty_file.jinja2"
    files_default_datatype: str = "files/default_datatype_icd.jinja2"
    files_kelvin_python_app_ignore_file: str = "apps/kelvin/python/python_app_gitignore_file.jinja2"
    files_python_app_pyproject_file: str = "apps/python_app_pyproject_file.jinja2"
    files_python_app_dockerfile: str = "apps/python_app_dockerfile.jinja2"


project_templates: MappingProxyType = MappingProxyType(
    {
        ProjectType.kelvin: {
            ApplicationLanguage.python: {
                ApplicationFlavour.default: {
                    FileType.APP: [
                        {
                            "name": GeneralConfigs.default_python_init_file,
                            "content": "apps/kelvin/python/python_app_init_file.jinja2",
                        },
                        {
                            "name": "{app_file_system_name}{app_lang_extension}",
                            "content": "apps/kelvin/python/default/python_app_file.jinja2",
                        },
                    ],
                    FileType.CONFIGURATION: [
                        {
                            "name": GeneralConfigs.default_python_setup_file,
                            "content": "apps/kelvin/python/python_app_setup_file.jinja2",
                        },
                        {
                            "name": GeneralConfigs.default_requirements_file,
                            "content": "apps/kelvin/python/python_app_requirements_file.jinja2",
                        },
                        {
                            "name": GeneralConfigs.default_python_pyproject_file,
                            "content": Templates.files_python_app_pyproject_file,
                        },
                        {
                            "name": GeneralConfigs.default_git_ignore_file,
                            "content": "apps/kelvin/python/python_app_gitignore_file.jinja2",
                        },
                        {
                            "name": GeneralConfigs.default_dockerignore_file,
                            "content": Templates.files_default_dockerignore,
                        },
                    ],
                    FileType.BUILD: [],
                    FileType.DATA: [
                        {
                            "name": GeneralConfigs.default_git_keep_file,
                            "content": Templates.files_default_empty_file,
                        },
                    ],
                    FileType.DATATYPE: [
                        {
                            "name": GeneralConfigs.default_git_keep_file,
                            "content": Templates.files_default_empty_file,
                        },
                    ],
                    FileType.DOCS: [
                        {
                            "name": GeneralConfigs.default_git_keep_file,
                            "content": Templates.files_default_empty_file,
                        },
                    ],
                    FileType.TESTS: [
                        {
                            "name": GeneralConfigs.default_python_init_file,
                            "content": "apps/kelvin/python/python_app_init_file.jinja2",
                        },
                        {
                            "name": GeneralConfigs.default_python_test_file,
                            "content": "apps/kelvin/python/python_app_tests_file.jinja2",
                        },
                    ],
                    FileType.WHEELS: [
                        {
                            "name": GeneralConfigs.default_git_keep_file,
                            "content": Templates.files_default_empty_file,
                        },
                    ],
                },
                ApplicationFlavour.pubsub: {
                    FileType.APP: [
                        {
                            "name": GeneralConfigs.default_python_init_file,
                            "content": "apps/kelvin/python/pubsub/python_app_init_file.jinja2",
                        },
                        {
                            "name": GeneralConfigs.default_python_main_file,
                            "content": "apps/kelvin/python/pubsub/python_app__main__file.jinja2",
                        },
                        {
                            "name": "main.py",
                            "content": "apps/kelvin/python/pubsub/python_app_main_file.jinja2",
                        },
                        {
                            "name": "{app_file_system_name}{app_lang_extension}",
                            "content": "apps/kelvin/python/pubsub/python_app_file.jinja2",
                        },
                    ],
                    FileType.CONFIGURATION: [
                        {
                            "name": GeneralConfigs.default_python_setup_file,
                            "content": "apps/kelvin/python/python_app_setup_file.jinja2",
                        },
                        {
                            "name": GeneralConfigs.default_requirements_file,
                            "content": "apps/kelvin/python/python_app_requirements_file.jinja2",
                        },
                        {
                            "name": GeneralConfigs.default_python_pyproject_file,
                            "content": Templates.files_python_app_pyproject_file,
                        },
                        {
                            "name": GeneralConfigs.default_git_ignore_file,
                            "content": "apps/kelvin/python/python_app_gitignore_file.jinja2",
                        },
                        {
                            "name": GeneralConfigs.default_dockerignore_file,
                            "content": Templates.files_default_dockerignore,
                        },
                    ],
                },
            }
        },
        ProjectType.bridge: {
            ApplicationLanguage.python: {
                ApplicationFlavour.default: {
                    FileType.APP: [
                        {
                            "name": GeneralConfigs.default_python_init_file,
                            "content": "apps/bridge/python/python_app_init_file.jinja2",
                        },
                        {
                            "name": "{app_file_system_name}{app_lang_extension}",
                            "content": "apps/bridge/python/default/python_app_file.jinja2",
                        },
                    ],
                    FileType.CONFIGURATION: [
                        {
                            "name": GeneralConfigs.default_python_setup_file,
                            "content": "apps/bridge/python/python_app_setup_file.jinja2",
                        },
                        {
                            "name": GeneralConfigs.default_requirements_file,
                            "content": "apps/bridge/python/python_app_requirements_file.jinja2",
                        },
                        {
                            "name": GeneralConfigs.default_python_pyproject_file,
                            "content": Templates.files_python_app_pyproject_file,
                        },
                        {
                            "name": GeneralConfigs.default_git_ignore_file,
                            "content": "apps/bridge/python/python_app_gitignore_file.jinja2",
                        },
                        {
                            "name": GeneralConfigs.default_dockerignore_file,
                            "content": Templates.files_default_dockerignore,
                        },
                    ],
                    FileType.BUILD: [],
                    FileType.DATATYPE: [
                        {
                            "name": GeneralConfigs.default_git_keep_file,
                            "content": Templates.files_default_empty_file,
                        },
                    ],
                    FileType.WHEELS: [
                        {
                            "name": GeneralConfigs.default_git_keep_file,
                            "content": Templates.files_default_empty_file,
                        },
                    ],
                }
            }
        },
        ProjectType.docker: {
            ApplicationFlavour.default: {
                FileType.CONFIGURATION: [
                    {
                        "name": GeneralConfigs.default_dockerignore_file,
                        "content": Templates.files_default_dockerignore,
                    },
                    {
                        "name": GeneralConfigs.default_dockerfile,
                        "content": Templates.files_default_empty_file,
                    },
                ],
            }
        },
    },
)

_embedded_files: MappingProxyType = MappingProxyType(
    {
        EmbeddedFiles.EMPTY_FILE: Templates.files_default_empty_file,
        EmbeddedFiles.DOCKERIGNORE: Templates.files_default_dockerignore,
        EmbeddedFiles.DEFAULT_DATATYPE_TEMPLATE: Templates.files_default_datatype,
        EmbeddedFiles.KELVIN_PYTHON_APP_GITIGNORE: Templates.files_kelvin_python_app_ignore_file,
        EmbeddedFiles.KELVIN_PYTHON_APP_PYPROJECT: Templates.files_python_app_pyproject_file,
        EmbeddedFiles.KELVIN_PYTHON_APP_DOCKERFILE: Templates.files_python_app_dockerfile,
        EmbeddedFiles.BRIDGE_PYTHON_APP_DOCKERFILE: Templates.files_python_app_dockerfile,
    }
)
