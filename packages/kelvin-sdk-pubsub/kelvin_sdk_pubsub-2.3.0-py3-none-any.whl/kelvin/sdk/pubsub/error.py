"""Exceptions."""


class PubSubError(Exception):
    """General pub-sub error."""


class ConnectionError(PubSubError):
    """Connection error."""
