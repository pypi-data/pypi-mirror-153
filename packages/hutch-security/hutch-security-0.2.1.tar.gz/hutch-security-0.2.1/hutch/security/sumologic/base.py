"""Provides a base SumoLogic client implementation for use by other wrappers."""

from sumologic import SumoLogic  # Via the SumoLogic SDK.

from hutch.security.sumologic.constants import API_ENDPOINT


class Client:
    """Provides a base SumoLogic client."""

    def __init__(self, access_id: str, access_key: str, api_url: str = API_ENDPOINT):
        """Initialise a generic SumoLogic client.

        :param access_id: The SumoLogic access ID to authenticate with.
        :param access_key: The SumoLogic access key to authenticate with.
        :param api_url: The SumoLogic API endpoint to interact with.
        """
        self.client = SumoLogic(access_id, access_key, endpoint=api_url)
