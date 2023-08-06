import configparser
import os
from os.path import expanduser
from typing import Dict
from typing import Optional

CFG_CREDENTIALS_DICT = {
    "ALVIN_API_TOKEN": "your_newly_generated_token",
    "ALVIN_PLATFORM_ID": "your_alvin_platform_id",
    "ALVIN_API_HOST": "https://app.alvin.ai",
    "ALVIN_UI_HOST": "https://app.alvin.ai",
    "DEBUG": "true",
    "GIT_COMPARE_BRANCH": "main",
    "DBT_ROOT_DIR": "",
    "ROOT_DIR": "",
}
USER_CONFIG_DIR = expanduser("~") + "/.alvin"
USER_CONFIG = USER_CONFIG_DIR + "/alvin.cfg"
CONFIG = configparser.ConfigParser()
GLOBAL = "GLOBAL"
CORE_SECTION = "ALVIN"


def create_cfg_file(directory_path: str) -> bool:
    config_write = configparser.ConfigParser()
    config_write.add_section(CORE_SECTION)
    config_write.add_section(GLOBAL)
    config_write[GLOBAL]["active_profile"] = CORE_SECTION

    for k, v in CFG_CREDENTIALS_DICT.items():
        config_write[CORE_SECTION][k] = v

    alvin_cfg_file_path = directory_path + "/alvin.cfg"

    if os.path.isfile(alvin_cfg_file_path):
        return True

    else:
        with open(alvin_cfg_file_path, "w") as f:
            config_write.write(f)
        return False


def current_active_project_name(config_read: configparser.ConfigParser) -> str:
    """Is active project set up? Return name if yes else None"""
    activate_profile = config_read[GLOBAL]["active_profile"]
    return activate_profile


def set_current_config_context(context: str) -> bool:
    """Set up the context in active project"""
    CONFIG.read(USER_CONFIG)
    if context in CONFIG.sections():
        CONFIG.set(GLOBAL, "active_profile", context)
        with open(USER_CONFIG, "w+") as f:
            CONFIG.write(f)
        return True
    else:
        return False


def set_key_value_in_cfg(current_section: str, key: str, value: str) -> Optional[bool]:
    """Update this function to write particular sections to the cfg file"""
    try:
        config = configparser.ConfigParser()
        config.read(USER_CONFIG)

        if os.path.isfile(USER_CONFIG):
            current_section = current_section.upper()
            if current_section not in config.sections():
                config.add_section(section=current_section)
            config.set(current_section, key, value)
            with open(USER_CONFIG, "w+") as f:
                config.write(f)
        return True

    except Exception:
        return False


def load_cfg_file() -> Dict:
    """Load credentials from cfg file"""
    config_read = configparser.ConfigParser()

    if not os.path.isfile(USER_CONFIG):
        return {}

    config_read.read(USER_CONFIG)

    if config_read:
        credentials = {}
        for k, _ in CFG_CREDENTIALS_DICT.items():
            credentials.update({k.lower(): config_read[CORE_SECTION].get(k)})
        return credentials

    return {}
