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

from typing import Dict, Generator, List, Optional, Tuple

from kelvin.sdk.lib.api.datatype import datatype_download, datatype_list, datatype_upload
from kelvin.sdk.lib.configs.datatype_configs import DataTypeConfigs
from kelvin.sdk.lib.configs.general_configs import GeneralConfigs
from kelvin.sdk.lib.exceptions import DataTypeException
from kelvin.sdk.lib.models.apps.kelvin_app import DataType
from kelvin.sdk.lib.models.apps.ksdk_app_configuration import KelvinAppConfiguration
from kelvin.sdk.lib.models.apps.ksdk_app_setup import KelvinAppBuildingObject
from kelvin.sdk.lib.models.datatypes import ICDPayloadHelper
from kelvin.sdk.lib.models.factories.app_setup_configuration_objects_factory import get_project_building_object
from kelvin.sdk.lib.models.generic import KPath
from kelvin.sdk.lib.models.ksdk_docker import DockerImageName
from kelvin.sdk.lib.models.operation import OperationResponse
from kelvin.sdk.lib.models.types import EmbeddedFiles
from kelvin.sdk.lib.templates.templates_manager import get_embedded_file
from kelvin.sdk.lib.utils.datatype_utils import (
    check_if_datatype_name_is_valid,
    check_if_datatype_name_with_version_is_valid,
)
from kelvin.sdk.lib.utils.display_utils import display_yes_or_no_question
from kelvin.sdk.lib.utils.general_utils import get_files_from_dir, unique_items
from kelvin.sdk.lib.utils.logger_utils import logger


# 1 - App Building
def setup_datatypes(kelvin_app_building_object: KelvinAppBuildingObject) -> Optional[KPath]:
    """
    Handle the datatypes, both the raw datatype folder and app configuration datatype specifications and copy them
    to the intended build dir folder for processing.


    Parameters
    ----------
    kelvin_app_building_object : KelvinAppBuildingObject
        the KelvinAppBuildingObject used to configure the datatype interaction.

    Returns
    -------
    Optional[KPath]
        an optional string indicating the path to the build folder that will contain the models to be compiled.

    """
    logger.info("Processing application data types..")

    datatype_dir_path = kelvin_app_building_object.app_datatype_dir_path
    if datatype_dir_path is None:
        return None

    app_configuration_object: KelvinAppConfiguration = kelvin_app_building_object.app_config_model
    app_config_file_path: KPath = kelvin_app_building_object.app_config_file_path
    kelvin_app_configuration = app_configuration_object.app.app_type_configuration
    app_name = app_configuration_object.info.name
    if kelvin_app_configuration:
        # 1 - retrieves datatypes from the configuration (kelvin->app->data_types)
        datatypes_to_handle_complete = [*(kelvin_app_configuration.data_types or [])]
        datatypes_to_handle = [
            item for item in datatypes_to_handle_complete if not _is_a_raw_datatype(data_type=item.name)
        ]

        # 2 - reset the "build/datatype/" directory
        datatype_dir_path.delete_dir().create_dir()

        # 3 - handle the datatypes prior to the upload
        if datatypes_to_handle:
            logger.info(f'Retrieving data types for "{app_name}"')
            if kelvin_app_building_object.build_for_upload:
                datatypes_successfully_handled = _handle_upload_phase_datatypes(
                    datatypes_to_handle=datatypes_to_handle,
                    input_dir_path=KPath(datatype_dir_path.name),
                    ignore_warning=kelvin_app_building_object.upload_datatypes,
                )
                # 5 - update app's app.yaml by removing datatypes path field after upload
                remove_paths_from_datatypes = any([item.path for item in datatypes_to_handle])
                if datatypes_successfully_handled and remove_paths_from_datatypes:
                    # Commit the changes and proceed
                    datatypes = [datatype.dict(exclude={"path"}) for datatype in datatypes_to_handle]
                    raw_app_config = app_config_file_path.read_yaml()
                    raw_app_config["app"]["kelvin"]["data_types"] = datatypes
                    app_config_file_path.write_yaml(yaml_data=raw_app_config)

            for datatype in datatypes_to_handle:
                # local
                if datatype.path:
                    datatype_path = app_config_file_path.parent.absolute() / KPath(datatype.path)
                    ICDPayloadHelper(**datatype_path.read_yaml())
                    datatype_path.clone_into(path=datatype_dir_path)
                # remote
                else:
                    datatype_name_with_version = f"{datatype.name}:{datatype.version}"
                    download_datatype(
                        datatype_name_with_version=datatype_name_with_version,
                        output_dir=datatype_dir_path,
                    )

            content = [content for content in datatype_dir_path.dir_content() if not content.startswith(".")]
            should_compile = bool(content)
            return datatype_dir_path if should_compile else None

    logger.info("No data types to process")
    return None


# 2 - datatype creation
def create_datatype(datatype_name: str, output_dir: Optional[str] = None) -> OperationResponse:
    """
    Creates a data type from the specified parameters.

    Parameters
    ----------
    datatype_name : str
        the name of the datatype to create.
    output_dir : Optional[str]
        the output directory where the data type will be created.

    Returns
    ----------
    OperationResponse
        an OperationResponse object encapsulating the result of the data type creation operation.

    """
    try:
        check_if_datatype_name_is_valid(datatype_name=datatype_name)

        # 1 - check if the current output directory is an app.
        datatype_output_dir: KPath = _evaluate_datatype_dir(datatype_dir=output_dir)

        # 2 - Validate the datatype name and determine its file path
        datatype_item = ICDPayloadHelper(
            name=datatype_name,
            version=DataTypeConfigs.datatype_default_version,
            description="",
            payload_fields=[],
            class_name="SomeClassName",  # this is not used
        )
        datatype_file_name = datatype_item.datatype_file_name

        logger.info(f'Creating spec for data type "{datatype_item.name}"')

        # 3 - Render the default ICD sample template
        default_icd_template = get_embedded_file(embedded_file=EmbeddedFiles.DEFAULT_DATATYPE_TEMPLATE)
        default_icd_template_rendered = default_icd_template.render(
            datatype_name=datatype_item.name, datatype_version=datatype_item.version
        )

        # 4 - Write it down on the target file
        template_output_file_path: KPath = datatype_output_dir / datatype_file_name
        template_output_file_path.write_content(content=default_icd_template_rendered)

        # 5 - Log the success message
        output_file: str = str(template_output_file_path.absolute())
        success_message = f'Data type "{datatype_name}" spec successfully created in "{output_file}"'
        logger.relevant(success_message)
        return OperationResponse(success=True, log=success_message)

    except Exception as exc:
        error_message = f"Error creating data type spec file: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


# 3 - datatype upload
def upload_datatypes(input_dir: Optional[str] = None, datatypes: Optional[List[str]] = None) -> OperationResponse:
    """
    Upload all the data types in the provided input directory.

    Parameters
    ----------
    input_dir: Optional[str]
        the directory to read the data types from.
    datatypes: Optional[List[str]]
        the names of the data types to upload.

    Returns
    ----------
    OperationResponse
        an OperationResponse object encapsulating the result of the data type upload operation.

    """
    try:
        # auxiliary variable due to mypy issue with optional str
        datatypes_input_dir: KPath = _evaluate_datatype_dir(datatype_dir=input_dir)

        logger.info(f'Uploading data types from directory "{datatypes_input_dir}"')

        loaded_datatypes = _load_all_datatype_files(input_dir=datatypes_input_dir)
        if datatypes:
            loaded_datatypes = _filter_datatypes(loaded_datatypes=loaded_datatypes, datatype_names=datatypes)
        if loaded_datatypes:
            all_platform_datatypes = datatype_list(all_datatypes=True, should_display=False)
            all_datatypes = [DataType(**item) for item in all_platform_datatypes.data if all_platform_datatypes]
            dependency_tree = _build_datatype_upload_dependency_tree(loaded_datatypes=loaded_datatypes)
            upload_result = _process_datatype_upload_dependency_tree(
                all_platform_datatypes=all_datatypes,
                loaded_datatypes=loaded_datatypes,
                dependency_tree=dependency_tree,
            )
            success_message = "Data types successfully processed"
            logger.relevant(success_message)
            return OperationResponse(success=upload_result, log=success_message)
        else:
            error_message = "No data types to process matching your criteria"
            logger.error(error_message)
            return OperationResponse(success=False, log=error_message)
    except Exception as exc:
        error_message = f"Error uploading data types: {str(exc)}"
        logger.exception(error_message)
        return OperationResponse(success=False, log=error_message)


# 4 - datatype download
def download_datatype(datatype_name_with_version: str, output_dir: Optional[str] = None) -> OperationResponse:
    """
    Download the datatype corresponding to the provided data type id into the provided output dir.

    Parameters
    ----------
    datatype_name_with_version: str
        the name with version of the data type to download.
    output_dir: Optional[str]
        the path into which the data types should be downloaded.

    Returns
    ----------
    OperationResponse
        an OperationResponse object encapsulating the result of the data type download operation.

    """
    check_if_datatype_name_with_version_is_valid(app_name_with_version=datatype_name_with_version)

    datatype_output_dir: KPath = _evaluate_datatype_dir(datatype_dir=output_dir)

    name_with_version = DockerImageName.parse(name=datatype_name_with_version)
    if name_with_version.version is None:
        raise DataTypeException('Please provide a valid datatype version. "datatype:version"')

    acquired_datatype: Optional[ICDPayloadHelper] = datatype_download(
        datatype_name=name_with_version.name,
        datatype_version=name_with_version.version,
        output_dir=datatype_output_dir,
    )
    if acquired_datatype:
        downloaded_datatype_fields = acquired_datatype.dependency_datatypes
        for dependency_datatype_name in downloaded_datatype_fields:
            download_datatype(datatype_name_with_version=dependency_datatype_name, output_dir=datatype_output_dir)

    if not acquired_datatype:
        raise DataTypeException("Error processing data type tree")

    return OperationResponse(success=True, log="datatype successfully downloaded.")


# Internal utils
def _load_all_datatype_files(input_dir: str) -> List[Tuple[str, ICDPayloadHelper]]:
    """
    Load all datatypes from the provided input directory.

    Parameters
    ----------
    input_dir : str
        the input directory to read the datatype files from.

    Returns
    -------
    List[Tuple[str, ICDPayloadHelper]]
        a list of tuples containing the key and the respective ICDPayloadHelper


    """
    logger.info(f'Loading all data type files from directory "{input_dir}"')

    # 1 - get all datatypes
    yml_file_type: str = DataTypeConfigs.datatype_default_icd_extension
    datatype_files = get_files_from_dir(file_type=yml_file_type, input_dir=input_dir)
    datatype_file_paths = [KPath(input_dir) / file for file in datatype_files]

    # 2 - from the datatype files, load all datatype entries into a list of tuples (path + datatype ICD)
    loaded_datatypes: List = []
    for file in datatype_file_paths:
        yaml_content: Generator = file.read_yaml_all()
        for entry in yaml_content:
            loaded_datatypes.append((file, ICDPayloadHelper(**entry)))

    # 3 - report and return
    total = len(loaded_datatypes)
    logger.relevant(f'{total} data types loaded from directory "{input_dir}"')
    return loaded_datatypes


def _handle_upload_phase_datatypes(
    datatypes_to_handle: List[DataType], input_dir_path: KPath, ignore_warning: bool = False
) -> bool:
    """
    If a local datatype is provided during the appregistry upload phase, make sure to warn the user
    and, if ruled so, upload them.

    Parameters
    ----------
    datatypes_to_handle : List[DataType]
        the names of the datatypes to handle. Mainly for display purpose.
    input_dir_path : KPath
        The input directory where the datatypes are hosted.
    ignore_warning: bool
        indicates whether the upload warning should be displayed.

    Returns
    -------
    bool
        a boolean indicating whether the datatypes have been successfully uploaded.

    """
    local_datatypes = [f"{model.name}:{model.version}" for model in datatypes_to_handle if model.path]

    if local_datatypes:
        local_datatypes_list = ", ".join(local_datatypes)
        local_datatypes_upload_warning: str = f"""

            The application you're trying to upload has references to local data types:

            > {local_datatypes_list}

            Do you wish to upload them to the platform before proceeding?

        """
        if not ignore_warning:
            ignore_warning = display_yes_or_no_question(question=local_datatypes_upload_warning)
        if ignore_warning:
            result = upload_datatypes(input_dir=input_dir_path, datatypes=None)
            if not result.success:
                raise DataTypeException(result.log)

    return True


def _filter_datatypes(
    loaded_datatypes: List[Tuple[str, ICDPayloadHelper]], datatype_names: List[str]
) -> List[Tuple[str, ICDPayloadHelper]]:
    """
    Filter the loaded datatypes list

    Parameters
    ----------
    loaded_datatypes : List[Tuple[str, ICDPayloadHelper]]
        the list of datatypes to process.
    datatype_names : List[str]
        the list of datatypes to filter.

    Returns
    -------
    List[Tuple[str, ICDPayloadHelper]]
        a list of filtered datatypes tuples

    """
    filtered_datatypes: List[Tuple[str, ICDPayloadHelper]] = []
    filtered_datatypes_names: List[str] = []

    for datatype in loaded_datatypes:
        file, icd = datatype
        if icd.full_datatype_name in datatype_names:
            filtered_datatypes.append(datatype)
            filtered_datatypes_names.append(icd.full_datatype_name)

    # check for not found datatypes
    for datatype_name in datatype_names:
        if datatype_name not in filtered_datatypes_names:
            logger.warn(f'No data type found matching your criteria: "{datatype_name}"')

    total = len(filtered_datatypes)
    if total:
        logger.relevant(f"A total of {total} data types loaded match your criteria: {filtered_datatypes_names}")

    return filtered_datatypes


def _build_datatype_upload_dependency_tree(
    loaded_datatypes: List[Tuple[str, ICDPayloadHelper]]
) -> Tuple[List[str], List[str]]:
    """
    Process the loaded datatypes and retrieve the dependency tree with the correct upload structure.

    Parameters
    ----------
    loaded_datatypes : List[Tuple[str, ICDPayloadHelper]]
        the list of datatypes to process.

    Returns
    -------
    Tuple[List[str], List[str]]
        the organized list datatype names with version, ready to operate.

    """
    logger.info("Processing the data type dependency tree.")
    requires_processing: Dict[str, List[str]] = {}
    prepare_for_upload: List[str] = []

    # 1 - Load the datatypes
    for _, datatype in loaded_datatypes:
        datatype_name_with_version = f"{datatype.name}:{datatype.version}"
        datatype_fields = datatype.payload_fields or []
        dependencies = requires_processing[
            datatype_name_with_version
        ] = []  # Register the datatype in the dependency tree
        for field in datatype_fields:
            # 2 - Custom datatypes must have a semver tag. If not, its a raw sub type and its not processed (go to #4)
            if field.type and ":" in field.type and field.type not in dependencies:
                # 3 - Register each sub datatype reference
                dependencies.append(field.type)
        # 4 - if the datatype has no custom datatype in its fields, skip any processing and mark it for upload.
        if not dependencies:
            prepare_for_upload.append(datatype_name_with_version)

    verify_on_the_platform = []
    while requires_processing:
        keys = requires_processing.keys()
        items = list(requires_processing.items())
        for key, value in items:
            for item in value:
                if item in keys:
                    prepare_for_upload.append(item)
                else:
                    verify_on_the_platform.append(item)
                prepare_for_upload.append(key)
            del requires_processing[key]

    prepare_for_upload = unique_items(items=prepare_for_upload)
    verify_on_the_platform = unique_items(items=verify_on_the_platform)
    verify_on_the_platform = [item for item in verify_on_the_platform if item not in prepare_for_upload]
    return prepare_for_upload, verify_on_the_platform


def _process_datatype_upload_dependency_tree(
    all_platform_datatypes: List[DataType],
    loaded_datatypes: List[Tuple[str, ICDPayloadHelper]],
    dependency_tree: Tuple[List[str], List[str]],
) -> bool:
    """
    Process the datatype dependency tree and uploaded what is necessary to the platform.

    Parameters
    ----------
    all_platform_datatypes : List[DataType]
        a list of all platform datatypes.
    loaded_datatypes : List[Tuple[str, ICDPayloadHelper]]
        a list containing all the loaded datatypes.
    dependency_tree : Tuple[List[str], List[str]]
        the dependency tree composed by the ordered name of datatypes to upload.

    Returns
    -------
    bool
        a bool indicating the datatypes were successfully processed.

    """
    logger.info("Initializing the data type upload operation.")

    # 1 - get a list of datatypes as strings
    all_platform_datatypes_names: List[str] = [f"{model.name}:{model.version}" for model in all_platform_datatypes]

    datatypes_to_upload, datatypes_to_check_on_the_platform = dependency_tree
    for datatype in datatypes_to_check_on_the_platform:
        # 2 - if the datatype is not present in the platform nor the local definition, raise an exception
        if datatype not in all_platform_datatypes_names:
            raise DataTypeException(message=f'Invalid data type "{datatype}". Please check the platform')
        else:  # 3 - If the datatype already exists, inform the user
            logger.warn(f'Data type "{datatype}" already present in the system. Skipping.')

    for datatype_name_with_version in datatypes_to_upload:
        if datatype_name_with_version not in all_platform_datatypes_names:
            name, version = datatype_name_with_version.split(":")
            clean = [(file, icd) for (file, icd) in loaded_datatypes if icd.name == name and icd.version == version]
            file, icd = next(iter(clean))
            if icd:
                datatype_uploaded = datatype_upload(datatype_content=icd.dict(), source=str(file))
                if not datatype_uploaded.success:
                    raise DataTypeException("Error processing data type tree")
        else:
            logger.warn(f'Data type "{datatype_name_with_version}" already present in the system. Skipping.')

    return True


def _evaluate_datatype_dir(datatype_dir: Optional[str] = None) -> KPath:
    """
    Check if the provided dir is valid for two conditions:
        1 - Is a valid app directory
        2 - If The output_dir is none, the current dir will be used and must be a valid app directory

    Parameters
    ----------
    datatype_dir : Optional[str]
        optional output dir

    Returns
    -------
    KPath
        a resolved and validated KPath

    """
    try:
        # if output dir is an app dir, create the datatype inside the app's datatype folder
        # otherwise create the datatype in the app's root
        if not datatype_dir:
            datatype_dir = ""
        base_build_object = get_project_building_object(app_dir=datatype_dir)
        datatype_output_dir = base_build_object.app_dir_path / GeneralConfigs.default_datatype_dir
    except Exception:
        if not datatype_dir:
            raise DataTypeException("Please provide a valid application directory or specify a directory")
        else:
            datatype_output_dir = KPath(datatype_dir)

    datatype_output_dir = datatype_output_dir.complete_path()
    return datatype_output_dir


def _is_a_raw_datatype(data_type: str) -> bool:
    """
    Indicates whether the provided data type is a raw data type.

    Parameters
    ----------
    data_type : str
        the input data type.


    Returns
    -------
    bool
        a boolean indicating whether the provided data type is part of the raw list.

    """
    if ":" in data_type:
        data_type_name, _ = data_type.split(":")
    else:
        data_type_name = data_type

    return data_type_name is not None and data_type_name in DataTypeConfigs.raw_datatype_list
