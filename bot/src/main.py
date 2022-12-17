# Written by: Christopher Gholmieh
# Imports:

# Starcraft II:
# > Bot AI:
from sc2.bot_ai import BotAI, Race

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
        pass

    async def on_step(self, iteration: int) -> None:
        pass
