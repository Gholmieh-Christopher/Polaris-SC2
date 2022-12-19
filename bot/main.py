# Written by: Christopher Gholmieh
# Imports:

# Starcraft II:
# > Bot AI:
from sc2.bot_ai import BotAI, Race

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

    # Functions:
    async def on_start(self) -> None:
        # Manager References:
        self.TownhallManager: TownhallManager = TownhallManager()

        # Installing Supervisors:
        self.TownhallManager.assign_supervisor(self.townhalls.first)

    async def on_step(self, iteration: int) -> None:
        # Updating Managers:
        self.TownhallManager.update_supervisors(self)
