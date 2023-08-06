#!/usr/bin/env python3

import re
from pathlib import Path

import bottle

from . import routes  # noqa: F401
from .metadata import Metadata, Profile

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = "80"
USER_CONFIG_FILENAME = ".metamock.config"

# config priority:
# 1) cli argument (--config) (dict or file)
# 2) ~/.metamock.config
# 3) (MODULE_INSTALL_DIR)/default.config


class Server:
    def __init__(self, config_file=None, profile=None, debug=False):

        self.debug = debug

        if debug:
            bottle.debug(debug)

        APP_DIR = Path(__file__).parent

        VIEWS_DIR = APP_DIR / "views"
        VIEWS_DIR.resolve(strict=True)
        bottle.TEMPLATE_PATH.insert(0, str(VIEWS_DIR))

        USER_CONFIG_FILE = Path.home() / USER_CONFIG_FILENAME
        DEFAULT_CONFIG_FILE = APP_DIR / "default.config"

        self.profile = profile

        self.app = bottle.default_app()

        config_file = config_file or USER_CONFIG_FILE
        if not config_file.is_file():
            config_file = DEFAULT_CONFIG_FILE

        config_file.resolve(strict=True)
        if debug:
            print(f"{config_file=}")

        self.app.config.load_config(str(config_file))

        profile_name = profile or self.app.config.get(
            "metadata.profile", "default"
        )
        if debug:
            print(f"{profile_name=}")

        self.app.config.meta_set(
            "metadata",
            "obj",
            Metadata(self.parse_profiles(self.app.config), profile_name),
        )

    def run(self, host, port, server):

        default_host = self.app.config.get(
            "metadata.host", DEFAULT_HOST
        ).split()[0]
        default_port = self.app.config.get(
            "metadata.port", DEFAULT_PORT
        ).split()[0]

        return self.app.run(
            server=server or "wsgiref",
            debug=self.debug,
            host=host or default_host,
            port=int(port or default_port),
        )

    #    def port(self, value):
    #        value = int(value)
    #
    #        if value < 0 or value > 65535:
    #            raise argparse.ArgumentTypeError(
    #                "invalid port value: {}: value must be 0-65535".format(value))
    #
    #        return value
    #
    #
    #    def existing_file(self, value):
    #        if not Path(value).isfile():
    #            raise argparse.ArgumentTypeError(
    #                'file does not exist: {}'.format(value))
    #
    #        return value
    #
    #
    def to_int(self, value):
        return value if value is None else int(value)

    def to_bool(self, value, default=False):
        if value is None:
            return default

        return value.lower() in ("yes", "true", "y", "t", "1")

    def parse_profiles(self, config):
        prog = re.compile("^profile:([^\\.]+)\\.(.*)$")
        profiles = {}
        region = self.app.config.get("aws.region", "us-east-1")
        access_key = self.app.config.get("aws.access_key")
        secret_key = self.app.config.get("aws.secret_key")
        mfa_enabled = self.app.config.get("aws.mfa_enabled")
        mfa_secret = self.app.config.get("aws.mfa_secret")
        token_duration = self.app.config.get("metadata.token_duration")
        role_arn = self.app.config.get("metadata.role_arn")

        for key, value in config.items():
            res = prog.match(key)

            if res:
                profiles.setdefault(res.group(1), {})[res.group(2)] = value

        profiles.setdefault("default", {})

        for profile in profiles.values():
            profile.setdefault("region", region)
            profile.setdefault("access_key", access_key)
            profile.setdefault("secret_key", secret_key)
            profile["token_duration"] = self.to_int(
                profile.setdefault("token_duration", token_duration)
            )
            profile.setdefault("role_arn", role_arn)
            profile.setdefault("mfa_secret", mfa_secret)
            profile["mfa_enabled"] = self.to_bool(
                profile.setdefault("mfa_enabled", mfa_enabled), default=True
            )

        result = {}
        for name, values in profiles.items():
            try:
                result[name] = Profile(**values)
            except Exception as ex:
                raise Exception("Error loading profile {}".format(name), ex)

        return result
