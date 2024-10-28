from unittest import TestCase
from unittest.mock import ANY, patch

import typer
from typer.testing import CliRunner

from smsh.__version__ import __version__
from smsh.app import main
from smsh.config import cfg

runner = CliRunner()
app = typer.Typer()
app.command()(main)


class SimpleTest(TestCase):
    @classmethod
    def setUpClass(cls):
        assert cfg.get("DISABLE_STREAMING") == "false"
        assert cfg.get("DEFAULT_MODEL") == "gpt-4o"

    @staticmethod
    def get_arguments(prompt, **kwargs):
        arguments = [prompt]
        for key, value in kwargs.items():
            arguments.append(key)
            if isinstance(value, bool):
                continue
            arguments.append(value)
        return arguments

    def test_shell(self):
        dict_arguments = {
            "prompt": "make a commit using git",
        }
        result = runner.invoke(app, self.get_arguments(**dict_arguments))
        assert "git commit" in result.stdout

    def test_describe_shell(self):
        dict_arguments = {
            "prompt": "ls",
            "--describe-shell": True,
        }
        result = runner.invoke(app, self.get_arguments(**dict_arguments))
        assert result.exit_code == 0
        assert "ls" in result.stdout.lower()

    @patch("smsh.handler.Handler.get_completion")
    def test_model_option(self, mocked_get_completion):
        dict_arguments = {
            "prompt": "make a commit using git",
            "--model": "gpt-4",
        }
        result = runner.invoke(app, self.get_arguments(**dict_arguments))
        mocked_get_completion.assert_called_once_with(
            messages=ANY,
            model="gpt-4",
            temperature=0.0,
            top_p=1.0,
        )
        assert result.exit_code == 0

    def test_version(self):
        dict_arguments = {
            "prompt": "",
            "--version": True,
        }
        result = runner.invoke(app, self.get_arguments(**dict_arguments), input="d\n")
        assert __version__ in result.stdout

    def test_help(self):
        dict_arguments = {
            "prompt": "",
            "--help": True,
        }
        result = runner.invoke(app, self.get_arguments(**dict_arguments))
        assert result.exit_code == 0

    def test_config(self):
        dict_arguments = {
            "prompt": "",
            "--config": True,
        }

        result = runner.invoke(app, self.get_arguments(**dict_arguments))
        assert "DEFAULT_MODEL" in result.stdout
