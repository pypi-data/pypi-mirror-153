import enum
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Optional

from humps import camelize
from pydantic import BaseModel


def to_camel(s: str) -> str:
    return camelize(s)


class CamelBaseModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class OutputFormat(str, enum.Enum):
    json = "json"
    table = "table"
    yaml = "yaml"


class AffectedEntityType(enum.Enum):
    ENTITY = "ENTITY"
    JOB = "JOB"


class GitChangeType(enum.Enum):
    MODEL_FILE_RENAME = "MODEL_FILE_RENAME"
    MODEL_ALIAS_RENAME = "MODEL_ALIAS_RENAME"
    NONE = "NONE"


class FileGitHistory(BaseModel):
    path: str
    previous_path: str
    file_name: str
    model_name: str
    file_alias: Optional[str]
    previous_file_name: str
    previous_model_name: str
    previous_file_alias: Optional[str]
    change_type: GitChangeType


class CalledProcessError(RuntimeError):
    pass


class JsonOpenError(RuntimeError):
    pass


class Model(CamelBaseModel):
    model_id: str
    model_name: str
    filename: str
    node: Dict[str, Any]


class Macro(CamelBaseModel):
    macro_id: str
    macro_name: str
    filename: str
    macro: Dict[str, Any]


class Test(CamelBaseModel):
    test_id: str
    test_type: str
    test_name: str
    node: Dict[str, Any]


class Source(CamelBaseModel):
    source_id: str
    source_name: str
    table_name: str
    filename: str
    node: Dict[str, Any]


class ModelSchema(CamelBaseModel):
    model_name: str
    filename: str
    model_schema: Any
    file: Path
    prefix: str = "model"


class MacroSchema(CamelBaseModel):
    macro_name: str
    filename: str
    macro_schema: Any
    file: Path
    prefix: str = "macro"


class SourceSchema(CamelBaseModel):
    source_name: str
    table_name: str
    filename: str
    source_schema: Dict[str, Any]
    table_schema: Dict[str, Any]
    prefix: str = "source"


class BaseCLIReport(CamelBaseModel):
    markdown_text: str
    status_code: int


class ImpactAnalysisCLIReport(BaseCLIReport):
    pass
