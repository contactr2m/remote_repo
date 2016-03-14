"""App configuration for custom_user."""
from django.apps import AppConfig


class AccountsUserConfig(AppConfig):

    """Default configuration for custom_user."""
    label = 'accounts_user'
    name = 'accounts'
    verbose_name = "Custom Email User"
