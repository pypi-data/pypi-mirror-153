from typing import Callable, Optional

from django.db.models import Model
from pydantic import BaseModel, Field

LoginFunction = Callable[[Model, str], str]


class PermissionTestExpectation(BaseModel):
    user: Model = Field(
        description="Should be AbstractBaseUser but this lead to a circular import. "
    )
    password: str = Field(description="Password that is used for the user to login")
    get_list_status_code: Optional[int] = None
    get_list_return_number: Optional[int] = None
    get_detail_status_code: Optional[int] = None
    create_status_code: Optional[int] = None
    patch_status_code: Optional[int] = None
    put_status_code: Optional[int] = None
    delete_status_code: Optional[int] = None

    class Config:
        arbitrary_types_allowed = True
