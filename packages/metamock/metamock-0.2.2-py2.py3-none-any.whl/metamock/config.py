#!/usr/bin/env python


def optional(key, value):
    if value:
        return f"{key}={value}\n"
    else:
        return f"#{key}=...\n"


def write_config(
    output,
    host,
    port,
    access_key,
    secret_key,
    region,
    mfa_enabled,
    mfa_secret,
    mfa_token_duration,
    mfa_role_arn,
):
    output.write("[aws]\n")
    output.write(f"access_key={access_key}\n")
    output.write(f"secret_key={secret_key}\n")
    output.write(f"region={region}\n")
    output.write("mfa_enabled={mfa_enabled}\n")
    output.write(optional("mfa_secret", mfa_secret))
    output.write(optional("mfa_token_duration", mfa_token_duration))
    output.write(optional("mfa_role_arn", mfa_role_arn))
    output.write("[metadata]\n")
    output.write(f"host={host}\n")
    output.write(f"port={port}\n")
    output.write("profile=default\n")
