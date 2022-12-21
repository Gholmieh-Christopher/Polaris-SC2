# Written by: Christopher Gholmieh
# Imports:

# Starcraft II:
# > Position:
from sc2.position import Point2

# > Bot AI:
from sc2.bot_ai import BotAI

# > Units:
from sc2.units import Units

# > Unit:
from sc2.unit import Unit

# > IDs:
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId

# Loguru:
# > Logger:
from loguru import logger

# Typing:
import typing

# Enumerations:
from bot.enumerations import HarvesterTypes

# Core:
from bot.core import UnitController, Enumeration

# Classes:
class HarvesterController(UnitController):
    # Initialization:
    def __init__(
        self, harvester: Unit, harvester_type: Enumeration, target: Unit
    ) -> None:
        # Initialization:
        super().__init__(harvester)

        # Miscellaneous:
        self.harvester_type: Enumeration = harvester_type

        # Integers:
        self.target_identifier: int = target.tag

        # Gathering:
        harvester.gather(target)

    # Functions:
    def locate_harvester(self, AI: BotAI) -> typing.Union[Unit, None]:
        unit: typing.Union[Unit, None] = AI.workers.find_by_tag(self.unit.tag)
        if unit is None:
            logger.info("Harvester of tag {} does not exist.".format(self.unit.tag))

        return unit

    def locate_townhall(self, harvester: Unit, AI: BotAI) -> typing.Union[Unit, None]:
        unit: typing.Union[Unit, None] = AI.townhalls.closest_to(harvester)
        if unit is None:
            logger.info(
                "There is no townhall around worker of tag {}.".format(self.unit.tag)
            )

        return unit

    def locate_target(self, harvester: Unit, AI: BotAI) -> typing.Union[Unit, None]:
        if self.harvester_type == HarvesterTypes.HARVESTER_MINERAL_TYPE:
            mineral_fields: Units = AI.mineral_field.closer_than(10, harvester)
            if not any(mineral_fields):
                return None

            return mineral_fields.find_by_tag(self.target_identifier)
        else:
            refineries: Units = (
                AI.structures.of_type(UnitTypeId.REFINERY)
                .closer_than(10, harvester)
                .ready
            )
            if not any(refineries):
                return None

            return refineries.find_by_tag(self.target_identifier)

    def on_frame(self, AI: BotAI) -> None:
        # Unit Objects:
        harvester: typing.Union[Unit, None] = self.locate_harvester(AI)

        # Guardian Statement:
        if harvester is None:
            return None

        # Unit Objects:
        target: typing.Union[Unit, None] = self.locate_target(harvester, AI)

        # Guardian Statement:
        if target is None:
            return None

        # Correcting Worker:
        if (
            len(harvester.orders) > 0
            and harvester.is_gathering
            and isinstance(harvester.order_target, int)
            and harvester.order_target != self.target_identifier
        ):
            harvester.gather(target)

            return None

        # Speedmining:
        self.speedmine(harvester, target, AI)

    def speedmine(self, harvester: Unit, target: Unit, AI: BotAI) -> None:
        # Unit Objects:
        townhall: Unit = self.locate_townhall(harvester, AI)
        if townhall is None:
            return None

        # Speedmining:
        if harvester.is_returning and len(harvester.orders) == 1:
            position: Point2 = townhall.position.towards(
                harvester, townhall.radius + harvester.radius
            )

            if 0.75 < harvester.distance_to(target) < 2:
                harvester.move(position)
                harvester(AbilityId.SMART, townhall, queue=True)

                return None

        if (
            harvester.is_returning is False
            and len(harvester.orders) == 1
            and isinstance(harvester.order_target, int)
        ):
            if 0.75 < harvester.distance_to(townhall) < 2:
                harvester.move(townhall)
                harvester(AbilityId.SMART, target, queue=True)
