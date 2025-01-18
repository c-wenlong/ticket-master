from typing import Generic, Optional, TypeVar
from pydantic import BaseModel

DataT = TypeVar('DataT', default=dict)

class BaseResponse(BaseModel):
    message: str

class HttpResponse(BaseModel, Generic[DataT]):
    base: BaseResponse
    data: Optional[DataT] = None