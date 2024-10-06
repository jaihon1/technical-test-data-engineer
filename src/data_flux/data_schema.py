from abc import ABC
from typing import List, Optional
from pydantic import BaseModel, Field, PositiveInt

from api_schema import ListenHistorySchema, TrackSchema, UserSchema
from endpoints import Endpoints


class BaseDataSchema(BaseModel, ABC):
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    version_id: PositiveInt

class UserDataSchema(BaseDataSchema):
    id: PositiveInt
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[str] = None
    favorite_genres: Optional[str] = None

class TrackDataSchema(BaseDataSchema):
    id: PositiveInt
    name: Optional[str] = None
    artist: Optional[str] = None
    songwriters: Optional[str] = None
    duration: Optional[str] = None
    genres: Optional[str] = None
    album: Optional[str] = None

class ListenHistoryDataSchema(BaseDataSchema):
    user_id: PositiveInt
    items: Optional[List[PositiveInt]] = Field(None, min_items=0)


def build_common_data_schema(data, version_id):
    """
    Build common schema fields that are present in all schemas.
    """
    return {
        'version_id': version_id,
        'created_at': data.created_at,
        'updated_at': data.updated_at
    }

def build_user_data_schema(data: UserSchema, version_id) -> UserDataSchema:
    common_fields = build_common_data_schema(data, version_id)

    return UserDataSchema(
        **common_fields,
        id=data.id,
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        gender=data.gender,
        favorite_genres=data.favorite_genres,
    )

def build_track_data_schema(data: TrackSchema, version_id) -> TrackDataSchema:
    common_fields = build_common_data_schema(data, version_id)

    return TrackDataSchema(
        **common_fields,
        id=data.id,
        name=data.name,
        artist=data.artist,
        songwriters=data.songwriters,
        duration=data.duration,
        genres=data.genres,
        album=data.album
    )

def build_listen_history_data_schema(data: ListenHistorySchema, version_id) -> ListenHistoryDataSchema:
    common_fields = build_common_data_schema(data, version_id)

    return ListenHistoryDataSchema(
        **common_fields,
        user_id=data.user_id,
        items=data.items
    )

endpoint_builder_map = {
    Endpoints.USERS: build_user_data_schema,
    Endpoints.TRACKS: build_track_data_schema,
    Endpoints.LISTEN_HISTORY: build_listen_history_data_schema,
}
