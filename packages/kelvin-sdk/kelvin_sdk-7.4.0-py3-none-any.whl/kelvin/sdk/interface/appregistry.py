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

from typeguard import typechecked

from kelvin.sdk.lib.models.operation import OperationResponse


@typechecked
def appregistry_list(should_display: bool = False) -> OperationResponse:
    """
    Returns the list of apps on the registry.

    Parameters
    ----------
    should_display: bool
        specifies whether or not the display should output data.

    Returns
    ----------
    kelvin.sdk.lib.models.operation.OperationResponse
        an OperationResponse object encapsulating the Applications available on the platform.

    """
    from kelvin.sdk.lib.api.appregistry import appregistry_list as _appregistry_list

    return _appregistry_list(query=None, should_display=should_display)


@typechecked
def appregistry_search(query: str, should_display: bool = False) -> OperationResponse:
    """
    Search for apps on the registry that match the provided query.

    Parameters
    ----------
    query: str
        the query to search for.
    should_display: bool
        specifies whether or not the display should output data.

    Returns
    ----------
    kelvin.sdk.lib.models.operation.OperationResponse
        an OperationResponse object encapsulating the matching Applications available on the platform.

    """
    from kelvin.sdk.lib.api.appregistry import appregistry_list as _appregistry_list

    return _appregistry_list(query=query, should_display=should_display)


@typechecked
def appregistry_show(app_name: str, should_display: bool = False) -> OperationResponse:
    """
    Returns detailed information on the specified application.

    Parameters
    ----------
    app_name: str
        the name with version of the app.
    should_display: bool
        specifies whether or not the display should output data.

    Returns
    ----------
    kelvin.sdk.lib.models.operation.OperationResponse
        an OperationResponse object encapsulating the yielded Application instance and its data.

    """
    from kelvin.sdk.lib.api.appregistry import appregistry_show as _appregistry_show

    return _appregistry_show(app_name=app_name, should_display=should_display)


@typechecked
def appregistry_upload(app_dir: str, upload_datatypes: bool = False) -> OperationResponse:
    """
    Uploads the specified application to the platform.

    - Packages the app
    - Pushes the app to the docker registry
    - Publishes the app on the appregistry endpoint.

    Parameters
    ----------
    app_dir: str
        the path to the application's dir.
    upload_datatypes: bool
        If specified, will upload locally defined data types.

    Returns
    ----------
    kelvin.sdk.lib.models.operation.OperationResponse
        an OperationResponse object encapsulating the result of the upload operation.

    """
    from kelvin.sdk.lib.api.appregistry import appregistry_upload as _appregistry_upload

    return _appregistry_upload(app_dir_path=app_dir, upload_datatypes=upload_datatypes)


@typechecked
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
    kelvin.sdk.lib.models.operation.OperationResponse
        an OperationResponse object encapsulating the result of the app download operation.

    """
    from kelvin.sdk.lib.api.appregistry import appregistry_download as _appregistry_download

    return _appregistry_download(app_name_with_version=app_name_with_version, override_local_tag=override_local_tag)


@typechecked
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
    kelvin.sdk.lib.models.operation.OperationResponse
        an OperationResponse object encapsulating the result of the app deletion operation.

    """
    from kelvin.sdk.lib.api.appregistry import appregistry_delete as _appregistry_delete

    return _appregistry_delete(
        app_name_with_version=app_name_with_version, ignore_destructive_warning=ignore_destructive_warning
    )
