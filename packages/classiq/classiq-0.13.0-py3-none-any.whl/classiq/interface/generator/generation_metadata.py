from typing import Dict, List, Optional, Union

import pydantic
from typing_extensions import Literal

from classiq.interface.generator.finance import FinanceMetadata, FinanceModelMetadata
from classiq.interface.generator.grover_operator import GroverMetadata

_INVALID_METADATA_ERROR_MSG = "Invalid metadata file."
ParamMetadataUnion = Union[GroverMetadata, FinanceMetadata, FinanceModelMetadata]


class FunctionMetadata(pydantic.BaseModel):
    metadata_type: Literal["function"] = "function"
    name: str
    parent: Optional[str]
    children: List[str]
    hierarchy_level: int
    _parents: Dict[int, str] = pydantic.PrivateAttr(default={})

    def add_parents(self, parents: Dict[int, str]):
        for parent_hierarchy_level in parents.keys():
            if parent_hierarchy_level >= self.hierarchy_level:
                raise ValueError("Parent's hierarchy level must be lower than child's")
        self._parents.update(parents)

    @property
    def parents(self):
        return self._parents


class GenerationMetadata(pydantic.BaseModel):
    # Ideally, we would use a "__root__" attribute, but the typescript transpilation
    # does weird things when we use it.
    metadata: ParamMetadataUnion = pydantic.Field(..., discriminator="metadata_type")
