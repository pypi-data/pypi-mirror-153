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

from typing import List, Optional, Sequence

from pydantic import BaseModel

from kelvin.sdk.lib.models.types import StatusDataSource


class LoginRequest(BaseModel):
    url: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    totp: Optional[str] = None
    reset_credentials: bool = True


class AuthenticationTokenRequest(BaseModel):
    full: bool = False
    margin: float = 10.0


class SecretCreateRequest(BaseModel):
    secret_name: str
    value: str


class SecretDeleteRequest(BaseModel):
    secret_names: Sequence[str]


class DataTypeCreateRequest(BaseModel):
    datatype_name: str
    output_dir: Optional[str]


class DataTypeUploadRequest(BaseModel):
    input_dir: Optional[str]
    datatypes: Optional[List[str]]


class AssetCreationObject(BaseModel):
    asset_name: str
    asset_type_name: str
    asset_title: str
    entity_type_name: str
    parent: Optional[str]


class AssetTypeCreationObject(BaseModel):
    asset_type_name: str
    asset_type_title: str
    asset_class_name: str


class EmulationStartRequest(BaseModel):
    app_config_path: Optional[str] = None
    app_name_with_version: Optional[str] = None
    tail: Optional[int] = None


class EmulationLogsRequest(BaseModel):
    app_name_with_version: Optional[str] = None
    tail: Optional[int] = 200


class EmulationStopRequest(BaseModel):
    app_name_with_version: Optional[str] = None
    container_name: Optional[str] = None


class AppBuildRequest(BaseModel):
    app_dir_absolute_path: str
    fresh_build: bool = False


class AppImagesUnpackRequest(BaseModel):
    app_name_with_version: str
    container_dir: Optional[str] = None
    output_dir: str


class ConfigurationSetRequest(BaseModel):
    configuration: str
    value: str


class ConfigurationUnsetRequest(BaseModel):
    configuration: str


class WorkloadListRequest(BaseModel):
    query: Optional[str] = None
    node_name: Optional[str] = None
    app_name: Optional[str] = None
    enabled: Optional[bool] = None
    source: StatusDataSource = StatusDataSource.CACHE


class WorkloadUpdateRequest(BaseModel):
    workload_name: str
    app_config_absolute_path: str
    workload_title: Optional[str] = None


class WorkloadLogsRequest(BaseModel):
    workload_name: str
    tail_lines: int
    output_file_absolute_path: Optional[str] = None
    follow: bool = False


class SchemaValidateRequest(BaseModel):
    file_path: str
    schema_file_path: Optional[str] = None
    full_schema_errors: bool = False
