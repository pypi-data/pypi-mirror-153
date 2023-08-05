from typing import Any


class MetabaseLoginError(ConnectionError):
    def __init__(self, credentials_info: dict, error_details: Any):
        msg = "Connection to Metabase failed!\n"
        msg += f"Credentials: {credentials_info}\n"
        msg += f"Details: {error_details}\n"
        super().__init__(msg)


class SuperuserCredentialsRequired(AssertionError):
    def __init__(self, credentials_info: dict, error_details: Any):
        msg = "Superuser credentials are required!\n"
        msg += f"Credentials: {credentials_info}\n"
        msg += f"Details: {error_details}\n"
        super().__init__(msg)


class EncryptionSecretKeyRequired(AssertionError):
    """
    Raised when missing the encryption secret key while it was required.
    """

    def __init__(self, credentials_info: dict, error_details: Any):
        msg = "Encryption secret key is required!\n"
        msg += f"Credentials: {credentials_info}\n"
        msg += f"Details: {error_details}\n"
        super().__init__(msg)
