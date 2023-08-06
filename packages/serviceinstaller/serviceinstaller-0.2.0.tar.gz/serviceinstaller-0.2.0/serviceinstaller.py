"""
A flexible service installer, currently compatible with Linux Systemd.
"""

# Standard library imports
import collections
import collections.abc
import copy
import configparser
import getpass
import logging
from pathlib import Path
import os
import subprocess
import sys


COMMAND_TIMEOUT = 60


# --- Utility functions ---
def update_dict_recursive(base, update):
    for update_key, update_value in update.items():
        base_value = base.get(update_key, {})
        if not isinstance(base_value, collections.abc.Mapping):
            base[update_key] = update_value
        elif isinstance(update_value, collections.abc.Mapping):
            base[update_key] = update_dict_recursive(
                base_value, update_value)
        else:
            base[update_key] = update_value
    return base


def get_actual_username():
    try:
        username = os.environ["SUDO_USER"]
        if username:
            return username
    except KeyError:
        pass
    return getpass.getuser()


# --- Module level constants ---
__version__ = "0.2.0"

PlatformConfig = collections.namedtuple(
    "PlatformConfig",
    ("full_name", "install_path", "configparser_options", "default_contents"))

INSTALL_PATH_SYSTEMD = Path("/etc") / "systemd" / "system"

CONFIGPARSER_OPTIONS_SYSTEMD = {
    "delimiters": ("=", ),
    "comment_prefixes": ("#", ),
    "empty_lines_in_values": False,
    }

DEFAULT_CONTENTS_SYSTEMD = {
    "Unit": {
        "After": "multi-user.target",
        },
    "Service": {
        "Type": "simple",
        "Restart": "on-failure",
        "User": get_actual_username(),
        },
    "Install": {
        "WantedBy": "multi-user.target",
        },
    }

SUPPORTED_PLATFORMS = {
    "linux": PlatformConfig(
        "Linux (systemd)", INSTALL_PATH_SYSTEMD, CONFIGPARSER_OPTIONS_SYSTEMD,
        DEFAULT_CONTENTS_SYSTEMD),
    }


# --- Main functions ---
def get_platform_config(platform=None):
    if platform is None:
        platform = sys.platform
    platform_config = None
    for plat_name, plat_config in SUPPORTED_PLATFORMS.items():
        if platform.startswith(plat_name):
            platform_config = plat_config
            break
    if platform_config is None:
        raise ValueError(
            "Service installation only currently supported on "
            f"{list(SUPPORTED_PLATFORMS.keys())}, not on {platform}.")
    return platform_config


def generate_systemd_config(config_dict, platform=None):
    platform_config = get_platform_config(platform)
    service_config = configparser.ConfigParser(
        **platform_config.configparser_options)
    # Make configparser case sensitive
    service_config.optionxform = str
    config_dict = update_dict_recursive(
        copy.deepcopy(platform_config.default_contents), config_dict)
    service_config.read_dict(config_dict)
    return service_config


def write_systemd_config(
        service_config,
        filename,
        platform=None,
        output_path=None,
        ):
    platform_config = get_platform_config(platform)
    if output_path is None:
        output_path = platform_config.install_path
    output_path = Path(output_path)
    os.makedirs(output_path, mode=0o755, exist_ok=True)
    output_file_path = output_path / filename

    with open(output_file_path, mode="w",
              encoding="utf-8", newline="\n") as service_file:
        service_config.write(service_file)

    os.chmod(output_file_path, 0o644)
    try:
        os.chown(output_file_path, 0, 0)
    except PermissionError:
        logging.warning(
            "Warning: Could not change owner of service file to root due to "
            "insufficient permissions (needs sudo).")
        logging.debug("Error details:", exc_info=True)
    except AttributeError:
        logging.warning(
            "Warning: Could not change owner of service file to root because "
            "chown is not supported on this operating system.")
        logging.debug("Error details:", exc_info=True)

    return output_path


def install_service(
        service_settings,
        service_filename,
        services_enable=None,
        services_disable=None,
        platform=None,
        output_path=None,
        skip_enable=False,
        ):
    """
    Install a service with the given settings to the given filename.

    Currently only supports Linux Systemd.

    Parameters
    ----------
    service_settings : dict of str: any
        Dictionary, potentially ntested, of the settings for the service.
        Varies by service platform; for systemd, will contain the parameters
        listed in a standard service unit file. Applied on top of the defaults.
    service_filename : str, optional
        What to name the resulting service file (as needed),
        including any extension. The default is None.
    services_enable : list-like, optional
        Services to manually enable along with this one. The default is None.
    services_disable : list-like, optional
        Services to manually disable along with this one. The default is None.
    platform : str, optional
        Platform to install the service on. Currently, only ``linux`` suported.
        By default, will be detected automatically.
    output_path : pathlib.Path or str, optional
        The path to which to write the generated service.
        By default, will be the standard location for the selected platform.
    skip_enable : bool, optional
        Skip enabling/disabling services, just generate/write the service file.
        Useful for testing purposes on non-native systems.

    Returns
    -------
    pathlib.Path
        The output path to which the service file was written.

    """
    if services_enable is None:
        services_enable = []
    if services_disable is None:
        services_disable = []
    if output_path is not None:
        output_path = Path(output_path)

    logging.debug("Installing %s service...", service_filename)
    platform_config = get_platform_config(platform)
    logging.debug("Using platform config settings: %s", platform_config)
    logging.debug("Generating service configuration file...")
    service_config = generate_systemd_config(service_settings, platform)


    logging.debug(
        "Writing service configuration file to %s",
        (output_path or platform_config.install_path) / service_filename)
    output_path = write_systemd_config(
        service_config,
        service_filename,
        platform=platform,
        output_path=output_path,
        )

    if not skip_enable:

        logging.debug("Reloading systemd daemon...")
        subprocess.run(
            ["systemctl", "daemon-reload"],
            timeout=COMMAND_TIMEOUT,
            check=True,
            )

        for service in services_disable:
            logging.debug("Disabling %s (if enabled)...", service)
            subprocess.run(
                ["systemctl", "disable", service],
                timeout=COMMAND_TIMEOUT,
                check=False,
                )

        for service in [*services_enable, service_filename]:
            logging.debug("Enabling %s...", service)
            subprocess.run(
                ["systemctl", "enable", service],
                timeout=COMMAND_TIMEOUT,
                check=True,
                )

    logging.info("Successfully installed %s service to %s",
                 service_filename, output_path)

    return output_path
