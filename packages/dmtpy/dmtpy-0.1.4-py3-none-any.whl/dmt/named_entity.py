from .entity import Entity

class NamedEntity(Entity):
    """ A Named Entity representing system/SIMOS/NamedEntity"""

    def __init__(self) -> None:
        self.__name = None

    @property
    def name(self) -> str:
        """"""
        return self.__name

    @name.setter
    def name(self, value: str):
        """Set name"""
        self.__name = str(value)
