from abc import ABC
from typing import List, Optional, Union
from pydantic import BaseModel, PositiveInt, Field

class BaseSchema(BaseModel, ABC):
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class UserSchema(BaseSchema):
    id: PositiveInt
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[str] = None
    favorite_genres: Optional[str] = None

class TrackSchema(BaseSchema):
    id: PositiveInt
    name: Optional[str] = None
    artist: Optional[str] = None
    songwriters: Optional[str] = None
    duration: Optional[str] = None
    genres: Optional[str] = None
    album: Optional[str] = None

class ListenHistorySchema(BaseSchema):
    user_id: PositiveInt
    items: Optional[List[PositiveInt]] = Field(None, min_items=0)

class ApiSchema(BaseModel):
    total: PositiveInt
    page: PositiveInt
    size: PositiveInt
    pages: PositiveInt
    items: List[Union[UserSchema, TrackSchema, ListenHistorySchema]] = Field(..., min_items=1)
