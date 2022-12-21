# Written by: Christopher Gholmieh
# Imports:

# Starcraft II:
# > Bot AI:
from sc2.bot_ai import BotAI, Race

# > Unit:
from sc2.unit import Unit

# Managers:
from .managers import TownhallManager

# Classes:
class PolarisSC2(BotAI):
    # Configuration:
    RACE: Race = Race.Terran

    NAME: str = "CompetitiveBot"

    # Initialization:
    def __init__(self) -> None:
        pass

    # Events:
    async def on_building_construction_complete(self, unit: Unit) -> None:
        # Installing Supervisors:
        if unit.name == "CommandCenter":
            self.TownhallManager.assign_supervisor(unit, self)

    async def on_unit_destroyed(self, identifier: int) -> None:
        # Updating Managers:
        self.TownhallManager.on_unit_death(identifier)

    # Functions:
    async def on_start(self) -> None:
        # Manager References:
        self.TownhallManager: TownhallManager = TownhallManager()

        # Installing Supervisors:
        self.TownhallManager.assign_supervisor(self.townhalls.first, self)

    async def on_step(self, iteration: int) -> None:
        # Updating Supervisors:
        self.TownhallManager.update_supervisors(self)
