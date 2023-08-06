from google.cloud import secretmanager

from ssb_altinn3_util.clients.decorators.simple_exception_wrapper import (
    exception_handler,
)


class SecretManagerClient:
    def __init__(self):
        self.client = secretmanager.SecretManagerServiceClient()

    @exception_handler("Secret Client")
    def get_secret(self, secret_path: str):
        """
        Attempts to fetch a secret from GCP Secret manager using credentials of current user.

        :param secret_path: Path to the secret in format: projects/{PROJECT_ID}/secrets/{SECRET_ID}/versions/latest
        :return: the secret
        """
        encoded = self.client.access_secret_version(name=secret_path)
        return encoded.payload.data.decode("UTF-8")
