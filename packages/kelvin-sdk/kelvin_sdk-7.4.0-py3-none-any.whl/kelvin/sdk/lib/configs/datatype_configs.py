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


class DataTypeConfigs:
    datatype_default_icd_extension: str = ".yml"
    datatype_default_version: str = "0.0.1"
    datatype_name_acceptance_regex: str = r"^[a-zA-Z]\w*(\.[a-zA-Z]\w*)*$"
    datatype_class_name_acceptance_regex: str = r"^[a-zA-Z][a-zA-Z0-9_]+$"
    raw_datatype_list: list = [
        "raw.boolean",
        "raw.float32",
        "raw.float64",
        "raw.int8",
        "raw.int16",
        "raw.int32",
        "raw.int64",
        "raw.text",
        "raw.uint8",
        "raw.uint16",
        "raw.uint32",
        "raw.uint64",
        "object",
    ]
