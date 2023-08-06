from typing import Any, Dict

from synapse.config._base import Config
from synapse.module_api import ModuleApi
from synapse.module_api.errors import ConfigError

from request_digit_token._base import RequestDigitTokenBase
from request_digit_token._config import RequestDigitTokenConfig
from request_digit_token._servlets import RequestDigitTokenServlet


class RequestDigitToken(RequestDigitTokenBase):
    def __init__(self, config: RequestDigitTokenConfig, api: ModuleApi):
        RequestDigitTokenBase.__init__(self, config, api)

        self._api = api
        self._config = config

        self._api.register_web_resource(
            path="/_synapse/client/register/email",
            resource=RequestDigitTokenServlet(self._config, self._api),
        )

    @staticmethod
    def parse_config(config: Dict[str, Any]) -> RequestDigitTokenConfig:
        token_length = config.get("token_length", 6)

        if not isinstance(token_length, int):
            raise ConfigError("Config option 'token_length' is not int")

        token_lifetime = config.get("token_lifetime", "1h")

        parsed_config = RequestDigitTokenConfig(
            token_length=token_length,
            token_lifetime=Config.parse_duration(token_lifetime),
        )

        return parsed_config
