import enum
import uuid


RIDE_STATUS = enum("OPEN", "CLOSED", "WITHDRAWN")


class Person:
    def __init__(self, name: str) -> None:
        self.name = name
        self.ride = Ride()


class Ride:
    def __init__(self, id: uuid.UUID, origin: int, destination: int, seats: int, amount_per_km: int=20) -> None:
        self.id = id
        self.origin = origin
        self.destination = destination
        self.seats = seats
        self.amount_per_km = amount_per_km
        self.status = RIDE_STATUS.OPEN
    
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
        return ride_amount


class Rider(Person):
    def __init__(self, name: str) -> None:
        self.id = f"d-{uuid.uuid4()}"
        self.driver = None
        Person.__init__(self, name)
    
    def create_ride(self) -> None:
        pass
    
    def update_ride(self) -> None:
        pass
    
    def withdraw_ride(self) -> None:
        self.ride.closed = True
        self.ride = None
        self.driver.ride = None
