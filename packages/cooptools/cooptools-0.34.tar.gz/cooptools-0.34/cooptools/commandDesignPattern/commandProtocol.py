from typing import Protocol, List
from dataclasses import dataclass
from cooptools.commandDesignPattern.exceptions import ResolveBatchException

class CommandProtocol(Protocol):
    def execute(self) -> None:
        ...

    def undo(self) -> None:
        ...

@dataclass
class CommandBatch(CommandProtocol):
    commands: List[CommandProtocol]

    def execute(self) -> None:
        successful: List[CommandProtocol] = []
        try:
            for command in self.commands:
                command.execute()
        except Exception as e:
            for command in reversed(successful):
                command.undo()
            raise ResolveBatchException(self, e)

