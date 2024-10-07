from abc import ABC
from typing import List, Optional, Union
from pydantic import BaseModel, PositiveInt, Field

class BaseSchema(BaseModel, ABC):
    """
    Base API Schema class that provides common fields for all derived schemas.

    This class serves as a foundation for other schema classes, ensuring that
    they inherit common attributes such as `created_at` and `updated_at`.

    Attributes:
        created_at (Optional[str]):
            The timestamp of when the record was created.
            For current version, it defaults to None if not provided.
        updated_at (Optional[str]):
            The timestamp of when the record was last updated.
            For current version, it defaults to None if not provided.

    Inherits:
        BaseModel: Provides Pydantic model functionalities.
        ABC: Marks this class as an abstract base class.
    """

    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class UserSchema(BaseSchema):
    """
    v1.0.0 Schema representing a user.

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
        BaseSchema: Provides the foundation for schema validation.
    """

    id: PositiveInt
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[str] = None
    favorite_genres: Optional[str] = None

class TrackSchema(BaseSchema):
    """
    v1.0.0 Schema representing a music track.

    This schema defines the attributes relevant to a track and ensures that the
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
        BaseSchema: Provides the foundation for schema validation.
    """

    id: PositiveInt
    name: Optional[str] = None
    artist: Optional[str] = None
    songwriters: Optional[str] = None
    duration: Optional[str] = None
    genres: Optional[str] = None
    album: Optional[str] = None

class ListenHistorySchema(BaseSchema):
    """
    Schema representing the listen history of a user.

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
        BaseSchema: Provides the foundation for schema validation.
    """

    user_id: PositiveInt
    items: Optional[List[PositiveInt]] = Field(None, min_items=0)


class ApiSchema(BaseModel):
    """
    Schema representing the API response.

    This schema defines the attributes relevant to an API response,
    ensuring that pagination information is provided along with a list of items.

    Attributes:
        total (PositiveInt):
            The total number of items available.
            This field is required.
        page (PositiveInt):
            The current page number in the pagination.
            This field is required.
        size (PositiveInt):
            The number of items per page.
            This field is required.
        pages (PositiveInt):
            The total number of pages based on the total items and size.
            This field is required.
        items (List[Union[UserSchema, TrackSchema, ListenHistorySchema]]):
            A list of items included in the current response.
            Must contain a minimum of 1 item.

    Inherits:
        BaseModel: Provides Pydantic model functionalities.
    """

    total: PositiveInt
    page: PositiveInt
    size: PositiveInt
    pages: PositiveInt
    items: List[Union[UserSchema, TrackSchema, ListenHistorySchema]] = Field(..., min_items=1)
