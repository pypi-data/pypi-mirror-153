#!/usr/bin/env python
import os
import os.path

OVERWRITE = True


def write_config(access_key=None, secret_key=None, region=None):
    metadata_dir = os.path.join(os.path.expanduser("~"), ".metamock")

    if not os.path.isdir(metadata_dir):
        os.mkdir(metadata_dir)

    key_map = {
        "AWS_ACCESS_KEY_ID": "access_key",
        "AWS_SECRET_ACCESS_KEY": "secret_key",
        "AWS_REGION": "region",
    }
    config_file = os.path.join(metadata_dir, "config")
    if OVERWRITE or not os.path.isfile(config_file):
        ofp = open(config_file, "w")
        ofp.write("[aws]\n")
        for k, v in os.environ.items():
            if k in key_map:
                ofp.write(key_map[k] + "=" + v + "\n")
        ofp.write("mfa_enabled=False\n")
        ofp.write("[metadata]\n")
        ofp.write("profile=default\n")
        ofp.close
