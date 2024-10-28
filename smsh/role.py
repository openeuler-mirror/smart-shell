import json
import platform
from enum import Enum
from os import getenv, pathsep
from os.path import basename
from pathlib import Path
from typing import Optional, Dict

import typer
from click import BadArgumentUsage
from distro import name as distro_name
from smsh.config import cfg
from smsh.utils import option_callback

SHELL_ROLE = """Provide only {shell} commands for {os} without any description.
If there is a lack of details, provide most logical solution.
Ensure the output is a valid shell command.
If multiple steps required try to combine them together using &&.
Provide only plain text without Markdown formatting.
Do not provide markdown formatting such as ```.
"""

DESCRIBE_SHELL_ROLE = """请你用中文描述以下需求。
为给定的shell命令提供一个简洁的单句描述。
描述命令的每个参数和选项。
在大约80个词内提供简短的响应。
尽可能应用Markdown格式。
"""
# Provide a terse, single sentence description of the given shell command.
# Describe each argument and option of the command.
# Provide short responses in about 80 words.
# APPLY MARKDOWN formatting when possible.


ROLE_TEMPLATE = "You are {name}\n{role}"


class SystemRole:
    storage: Path = Path(cfg.get("ROLE_STORAGE_PATH"))

    def __init__(
        self,
        name: str,
        role: str,
        variables: Optional[Dict[str, str]] = None,
    ) -> None:
        self.storage.mkdir(parents=True, exist_ok=True)
        self.name = name
        if variables:
            role = role.format(**variables)
        self.role = role

    @classmethod
    def create_defaults(cls) -> None:
        cls.storage.parent.mkdir(parents=True, exist_ok=True)
        variables = {"shell": cls._shell_name(), "os": cls._os_name()}
        for default_role in (
            SystemRole("Shell Command Generator", SHELL_ROLE, variables),
            SystemRole("Shell Command Descriptor", DESCRIBE_SHELL_ROLE, variables),
        ):
            if not default_role._exists:
                default_role._save()

    @classmethod
    def get(cls, name: str) -> "SystemRole":
        file_path = cls.storage / f"{name}.json"
        if not file_path.exists():
            raise BadArgumentUsage(f'Role "{name}" not found.')
        return cls(**json.loads(file_path.read_text()))

    @classmethod
    @option_callback
    def create(cls, name: str) -> None:
        role = typer.prompt("Enter role description")
        role = cls(name, role)
        role._save()

    @classmethod
    @option_callback
    def list(cls, _value: str) -> None:
        if not cls.storage.exists():
            return
        # Get all files in the folder.
        files = cls.storage.glob("*")
        # Sort files by last modification time in ascending order.
        for path in sorted(files, key=lambda f: f.stat().st_mtime):
            typer.echo(path)

    @classmethod
    @option_callback
    def show(cls, name: str) -> None:
        typer.echo(cls.get(name).role)

    @classmethod
    def get_role_name(cls, initial_message: str) -> Optional[str]:
        if not initial_message:
            return None
        message_lines = initial_message.splitlines()
        if "You are" in message_lines[0]:
            return message_lines[0].split("You are ")[1].strip()
        return None

    @classmethod
    def _os_name(cls) -> str:
        current_platform = platform.system()
        if current_platform == "Linux":
            return "Linux/" + distro_name(pretty=True)
        if current_platform == "Windows":
            return "Windows " + platform.release()
        if current_platform == "Darwin":
            return "Darwin/MacOS " + platform.mac_ver()[0]
        return current_platform

    @classmethod
    def _shell_name(cls) -> str:
        current_platform = platform.system()
        if current_platform in ("Windows", "nt"):
            is_powershell = len(getenv("PSModulePath", "").split(pathsep)) >= 3
            return "powershell.exe" if is_powershell else "cmd.exe"
        return basename(getenv("SHELL", "/bin/sh"))

    @property
    def _exists(self) -> bool:
        return self._file_path.exists()

    @property
    def _file_path(self) -> Path:
        return self.storage / f"{self.name}.json"

    def _save(self) -> None:
        if self._exists:
            typer.confirm(
                f'Role "{self.name}" already exists, overwrite it?',
                abort=True,
            )

        self.role = ROLE_TEMPLATE.format(name=self.name, role=self.role)
        self._file_path.write_text(json.dumps(self.__dict__), encoding="utf-8")

    def same_role(self, initial_message: str) -> bool:
        if not initial_message:
            return False
        return True if f"You are {self.name}" in initial_message else False


class DefaultRoles(Enum):
    SHELL = "Shell Command Generator"
    DESCRIBE_SHELL = "Shell Command Descriptor"

    @classmethod
    def check_get(cls, shell: bool, describe_shell: bool) -> SystemRole:
        if shell:
            return SystemRole.get(DefaultRoles.SHELL.value)
        if describe_shell:
            return SystemRole.get(DefaultRoles.DESCRIBE_SHELL.value)
        else:
            raise BadArgumentUsage("No role selected.")

    def get_role(self) -> SystemRole:
        return SystemRole.get(self.value)


SystemRole.create_defaults()
