#!/usr/bin/env python

"""Tests for `metamock` package."""

from click.testing import CliRunner

import metamock
from metamock import __version__, cli


def test_version():
    """Test reading version and module name"""
    assert metamock.__name__ == "metamock"
    assert __version__
    assert isinstance(__version__, str)


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code != 0, result
    assert "metamock" in result.output

    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0, result
    assert "Show this message and exit." in result.output
