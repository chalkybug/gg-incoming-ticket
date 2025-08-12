from pydantic import BaseModel, validator
from typing import List, Union


class JiraViewModel(BaseModel):
    # key: Union[str, None] = None
    # link: Union[str, None] = None
    count: Union[int, None] = None
    summary: Union[str, None] = None
    assignee: Union[str, None] = None
    status: Union[int, None] = None
    query: Union[str, None] = None


class JiraBatchModel(BaseModel):
    batch: List[JiraViewModel]
