# Written by: Christopher Gholmieh
# Imports:

# Classes:
class Enumeration:
    # Initialization:
    def __init__(self, value: int, name: str) -> None:
        # Integers:
        self._value: int = value

        # Strings:
        self._name = name

    # Functions:
    @property
    def value(self) -> int:
        return self._value

    @property
    def name(self) -> str:
        return self._name

    # Methods:
    def __eq__(self, other_enumeration) -> bool:
        return (
            self.value == other_enumeration.value
            and self.name == other_enumeration.name
        )
