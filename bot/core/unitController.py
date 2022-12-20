# Written by: Christopher Gholmieh
# Imports:

# Starcraft II:
# > Bot AI:
from sc2.bot_ai import BotAI

# > Unit:
from sc2.unit import Unit

# Loguru:
# > Logger:
from loguru import logger

# Classes:
class UnitController:
    # Initialization:
    def __init__(self, unit: Unit):
        # Unit Objects:
        self.unit: Unit = unit

    # Functions:
    def on_frame(self, AI: BotAI) -> None:
        return None
