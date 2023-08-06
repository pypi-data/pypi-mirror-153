from dataclasses import dataclass
from ergast_py.models.constructor import Constructor

from ergast_py.models.driver import Driver

@dataclass
class DriverStanding:
    """
    Representation of a Formula One Driver's standing in a Season
    Driver Standings may contain:
        position: Integer
        positionText: String
        points: Float
        wins: Integer
        driver: Driver
        constructors: Constructor[]
    """

    def __init__(self, position: int, positionText: str, points: float, wins: int, driver: Driver,
                 constructors: list[Constructor]) -> None:
        self.position = position
        self.positionText = positionText
        self.points = points
        self.wins = wins
        self.driver = driver
        self.constructors = constructors
        pass

    def __str__(self):
        return f"DriverStanding(position={self.position}, positionText={self.positionText}, points={self.points}, wins={self.wins}, driver={self.driver}, constructors={self.constructors})"

    def __repr__(self):
        return f"DriverStanding(position={self.position}, positionText={self.positionText}, points={self.points}, wins={self.wins}, driver={self.driver}, constructors={self.constructors})"