from pydantic import ValidationError
import pytest
from src.data_flux.api_schema import ApiSchema, BaseSchema, ListenHistorySchema, TrackSchema, UserSchema


def test_base_schema_creation_with_optional_fields():
    # Test creation with no fields provided
    base_schema = BaseSchema()
    assert base_schema.created_at is None
    assert base_schema.updated_at is None

    # Test creation with specific fields
    test_created_at = "2024-10-07T12:00:00"
    test_updated_at = "2024-10-08T12:00:00"

    base_schema_with_data = BaseSchema(created_at=test_created_at, updated_at=test_updated_at)

    assert base_schema_with_data.created_at == test_created_at
    assert base_schema_with_data.updated_at == test_updated_at

def test_base_schema_invalid_data():
    # Since there are no strict types for created_at and updated_at, we expect no validation errors for incorrect types.
    with pytest.raises(ValidationError):
        BaseSchema(created_at=123)  # created_at should be a string

    with pytest.raises(ValidationError):
        BaseSchema(updated_at=456)  # updated_at should be a string


# Unit tests for UserSchema
def test_user_schema_validation():
    # Test valid data
    user_data = {
        "id": 42,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "gender": "male",
        "favorite_genres": "rock"
    }

    user = UserSchema(**user_data)

    assert user.id == 42
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.gender == "male"
    assert user.favorite_genres == "rock"

def test_user_schema_missing_required_fields():
    # Test missing required field
    with pytest.raises(ValidationError) as excinfo:
        UserSchema(first_name="John")

    assert "id" in str(excinfo.value)

def test_user_schema_with_invalid_id():
    # Test invalid ID
    with pytest.raises(ValidationError) as excinfo:
        UserSchema(id=-1, first_name="John")  # Invalid positive integer
    assert "Input should be greater than 0" in str(excinfo.value)

def test_user_schema_with_optional_fields():
    # Test optional fields with None values
    user_data = {"id": 2}
    user = UserSchema(**user_data)

    assert user.first_name is None
    assert user.last_name is None
    assert user.email is None
    assert user.gender is None
    assert user.favorite_genres is None


# Unit tests for TrackSchema
def test_track_schema_validation():
    # Test valid data
    track_data = {
        "id": 42,
        "name": "Song Title",
        "artist": "Artist Name",
        "songwriters": "Songwriter 1, Songwriter 2",
        "duration": "3:45",
        "genres": "rock",
        "album": "Album Name"
    }

    track = TrackSchema(**track_data)

    assert track.id == 42
    assert track.name == "Song Title"
    assert track.artist == "Artist Name"
    assert track.songwriters == "Songwriter 1, Songwriter 2"
    assert track.duration == "3:45"
    assert track.genres == "rock"
    assert track.album == "Album Name"

def test_track_schema_missing_required_fields():
    # Test missing required field
    with pytest.raises(ValidationError) as excinfo:
        TrackSchema(name="Song Title")

    assert "id" in str(excinfo.value)

def test_track_schema_with_invalid_id():
    # Test invalid ID
    with pytest.raises(ValidationError) as excinfo:
        TrackSchema(id=-1, name="Song Title")  # Invalid positive integer

    assert "Input should be greater than 0" in str(excinfo.value)

def test_track_schema_with_optional_fields():
    # Test optional fields with None values
    track_data = {"id": 2}
    track = TrackSchema(**track_data)

    assert track.name is None
    assert track.artist is None
    assert track.songwriters is None
    assert track.duration is None
    assert track.genres is None
    assert track.album is None


# Unit tests for ListenHistorySchema
def test_listen_history_schema_validation():
    # Test valid data
    history_data = {
        "user_id": 1,
        "items": [1, 2, 3]
    }

    history = ListenHistorySchema(**history_data)

    assert history.user_id == 1
    assert history.items == [1, 2, 3]

def test_listen_history_schema_missing_required_fields():
    # Test missing required field
    with pytest.raises(ValidationError) as excinfo:
        ListenHistorySchema(items=[1, 2, 3])

    assert "user_id" in str(excinfo.value)

def test_listen_history_schema_with_invalid_user_id():
    # Test invalid user_id
    with pytest.raises(ValidationError) as excinfo:
        ListenHistorySchema(user_id=-1, items=[1, 2, 3])  # Invalid positive integer

    assert "Input should be greater than 0" in str(excinfo.value)

def test_listen_history_schema_with_optional_fields():
    # Test optional items with None values
    history_data = {"user_id": 2}
    history = ListenHistorySchema(**history_data)

    assert history.items is None

def test_listen_history_schema_with_empty_items():
    # Test items as an empty list (should be valid)
    history_data = {"user_id": 3, "items": []}
    history = ListenHistorySchema(**history_data)

    assert history.items == []

# Unit tests for ApiSchema
def test_api_schema_validation():
    # Test valid data
    api_data = {
        "total": 100,
        "page": 1,
        "size": 10,
        "pages": 10,
        "items": [
            {"id": 1, "first_name": "John", "last_name": "Doe"},
            {"id": 2, "first_name": "Jane", "last_name": "Doe"}
        ]
    }

    api_response = ApiSchema(**api_data)

    assert api_response.total == 100
    assert api_response.page == 1
    assert api_response.size == 10
    assert api_response.pages == 10
    assert len(api_response.items) == 2

def test_api_schema_missing_required_fields():
    # Test missing required fields
    with pytest.raises(ValidationError) as excinfo:
        ApiSchema(items=[])  # Missing total, page, size, pages

    assert "total" in str(excinfo.value)
    assert "page" in str(excinfo.value)
    assert "size" in str(excinfo.value)
    assert "pages" in str(excinfo.value)

def test_api_schema_with_empty_items():
    # Test empty items list (should raise validation error)
    with pytest.raises(ValidationError) as excinfo:
        ApiSchema(total=10, page=1, size=5, pages=2, items=[])

    assert "List should have at least 1 item" in str(excinfo.value)  # Update this assertion


def test_api_schema_with_invalid_values():
    # Test invalid values for total, page, size, pages
    with pytest.raises(ValidationError) as excinfo:
        ApiSchema(total=-1, page=0, size=-5, pages=0, items=[{"id": 1, "first_name": "John", "last_name": "Doe"}])

    assert "Input should be greater than 0" in str(excinfo.value)
