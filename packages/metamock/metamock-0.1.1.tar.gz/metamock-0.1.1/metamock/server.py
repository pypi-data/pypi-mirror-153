#!/usr/bin/env python

import re
import sys
from pathlib import Path

from .metadata import Metadata, Profile, bottle

APP_DIR = Path(__file__).parent
bottle.TEMPLATE_PATH.append(str(Path(APP_DIR) / "metadata" / "views"))
DEFAULT_CONFIG_FILE = Path(APP_DIR) / "metamock.config"
sys.path.append(APP_DIR)


class Server:
    def __init__(self, config, host, port, profile):

        self.host = host
        self.port = port
        self.profile = profile

        self.app = bottle.default_app()

        self.app.config.load_config(config or DEFAULT_CONFIG_FILE)

        user_config = Path.home() / ".metamock" / "config"
        if user_config.is_file():
            self.app.config.load_config(str(user_config))

        profile_name = profile or self.app.config.get(
            "metadata.profile", "default"
        )

        self.app.config.meta_set(
            "metadata",
            "obj",
            Metadata(self.parse_profiles(self.app.config), profile_name),
        )

    def run(self):
        return self.app.run(
            host=self.host
            or self.app.config.get("metadata.host", "169.254.169.254"),
            port=self.port or int(self.app.config.get("metadata.port", 45000)),
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
