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

from typing import Any, List, Optional, cast

from kelvin.sdk.client.error import APIError
from kelvin.sdk.client.model.requests import AppCreate
from kelvin.sdk.lib.api.workload import retrieve_workload_and_workload_status_data
from kelvin.sdk.lib.apps.local_apps_manager import project_build
from kelvin.sdk.lib.configs.general_configs import GeneralConfigs
from kelvin.sdk.lib.exceptions import AppException
from kelvin.sdk.lib.models.apps.ksdk_app_configuration import KelvinAppConfiguration
from kelvin.sdk.lib.models.factories.app_setup_configuration_objects_factory import get_default_app_configuration
from kelvin.sdk.lib.models.factories.docker_manager_factory import get_docker_manager
from kelvin.sdk.lib.models.generic import KPath
from kelvin.sdk.lib.models.ksdk_docker import DockerImageName
from kelvin.sdk.lib.models.operation import OperationResponse
from kelvin.sdk.lib.session.session_manager import session_manager
from kelvin.sdk.lib.utils.display_utils import (
    DisplayObject,
    display_data_entries,
    display_data_object,
    display_yes_or_no_question,
)
from kelvin.sdk.lib.utils.exception_utils import retrieve_error_message_from_api_exception
from kelvin.sdk.lib.utils.logger_utils import logger


def appregistry_list(query: Optional[str] = None, should_display: bool = False) -> OperationResponse:
    """
    Search for apps on the registry that match the provided query.

    Parameters
    ----------
    query: Optional[str]
        the query to search for.
    should_display: bool
        specifies whether or not the display should output data.

    Returns
    ----------
    OperationResponse
        an OperationResponse object encapsulating the matching Applications available on the platform.

    """
    try:
        appregistry_list_step_1 = "Retrieving applications.."
        if query:
            appregistry_list_step_1 = f'Searching applications that match "{query}"'

        logger.info(appregistry_list_step_1)

        display_obj: DisplayObject = retrieve_appregistry_data(query=query, should_display=should_display)

        return OperationResponse(success=True, data=display_obj.parsed_data)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error retrieving applications: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error retrieving applications: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def appregistry_show(app_name: str, should_display: bool = False) -> OperationResponse:
    """
    Returns detailed information on the specified application.

    Parameters
    ----------
    app_name: str
        the name with version of the application.
    should_display: bool
        specifies whether or not the display should output data.

    Returns
    ----------
    OperationResponse
        an OperationResponse object encapsulating the yielded application instance and its data.

    """
    try:
        application_name = DockerImageName.parse(name=app_name)

        app_data: Any
        app_version_display: Optional[DisplayObject] = None
        app_info_table_title: str = GeneralConfigs.table_title.format(title="Application info")

        client = session_manager.login_client_on_current_url()

        if application_name.version:
            params = application_name.dict()
            logger.info('Retrieving details for version "{version}" of "{name}"'.format_map(params))
            app_data = client.app.get_app_version(app_name=application_name.name, app_version=application_name.version)
            app_data_display_object = display_data_object(
                data=app_data, should_display=False, object_title=app_info_table_title
            )
            data_to_display = app_data_display_object.tabulated_data
        else:
            logger.info(f'Retrieving details for "{application_name.name}"')
            app_data = client.app.get_app(app_name=application_name.name)
            app_data_without_version = app_data.copy(exclude={"versions"})
            app_data_display_object = display_data_object(
                data=app_data_without_version, should_display=False, object_title=app_info_table_title
            )
            data_to_display = app_data_display_object.tabulated_data

            # Display App Versions
            if app_data and app_data.versions:
                app_version_display = display_data_entries(
                    data=app_data.versions,
                    header_names=["Version", "Updated"],
                    attributes=["version", "updated"],
                    table_title=GeneralConfigs.table_title.format(title="Application versions"),
                    should_display=False,
                )
                data_to_display += "\n" + app_version_display.tabulated_data

        # Retrieve workload data for display
        logger.info(f'Retrieving workloads for "{application_name.name}"')
        workload_display = retrieve_workload_and_workload_status_data(
            app_name=application_name.name, app_version=application_name.version, should_display=False
        )
        if should_display:
            logger.info(f"{data_to_display}\n{workload_display.tabulated_data}")

        complete_app_info = {"app": app_data_display_object.parsed_data, "app_workloads": workload_display.parsed_data}
        if app_version_display:
            complete_app_info["app_versions"] = app_version_display.parsed_data

        return OperationResponse(success=True, data=complete_app_info)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error showing application: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error showing application: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def appregistry_delete(app_name_with_version: str, ignore_destructive_warning: bool = False) -> OperationResponse:
    """
    Deletes the specified application the platform's app registry.

    Parameters
    ----------
    app_name_with_version: str
        the name with version of the app to be deleted.
    ignore_destructive_warning: bool
        indicates whether it should ignore the destructive warning.

    Returns
    ----------
    OperationResponse
        an OperationResponse object encapsulating the result of the app deletion operation.

    """
    try:
        application_name = DockerImageName.parse(name=app_name_with_version)

        if application_name.version:
            if not ignore_destructive_warning:
                delete_app_version_prompt: str = """
                    This operation will delete version \"{version}\" of the application \"{name}\".
                    This will also delete ALL workloads and local data associated with this version of the application.

                """.format_map(
                    application_name.dict()
                )
                ignore_destructive_warning = display_yes_or_no_question(delete_app_version_prompt)
            if ignore_destructive_warning:
                params = application_name.dict()
                logger.info('Deleting version "{version}" of the application "{name}"'.format_map(params))
                client = session_manager.login_client_on_current_url()
                client.app.delete_app_version(app_name=application_name.name, app_version=application_name.version)
                logger.relevant('Version "{version}" of "{name}" successfully deleted'.format_map(params))
        else:
            if not ignore_destructive_warning:
                appregistry_delete_all_confirmation: str = f"""
                    This operation will delete ALL versions of the application \"{application_name.name}\".
                    This will also delete ALL workloads associated with this application.

                """
                ignore_destructive_warning = display_yes_or_no_question(appregistry_delete_all_confirmation)
            if ignore_destructive_warning:
                logger.info(f'Deleting application: "{application_name.name}"')
                client = session_manager.login_client_on_current_url()
                client.app.delete_app(app_name=application_name.name)
                logger.relevant(f'Application successfully deleted: "{application_name.name}"')

        success_message = f'Application successfully deleted: "{application_name.name}"'
        return OperationResponse(success=True, log=success_message)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error deleting application: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error retrieving application: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def appregistry_upload(app_dir_path: str, upload_datatypes: bool = False) -> OperationResponse:
    """
    Uploads the specified application to the platform.

    - Packages the app
    - Pushes the app to the docker registry
    - Publishes the app on the appregistry endpoint.

    Parameters
    ----------
    app_dir_path: str
        the path to the application's dir.
    upload_datatypes: bool
        If specified, will upload locally defined data types.

    Returns
    ----------
    OperationResponse
        an OperationResponse object encapsulating the result of the upload operation.

    """
    try:
        logger.info(f'Uploading application from path: "{KPath(app_dir_path).absolute()}"')

        # 1 - Get all the necessary credentials registry credentials
        user_credentials = session_manager.get_docker_credentials_for_current_url()
        docker_registry_url = user_credentials.full_registry_url

        # 2 - Load App-level configurations
        default_app_yaml = GeneralConfigs.default_app_config_file
        app_config_file_path: KPath = KPath(app_dir_path) / default_app_yaml
        app_config: KelvinAppConfiguration = get_default_app_configuration(app_config_file_path=app_config_file_path)

        docker_image_name = app_config.info.app_name_with_version
        app_name = app_config.info.name
        app_version = app_config.info.version
        client = session_manager.login_client_on_current_url()

        # 3 - Check if the application already exists
        app_version_already_exists = True
        try:
            client.app.get_app_version(app_name=app_name, app_version=app_version)
        except APIError as exc:
            for error in exc.errors:
                if error.http_status_code == 404:
                    app_version_already_exists = False
                    break
        if app_version_already_exists:
            raise AppException(message="The application version you're providing already exists")

        # 4 - Build the application
        app_successfully_packaged = project_build(
            app_dir=app_dir_path, build_for_upload=True, upload_datatypes=upload_datatypes
        )

        if not app_successfully_packaged.success:
            raise AppException(app_successfully_packaged.log)

        # 5 - Push the application to the appregistry
        docker_manager = get_docker_manager()
        logger.info(f'Pushing application content to "{docker_registry_url}"')
        push_was_successful = docker_manager.push_docker_image_to_registry(docker_image_name=docker_image_name)
        if not push_was_successful:
            raise AppException(f'Error pushing application "{docker_image_name}" to "{docker_registry_url}"')
        logger.relevant(f'Application "{docker_image_name}" successfully pushed to registry "{docker_registry_url}"')

        # 6 - Create the application on the app endpoint
        app_create_request: AppCreate = AppCreate(payload=app_config_file_path.read_yaml())
        newly_created_app = client.app.create_app(data=app_create_request)
        appregistry_upload_success: str = f"""\n
            Application successfully uploaded:
                Name: {app_name}
                Version: {app_version}

            To deploy this application version, run the following command:
                    kelvin workload deploy --app-name {app_name}:{app_version}
        """
        logger.relevant(appregistry_upload_success)

        return OperationResponse(success=True, data=newly_created_app, log=appregistry_upload_success)

    except APIError as exc:
        api_error = retrieve_error_message_from_api_exception(api_error=exc)
        api_error_message = f"Error uploading application: {api_error}"
        logger.error(api_error_message)
        return OperationResponse(success=False, log=api_error_message)

    except Exception as exc:
        error_message = f"Error uploading application: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def appregistry_download(app_name_with_version: str, override_local_tag: bool = False) -> OperationResponse:
    """
    Downloads the specified application from the platform's app registry.

    Parameters
    ----------
    app_name_with_version: str
        the app with version to be downloaded.
    override_local_tag: bool
        specifies whether or not it should override the local tag.

    Returns
    ----------
    OperationResponse
        an OperationResponse object encapsulating the result of the app download operation.

    """
    try:
        application_name = DockerImageName.parse(name=app_name_with_version)

        logger.info(f'Downloading application "{application_name.repository_image_name}"')

        docker_manager = get_docker_manager()

        downloaded_image: str = docker_manager.pull_docker_image_from_registry(
            docker_image_name=application_name.name_with_version,
            auth_config=docker_manager.logged_credentials(),
            override_local_tag=override_local_tag,
        )
        logger.relevant("Use `kelvin app images unpack` to extract its contents")

        success_message: str = f'"{downloaded_image}" successfully downloaded to the local registry.'
        return OperationResponse(success=True, log=success_message)

    except Exception as exc:
        error_message = f"Error downloading application: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


def retrieve_appregistry_data(query: Optional[str] = None, should_display: bool = True) -> DisplayObject:
    """
    Centralize the call to list applications.
    Retrieve all applications that match the provided criteria and yield the result.

    Parameters
    ----------
    query: Optional[str]
        the query to search specific applications.
    should_display: bool
        if specified, will display the results of this retrieve operation.

    Returns
    -------
    DisplayObject
        a DisplayObject containing the applications.

    """
    client = session_manager.login_client_on_current_url()

    yielded_applications = cast(List, client.app.list_apps(search=query)) or []

    return display_data_entries(
        data=yielded_applications,
        header_names=["Name", "Title", "Type", "Latest Version", "Updated"],
        attributes=["name", "title", "type", "latest_version", "updated"],
        table_title=GeneralConfigs.table_title.format(title="Applications"),
        should_display=should_display,
        no_data_message="No applications available",
    )
