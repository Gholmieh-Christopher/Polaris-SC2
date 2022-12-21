# Written by: Christopher Gholmieh
# Imports:
import typing

# Starcraft II:
# > Bot AI:
from sc2.bot_ai import BotAI

# > Units:
from sc2.units import Units

# > Unit:
from sc2.unit import Unit

# > IDs:
from sc2.ids.unit_typeid import UnitTypeId

# Loguru:
# > Logger:
from loguru import logger

# Typing:
import typing

# Enumerations:
from bot.enumerations import HarvesterTypes

# Controllers:
from bot.controllers import HarvesterController

# Core:
from bot.core import Supervisor

# Classes:
class TownhallSupervisor(Supervisor):
    # Initialization:
    def __init__(self, townhall: Unit, AI: BotAI) -> None:
        # Initialization:
        super().__init__()

        # Dictionaries:
        self.unit_controllers: dict = {}

        self.mineral_cache: dict = {}
        self.mineral_count: dict = {}

        self.vespene_cache: dict = {}
        self.vespene_count: dict = {}

        # Integers:
        self.townhall_identifier: int = townhall.tag

        # Unit Objects:
        mineral_fields: Units = AI.mineral_field.closer_than(10, townhall)

        harvesters: Units = AI.workers.closer_than(10, townhall)

        if not any(mineral_fields):
            return None

        if not any(harvesters):
            return None

        for harvester in harvesters:
            self.allocate_position(harvester, AI)

    # Functions:
    def allocate_position(self, harvester: Unit, AI: BotAI) -> None:
        townhall: typing.Union[Unit, None] = self.locate_townhall(AI)
        if townhall is None:
            return None

        mineral_fields: Units = AI.mineral_field.closer_than(10, townhall).filter(
            lambda mineral_field: self.mineral_count.get(mineral_field.tag, 0) < 2
        )

        if not any(mineral_fields):
            # TODO: Alllocate workers to refineries.
            refineries: Units = (
                AI.structures.of_type(UnitTypeId.REFINERY)
                .closer_than(10, townhall)
                .ready.filter(
                    lambda refinery: self.vespene_count.get(refinery.tag, 0) < 3
                )
            )
            if not any(refineries):
                # TODO: Something with worker, make harvester work at next base?
                return None

            _refinery: Unit = refineries.closest_to(harvester)

            # Caching:
            self.unit_controllers[harvester.tag] = HarvesterController(
                harvester, HarvesterTypes.HARVESTER_VESPENE_TYPE, _refinery
            )

            self.vespene_count[_refinery.tag] = (
                self.vespene_count.get(_refinery.tag, 0) + 1
            )
            self.vespene_cache[harvester.tag] = _refinery.tag

        mineral_field: Unit = mineral_fields.closest_to(harvester)

        # Caching:
        self.unit_controllers[harvester.tag] = HarvesterController(
            harvester, HarvesterTypes.HARVESTER_MINERAL_TYPE, mineral_field
        )

        self.mineral_count[mineral_field.tag] = (
            self.mineral_count.get(mineral_field.tag, 0) + 1
        )
        self.mineral_cache[harvester.tag] = mineral_field.tag

    def locate_townhall(self, AI: BotAI) -> typing.Union[Unit, None]:
        townhall: typing.Union[Unit, None] = AI.townhalls.find_by_tag(
            self.townhall_identifier
        )
        if townhall is None:
            logger.info(
                "Townhall of tag {} does not exist.".format(self.townhall_identifier)
            )

        return townhall

    def delete_entry(self, harvester_identifier: int) -> None:
        harvester_controller: typing.Union[
            HarvesterController, None
        ] = self.unit_controllers.get(harvester_identifier)

        if harvester_controller is None:
            return None

        del self.unit_controllers[harvester_identifier]

        if harvester_controller.harvester_type == HarvesterTypes.HARVESTER_MINERAL_TYPE:
            self.mineral_count[self.mineral_cache[harvester_identifier]] -= 1
            del self.mineral_cache[harvester_identifier]
        else:
            self.vespene_count[self.vespene_cache[harvester_identifier]] -= 1
            del self.vespene_cache[harvester_identifier]

    def on_frame(self, AI: BotAI, *args, **kwargs) -> None:
        # Unit Objects:
        townhall: typing.Union[Unit, None] = self.locate_townhall(AI)

        # Guardian Statement:
        if townhall is None:
            return None

        mineral_fields: Units = AI.mineral_field.closer_than(10, townhall)
        refineries: Units = (
            AI.structures.of_type(UnitTypeId.REFINERY).closer_than(10, townhall).ready
        )

        # Iterating:
        for harvester in AI.workers:
            harvester_controller: typing.Union[
                HarvesterController, None
            ] = self.unit_controllers.get(harvester.tag)

            # Recruitment:
            if (
                harvester_controller is None
                and harvester.is_gathering
                and isinstance(harvester.order_target, int)
                and harvester.order_target in [*mineral_fields.tags, *refineries.tags]
                and harvester.distance_to(townhall) < 8
            ):
                self.allocate_position(harvester, AI)

                continue

            # Harvester Cleanup:
            if (
                harvester.distance_to(townhall) > 8
                or harvester.is_attacking
                or harvester.is_constructing_scv
            ) and (self.unit_controllers.get(harvester.tag) is not None):
                self.delete_entry(harvester.tag)

            # Main:
            if harvester_controller is not None:
                harvester_controller.on_frame(AI)
