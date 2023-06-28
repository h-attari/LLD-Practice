"""
Module contains design logic for the LLD problem.
"""
import uuid
from enum import Enum


class RideStatus(Enum):
    """
    Enum class to assign ride statuses.
    """

    OPEN = 1
    CLOSED = 2
    WITHDRAWN = 3


class Person:
    """
    Parent class for Riders and Drivers.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.ride = None
        self.rides_count = 0


class Ride:
    """
    Class to accommodate Ride related attributes.
    """

    def __init__(
        self,
        origin: int,
        destination: int,
        seats: int,
        premium_ride: bool = False,
        amount_per_km: int = 20,
    ) -> None:
        self.ride_id = uuid.uuid4()
        self.origin = origin
        self.destination = destination
        self.seats = seats
        self.amount_per_km = amount_per_km
        self.status = RideStatus.OPEN
        self._premium = premium_ride

    def _calculate_amount(self) -> int:
        """
        Method to calculate the total ride fare at the time of ride completion.
        """
        km_travelled = self.destination - self.origin
        if self._premium:
            discount_mutiplier = 0.5 if self.seats > 1 else 0.75
        else:
            discount_mutiplier = 0.75 if self.seats > 1 else 1
        amount = km_travelled * self.seats * self.amount_per_km * discount_mutiplier
        return round(amount)


class Driver(Person, Ride):
    """
    Class to accommodate Driver related attributes.
    """

    def __init__(self, name: str) -> None:
        self.driver_id = f"d-{uuid.uuid4()}"
        self.rider = None
        Person.__init__(self, name)

    def close_ride(self) -> int:
        """
        Method used by driver instance to close and mark the current ride as completed.
        """
        ride = self.ride
        ride.status = RideStatus.CLOSED
        self.rider.rides_count += 1
        if not self.rider.preferred_rider and self.rider.rides_count > 10:
            self.rider.upgrade_rider()
        ride_amount = ride._calculate_amount()
        self.ride = None
        self.rider.ride = None
        return ride_amount


class Rider(Person, Ride):
    """
    Class to accommodate Rider related attributes.
    """

    def __init__(self, name: str) -> None:
        self.rider_id = f"d-{uuid.uuid4()}"
        self.driver = None
        self.preferred_rider = False
        Person.__init__(self, name)

    def upgrade_rider(self):
        """
        Method to mark a rider as premium after a certain condition fulfilled
        """
        self.preferred_rider = True
        self.ride._premium = True

    def create_ride(
        self, origin: int, destination: int, seats: int, driver: Driver
    ) -> None:
        """
        Method used by rider instance to initiate a new ride.
        """
        if self.ride is not None:
            raise ValueError("Only 1 ride at a time is allowed.")
        premium_ride = True if self.preferred_rider else False
        ride = Ride(origin, destination, seats, premium_ride)
        self.ride = ride
        driver.ride = ride
        driver.rider = self
        self.driver = driver
        print(f"Ride created with id: {ride.ride_id}")

    def update_ride(
        self, origin: int, destination: int, seats: int, driver: Driver
    ) -> None:
        """
        Method used by rider instance to update the current ride if present
        else initiate a new ride.
        """
        if self.ride is None:
            print("No present ride, creating a new ride.")
            self.create_ride(origin, destination, seats, driver)
        else:
            ride = self.ride
            ride.origin = origin
            ride.destination = destination
            ride.seats = seats
            print(f"Ride updated with id: {ride.ride_id}")

    def withdraw_ride(self) -> None:
        """
        Method used by rider instance to cancel the current ride.
        """
        self.ride.status = RideStatus.WITHDRAWN
        self.ride = None
        self.driver.ride = None
