from alvin_api_client import ApiClient
from alvin_api_client import Configuration
from alvin_api_client.api.default_api import DefaultApi

from alvin_cli.config import settings

alvin_ui_host = settings.alvin_ui_host
alvin_api_token = settings.alvin_api_token
alvin_platform_id = settings.alvin_platform_id

configuration = Configuration.get_default_copy()
configuration.host = settings.alvin_api_host
configuration.discard_unknown_keys = True
configuration.check_type = False
api_client = ApiClient(
    configuration=configuration,
    header_name="X-API-KEY",
    header_value=alvin_api_token,
)
configuration = configuration
default_api = DefaultApi(api_client)
