from enum import Enum


class Endpoints(Enum):
    """
    Enumeration of available API endpoints for the application to process.

    This class defines the various API endpoints available for the application.
    Each member represents a specific endpoint that can be used for making API
    requests. The values are the path strings corresponding to each endpoint.

    Attributes:
        TRACKS (str):
            The endpoint for track-related operations, mapped to the path '/tracks'.

        USERS (str):
            The endpoint for user-related operations, mapped to the path '/users'.

        LISTEN_HISTORY (str):
            The endpoint for listen history operations, mapped to the path '/listen_history'.
    """

    TRACKS = '/tracks'
    USERS = '/users'
    LISTEN_HISTORY = '/listen_history'