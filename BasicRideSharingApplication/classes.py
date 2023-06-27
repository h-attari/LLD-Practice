from enum import Enum
import uuid


class RideStatus(Enum):
    open = 1
    closed = 2
    withdrawn = 3


class Person:
    def __init__(self, name: str) -> None:
        self.name = name
        self.ride = None


class Ride:
    def __init__(self, origin: int, destination: int, seats: int, amount_per_km: int=20) -> None:
        self.id = uuid.uuid4()
        self.origin = origin
        self.destination = destination
        self.seats = seats
        self.amount_per_km = amount_per_km
        self.status = RideStatus.open
    
    def calculate_amount(self) -> int:
        km = self.destination - self.origin
        amount = km * self.seats * self.amount_per_km
        if self.seats > 1:
            amount *= 0.75
        return int(amount)


class Driver(Person):
    def __init__(self, name: str) -> None:
        self.id = f"d-{uuid.uuid4()}"
        self.rider = None
        Person.__init__(self, name)
    
    def close_ride(self) -> int:
        ride = self.ride
        ride_amount = ride.calculate_amount()
        ride.closed = True
        self.ride = None
        self.rider.ride = None
        ride.status = RideStatus.closed
        return ride_amount


class Rider(Person):
    def __init__(self, name: str) -> None:
        self.id = f"d-{uuid.uuid4()}"
        self.driver = None
        Person.__init__(self, name)
    
    def create_ride(self, origin: int, destination: int, seats: int, driver: Driver) -> None:
        if self.ride is not None:
            raise Exception("Only 1 ride at a time is allowed.")
        ride = Ride(origin, destination, seats)
        self.ride = ride
        driver.ride = ride
        driver.rider = self
        self.driver = driver
        print(f"Ride created with id: {ride.id}")
    
    def update_ride(self, origin: int, destination: int, seats: int, driver: Driver) -> None:
        if self.ride is None:
            print("No present ride, creating a new ride.")
            self.create_ride(origin, destination, seats, driver)
        else:
            ride = self.ride
            ride.origin = origin
            ride.destination = destination
            ride.seats = seats
            print(f"Ride updated with id: {ride.id}")
    
    def withdraw_ride(self) -> None:
        self.ride.status = RideStatus.withdrawn
        self.ride = None
        self.driver.ride = None
