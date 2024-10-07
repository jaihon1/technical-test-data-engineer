import pytest
from pydantic import ValidationError
from src.data_flux.api_schema import UserSchema, TrackSchema, ListenHistorySchema
from src.data_flux.data_schema import (
    BaseDataSchema,
    UserDataSchema,
    TrackDataSchema,
    ListenHistoryDataSchema,
    build_user_data_schema,
    build_track_data_schema,
    build_listen_history_data_schema,
)

# Test BaseDataSchema
def test_base_data_schema_valid():
    base_data = BaseDataSchema(
        version_id=1,
        created_at="2024-10-07T10:00:00Z",
        updated_at="2024-10-07T10:00:00Z"
    )
    assert base_data.version_id == 1
    assert base_data.created_at == "2024-10-07T10:00:00Z"
    assert base_data.updated_at == "2024-10-07T10:00:00Z"

def test_base_data_schema_missing_version_id():
    with pytest.raises(ValidationError) as exc_info:
        BaseDataSchema(
            created_at="2024-10-07T10:00:00Z",
            updated_at="2024-10-07T10:00:00Z"
        )
    assert 'version_id' in str(exc_info.value)

def test_base_data_schema_default_values():
    base_data = BaseDataSchema(
        version_id=1
    )
    assert base_data.version_id == 1
    assert base_data.created_at is None
    assert base_data.updated_at is None

def test_base_data_schema_invalid_version_id():
    with pytest.raises(ValidationError) as exc_info:
        BaseDataSchema(
            version_id=-1,  # Invalid value for PositiveInt
            created_at="2024-10-07T10:00:00Z",
            updated_at="2024-10-07T10:00:00Z"
        )
    assert 'Input should be greater than 0' in str(exc_info.value)


# Test UserDataSchema
def test_user_data_schema_valid():
    user_data = UserDataSchema(
        id=1,
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        gender="male",
        favorite_genres="Rock",
        version_id=1
    )
    assert user_data.id == 1
    assert user_data.first_name == "John"
    assert user_data.version_id == 1

def test_user_data_schema_missing_id():
    with pytest.raises(ValidationError) as exc_info:
        UserDataSchema(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            gender="male",
            favorite_genres="Rock",
            version_id=1
        )
    assert 'id' in str(exc_info.value)

def test_user_data_schema_missing_version_id():
    with pytest.raises(ValidationError) as exc_info:
        UserDataSchema(
            id=1,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            gender="male",
            favorite_genres="Rock"
        )
    assert 'version_id' in str(exc_info.value)

# Test TrackDataSchema
def test_track_data_schema_valid():
    track_data = TrackDataSchema(
        id=1,
        name="Some Song",
        artist="Some Artist",
        songwriters="Some Songwriter",
        duration="3:45",
        genres="Pop",
        album="Some Album",
        version_id=1
    )
    assert track_data.id == 1
    assert track_data.name == "Some Song"
    assert track_data.artist == "Some Artist"
    assert track_data.version_id == 1

def test_track_data_schema_missing_id():
    with pytest.raises(ValidationError) as exc_info:
        TrackDataSchema(
            name="Some Song",
            artist="Some Artist",
            songwriters="Some Songwriter",
            duration="3:45",
            genres="Pop",
            album="Some Album",
            version_id=1
        )
    assert 'id' in str(exc_info.value)

def test_track_data_schema_missing_version_id():
    with pytest.raises(ValidationError) as exc_info:
        TrackDataSchema(
            id=1,
            name="Some Song",
            artist="Some Artist",
            songwriters="Some Songwriter",
            duration="3:45",
            genres="Pop",
            album="Some Album"
        )
    assert 'version_id' in str(exc_info.value)

# Test ListenHistoryDataSchema
def test_listen_history_data_schema_valid():
    listen_history_data = ListenHistoryDataSchema(
        user_id=1,
        items=[1, 2, 3],
        version_id=1
    )
    assert listen_history_data.user_id == 1
    assert listen_history_data.items == [1, 2, 3]
    assert listen_history_data.version_id == 1

def test_listen_history_data_schema_missing_user_id():
    with pytest.raises(ValidationError) as exc_info:
        ListenHistoryDataSchema(
            items=[1, 2, 3],
            version_id=1
        )
    assert 'id' in str(exc_info.value)

def test_listen_history_data_schema_missing_version_id():
    with pytest.raises(ValidationError) as exc_info:
        ListenHistoryDataSchema(
            user_id=1,
            items=[1, 2, 3]
        )
    assert 'version_id' in str(exc_info.value)

# Test build functions
def test_build_user_data_schema():
    user_schema = UserSchema(
        id=1,
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        gender="male",
        favorite_genres="Rock"
    )
    version_id = 1
    user_data = build_user_data_schema(user_schema, version_id)

    assert isinstance(user_data, UserDataSchema)
    assert user_data.id == 1
    assert user_data.version_id == 1

def test_build_track_data_schema():
    track_schema = TrackSchema(
        id=1,
        name="Some Song",
        artist="Some Artist",
        songwriters="Some Songwriter",
        duration="3:45",
        genres="Pop",
        album="Some Album"
    )
    version_id = 1
    track_data = build_track_data_schema(track_schema, version_id)

    assert isinstance(track_data, TrackDataSchema)
    assert track_data.name == "Some Song"
    assert track_data.version_id == 1

def test_build_listen_history_data_schema():
    listen_history_schema = ListenHistorySchema(
        user_id=1,
        items=[1, 2, 3]
    )
    version_id = 1
    listen_history_data = build_listen_history_data_schema(listen_history_schema, version_id)

    assert isinstance(listen_history_data, ListenHistoryDataSchema)
    assert listen_history_data.user_id == 1
    assert listen_history_data.version_id == 1
