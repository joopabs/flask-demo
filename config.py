import logging
import os
import sys

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from dotenv import load_dotenv

load_dotenv()


def get_database_url():
    """Retrieves the database URL from Key Vault or environment variable."""

    USE_KEYVAULT = os.environ.get("USE_KEYVAULT", "False").lower() == "true"

    if USE_KEYVAULT:
        # Key Vault configuration
        KEY_VAULT_URL = os.environ.get("KEY_VAULT_URL")
        SECRET_NAME = os.environ.get("SECRET_NAME")

        # Authenticate with Key Vault
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

        # Retrieve the database URL from Key Vault
        try:
            secret = client.get_secret(SECRET_NAME)
            return secret.value
        except Exception as e:
            logging.critical(f"Failed to retrieve secret from Key Vault: {e}")
            sys.exit(1)
    else:
        return os.environ.get("DATABASE_URL")
