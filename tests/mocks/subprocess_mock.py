from unittest.mock import Mock
import subprocess
from typing import Any, List, Union


class SubprocessMock:
    def __init__(self):
        self.run = Mock(side_effect=self._run)

    def _run(self, command: Union[str, List[str]], check: bool = False,
             shell: bool = False) -> subprocess.CompletedProcess:
        if not isinstance(command, (str, list)):
            raise ValueError("Command must be a string or a list of strings")
        if not isinstance(check, bool):
            raise ValueError("Check must be a boolean")
        if not isinstance(shell, bool):
            raise ValueError("Shell must be a boolean")

        if isinstance(command, list):
            command_str = ' '.join(command)
        else:
            command_str = command

        print(f"Mocked subprocess run: {command_str}, check={check}, shell={shell}")

        return subprocess.CompletedProcess(args=command, returncode=0)

    def set_side_effect(self, side_effect: Any) -> None:
        self.run.side_effect = side_effect
