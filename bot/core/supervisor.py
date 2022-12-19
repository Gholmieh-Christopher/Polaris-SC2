# Written by: Christopher Gholmieh
# Imports:

# Starcraft II:
# > Bot AI:
from sc2.bot_ai import BotAI

# Loguru:
# > Logger:
from loguru import logger

# Classes:
class Supervisor:
    # Initialization:
    def __init__(self) -> None:
        pass

    # Functions:
    def update(self, AI: BotAI, *args, **kwargs) -> None:
        logger.info("Supervisor update function called.")
