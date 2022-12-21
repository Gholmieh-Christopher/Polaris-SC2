# Written by: Christopher Gholmieh
# Imports:

# Starcraft II:
# > Bot AI:
from sc2.bot_ai import BotAI

# > Unit:
from sc2.unit import Unit

# Typing:
import typing

# Classes:
class Manager:
    # Initialization:
    def __init__(self, Supervisor: typing.Callable) -> None:
        # Miscellaneous:
        self.Supervisor: typing.Callable = Supervisor

        # Dictionaries:
        self.supervisors: dict = {}

    # Functions:
    def unassign_supervisor(self, identifier: int) -> None:
        # Guardian Statement:
        if identifier not in self.supervisors:
            return None
        del self.supervisors[identifier]

        self.on_unassignment(identifier)

    def assign_supervisor(self, unit: Unit, *args, **kwargs) -> None:
        self.supervisors[unit.tag] = self.Supervisor(unit, *args, **kwargs)

        self.on_assignment(unit, *args, **kwargs)

    def update_supervisors(self, AI: BotAI) -> None:
        for Supervisor in self.supervisors.values():
            Supervisor.on_frame(AI)

    # Events:
    def on_unassignment(self, identifier: int) -> None:
        return None

    def on_assignment(self, unit: Unit, *args, **kwargs) -> None:
        return None

    # Hooks:
    def on_unit_death(self, identifier: int) -> None:
        return None
