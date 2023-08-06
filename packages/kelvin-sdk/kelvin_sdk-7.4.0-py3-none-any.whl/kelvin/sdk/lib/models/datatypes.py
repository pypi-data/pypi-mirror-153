import re
from typing import Any, Dict, List, Optional

from pydantic import Field, StrictStr

from kelvin.sdk.lib.configs.datatype_configs import DataTypeConfigs
from kelvin.sdk.lib.exceptions import DataTypeException
from kelvin.sdk.lib.models.generic import KSDKModel


class DottedIdentifierWithVersion(StrictStr):
    regex = re.compile(r"^([a-z][a-z0-9_]+\.)+[a-z][a-z0-9_]+:[^:]+$")


class DottedIdentifierWithOptionalVersion(StrictStr):
    regex = re.compile(r"^([a-z][a-z0-9_]+\.)+[a-z][a-z0-9_]+:?[^:]+$")


class ICDField(KSDKModel):
    description: str
    name: str
    type: str
    array: Optional[bool]


class ICDName(StrictStr):
    regex = re.compile(DataTypeConfigs.datatype_name_acceptance_regex)


class ICDClassName(StrictStr):
    regex = re.compile(DataTypeConfigs.datatype_class_name_acceptance_regex)


class ICDPayloadHelper(KSDKModel):
    name: ICDName
    class_name: ICDClassName
    description: str
    payload_fields: List[ICDField] = Field(..., alias="fields")
    version: str

    class Config:
        allow_population_by_field_name: bool = True

    def dict(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        return super().dict(by_alias=True, *args, **kwargs)

    @property
    def datatype_file_name(self) -> str:
        """
        Based on the data type name and its version, get the project specific file name.

        Returns
        -------
        str
            the name of the file that will be created to host the new Datatype

        """
        if not self.name or not self.version:
            raise DataTypeException("Datatype requires both a name and a version")

        name: str = self.name.replace(".", "_")
        version: str = self.version.replace(".", "-")

        return f"{name}__{version}{DataTypeConfigs.datatype_default_icd_extension}"

    @property
    def full_datatype_name(self) -> str:
        return f"{self.name}:{self.version}"

    @property
    def dependency_datatypes(self) -> List[str]:
        return_obj = []
        for item in self.payload_fields:
            if item.type and item.type.count(":") == 1:
                return_obj.append(item.type)
        return list(set(return_obj))
