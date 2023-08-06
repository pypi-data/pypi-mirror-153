import os
from typing import Optional, DefaultDict

from algoralabs.decorators.configuration import configuration
from algoralabs.gData import config_file


@configuration
class Auth:
    # Feature to keep values hidden from printing (not totally)
    # Allows for dynamic rendering of auth values
    @property
    def username(self) -> Optional[str]:
        return os.getenv("ALGORA_USER", None)

    @property
    def password(self) -> Optional[str]:
        return os.getenv("ALGORA_PWD", None)

    @property
    def token(self) -> Optional[str]:
        return os.getenv("AUTH_TOKEN", None)

    def can_authenticate(self) -> bool:
        auth_options = self.token or (self.username and self.password)
        return auth_options is not None

    def __eq__(self, other):
        return (
            self.token == other.toker and
            self.username == self.username and
            self.password == self.password
        )


@configuration(yaml_file=config_file, prefix="")
class AppConfig:
    app_name: str
    environment: str
    version: str


app_config = AppConfig()


@configuration(yaml_file=config_file, prefix=app_config.environment)
class EnvironmentConfig:
    urls: dict
    auth_config: Auth = Auth()

    def get_url(self, key="algora"):
        return self.urls.get(key, self.urls["algora"])

