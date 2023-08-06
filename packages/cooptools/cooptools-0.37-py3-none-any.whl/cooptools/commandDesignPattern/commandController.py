from dataclasses import dataclass, field
from cooptools.commandDesignPattern.commandProtocol import CommandProtocol
from cooptools.commandDesignPattern.exceptions import ResolveStateException
from typing import List

@dataclass
class CommandController:

    registered_stack: List[CommandProtocol] = field(default_factory=list)
    redo_stack: List[CommandProtocol] = field(default_factory=list)
    cursor: int = -1

    def register(self, commands: List[CommandProtocol]) -> None:
        # delete any registered commands after the current cursor
        del self.registered_stack[self.cursor + 1:]

        # add new commands
        self.registered_stack += commands

        # increment cursor
        self.cursor += len(commands)

    def resolve_state(self, revert_on_fail: bool = True) -> None:
        successful: List[CommandProtocol] = []
        command = None

        try:
            # execute the commands in the stack up to the cursor
            for command in self.registered_stack[:self.cursor + 1]:
                command.execute()
                successful.append(command)

        except Exception as e:
            # undo the commands that were successful
            if revert_on_fail:
                for ucommand in reversed(successful):
                    ucommand.undo()

            # raise the exception on the command that failed
            raise ResolveStateException(command=command, inner=e)

    def undo(self):
        # move cursor back in time
        if self.cursor > 0: self.cursor -= 1

    def redo(self):
        # move cursor forward in time
        if self.cursor < len(self.registered_stack): self.cursor += 1
