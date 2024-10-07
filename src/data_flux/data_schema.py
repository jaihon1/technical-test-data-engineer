from typing import List, Optional
from pydantic import BaseModel, Field, PositiveInt

from src.data_flux.api_schema import ListenHistorySchema, TrackSchema, UserSchema, BaseSchema
from src.data_flux.endpoints import Endpoints


class BaseDataSchema(BaseModel):
    """
    Base schema for data models, providing common fields for tracking creation,
    update timestamps, and version control.

    This class serves as a foundation for other data schema classes, ensuring
    that they inherit common attributes such as `created_at`, `updated_at`, and
    `version_id`.

    Attributes:
        created_at (Optional[str]):
            The timestamp of when the record was created.
            Defaults to None if not provided.
        updated_at (Optional[str]):
            The timestamp of when the record was last updated.
            Defaults to None if not provided.
        version_id (PositiveInt):
            Used to version control the iterations of data flux.
            This field is required.

    Inherits:
        BaseModel: Provides Pydantic model functionalities.
    """

    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    version_id: PositiveInt

class UserDataSchema(BaseDataSchema):
    """
    Schema representing user data.

    This schema defines the attributes relevant to a user and ensures that the
    `id` field is required, while other fields such as `first_name`, `last_name`,
    `email`, `gender`, and `favorite_genres` are optional.

    Attributes:
        id (PositiveInt):
            A unique identifier for the user.
            This field is required.
        first_name (Optional[str]):
            The first name of the user.
            Defaults to None if not provided.
        last_name (Optional[str]):
            The last name of the user.
            Defaults to None if not provided.
        email (Optional[str]):
            The email address of the user.
            Defaults to None if not provided.
        gender (Optional[str]):
            The gender of the user.
            Defaults to None if not provided.
        favorite_genres (Optional[str]):
            A string representing the user's favorite genres.
            Defaults to None if not provided.

    Inherits:
        BaseDataSchema: Provides the foundation for data schema validation.
    """

    id: PositiveInt
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[str] = None
    favorite_genres: Optional[str] = None

class TrackDataSchema(BaseDataSchema):
    """
    Schema representing track data.

    This schema defines the attributes relevant to a music track and ensures that the
    `id` field is required, while other fields such as `name`, `artist`, `songwriters`,
    `duration`, `genres`, and `album` are optional.

    Attributes:
        id (PositiveInt):
            A unique identifier for the track.
            This field is required.
        name (Optional[str]):
            The name of the track.
            Defaults to None if not provided.
        artist (Optional[str]):
            The artist of the track.
            Defaults to None if not provided.
        songwriters (Optional[str]):
            The songwriters of the track.
            Defaults to None if not provided.
        duration (Optional[str]):
            The duration of the track.
            Defaults to None if not provided.
        genres (Optional[str]):
            The genres associated with the track.
            Defaults to None if not provided.
        album (Optional[str]):
            The album the track belongs to.
            Defaults to None if not provided.

    Inherits:
        BaseDataSchema: Provides the foundation for data schema validation.
    """

    id: PositiveInt
    name: Optional[str] = None
    artist: Optional[str] = None
    songwriters: Optional[str] = None
    duration: Optional[str] = None
    genres: Optional[str] = None
    album: Optional[str] = None

class ListenHistoryDataSchema(BaseDataSchema):
    """
    Schema representing the listen history data of a user.

    This schema defines the attributes relevant to a user's listening history,
    ensuring that the `user_id` is required while `items` is optional.

    Attributes:
        user_id (PositiveInt):
            A unique identifier for the user.
            This field is required.
        items (Optional[List[PositiveInt]]):
            A list of unique identifiers for tracks that the user has listened to.
            Defaults to None if not provided, and must contain a minimum of 0 items.

    Inherits:
        BaseDataSchema: Provides the foundation for data schema validation.
    """

    user_id: PositiveInt
    items: Optional[List[PositiveInt]] = Field(None, min_items=0)


def build_common_data_schema(data: BaseSchema, version_id) -> BaseDataSchema:
    """
    Build a dictionary of common schema fields for use in data schemas.

    This function extracts common fields such as `version_id`, `created_at`, and `updated_at`
    from the provided data object and returns them in a standardized format. This is useful for
    ensuring consistency across different data schemas that share these attributes.

    Arguments:
        data (UserSchema, TrackSchema, ListenHistorySchema):
            An instance of BaseSchema containing common fields, including `created_at` and `updated_at`.

        version_id (PositiveInt):
            The version identifier for the data schema, used for version control.

    Returns:
        BaseDataSchema:
            An instance of BaseDataSchema.
    """

    return BaseDataSchema(
        version_id = version_id,
        created_at = data.created_at,
        updated_at = data.updated_at
    )

def build_user_data_schema(data: UserSchema, version_id) -> UserDataSchema:
    """
    Build a UserDataSchema instance from a UserSchema and a version identifier.

    This function extracts common fields from the provided `data`, which is an instance of
    UserSchema, and combines them with user-specific fields to create a UserDataSchema instance.
    This ensures that all necessary fields are included and correctly formatted.

    Arguments:
        data (UserSchema):
            An instance of UserSchema.

        version_id (PositiveInt):
            The version identifier for the data schema, used for version control.

    Returns:
        UserDataSchema:
            An instance of UserDataSchema.
    """

    common_fields = build_common_data_schema(data, version_id)

    return UserDataSchema(
        **common_fields.__dict__,
        id=data.id,
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        gender=data.gender,
        favorite_genres=data.favorite_genres,
    )

def build_track_data_schema(data: TrackSchema, version_id) -> TrackDataSchema:
    """
    Build a TrackDataSchema instance from a TrackSchema and a version identifier.

    This function extracts common fields from the provided `data`, which is an instance of
    TrackSchema, and combines them with track-specific fields to create a TrackDataSchema instance.
    This ensures that all necessary fields are included and correctly formatted.

    Arguments:
        data (TrackSchema):
            An instance of TrackSchema.

        version_id (PositiveInt):
            The version identifier for the data schema, used for version control.

    Returns:
        TrackDataSchema:
            An instance of TrackDataSchema.
    """

    common_fields = build_common_data_schema(data, version_id)

    return TrackDataSchema(
        **common_fields.__dict__,
        id=data.id,
        name=data.name,
        artist=data.artist,
        songwriters=data.songwriters,
        duration=data.duration,
        genres=data.genres,
        album=data.album
    )

def build_listen_history_data_schema(data: ListenHistorySchema, version_id) -> ListenHistoryDataSchema:
    """
    Build a ListenHistoryDataSchema instance from a ListenHistorySchema and a version identifier.

    This function extracts common fields from the provided `data`, which is an instance of
    ListenHistorySchema, and combines them with listen history-specific fields to create a
    ListenHistoryDataSchema instance. This ensures that all necessary fields are included and
    correctly formatted.

    Arguments:
        data (ListenHistorySchema):
            An instance of ListenHistorySchema.

        version_id (PositiveInt):
            The version identifier for the data schema, used for version control.

    Returns:
        ListenHistoryDataSchema:
            An instance of ListenHistoryDataSchema.
    """

    common_fields = build_common_data_schema(data, version_id)

    return ListenHistoryDataSchema(
        **common_fields.__dict__,
        user_id=data.user_id,
        items=data.items
    )


"""
Mapping of API endpoints to their corresponding data schema builder functions.

This dictionary serves as a routing mechanism that associates specific API endpoints
with their respective functions for building data schemas. Each key in the dictionary
represents an endpoint defined in the `Endpoints` enumeration, while the associated
value is a function that constructs the appropriate data schema.

Attributes:
    Endpoints.USERS (Endpoints):
        The endpoint for user-related operations, mapped to the function
        for building user data schemas.

    Endpoints.TRACKS (Endpoints):
        The endpoint for track-related operations, mapped to the function
        for building track data schemas.

    Endpoints.LISTEN_HISTORY (Endpoints):
        The endpoint for listen history operations, mapped to the function
        for building listen history data schemas.

Returns:
    dict:
        A dictionary mapping each endpoint to its corresponding data schema builder function.
"""

endpoint_builder_map = {
    Endpoints.USERS: build_user_data_schema,
    Endpoints.TRACKS: build_track_data_schema,
    Endpoints.LISTEN_HISTORY: build_listen_history_data_schema,
}
