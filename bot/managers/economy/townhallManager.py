# Written by: Christopher Gholmieh
# Imports:

# Starcraft II:
# > Unit:
from sc2.unit import Unit

# Loguru:
# > Logger:
from loguru import logger

# Supervisors:
from bot.supervisors import TownhallSupervisor

# Core:
from bot.core import Manager

# Classes:
class TownhallManager(Manager):
    # Initialization:
    def __init__(self) -> None:
        # Initialization:
        super().__init__(TownhallSupervisor)

    def on_assignment(self, unit: Unit, *args, **kwargs) -> None:
        logger.info("Assigned!")
