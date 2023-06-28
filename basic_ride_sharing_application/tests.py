"""
Module to include test cases and scenarios for the LLD solution.
"""
from classes import Driver, Rider

if __name__ == "__main__":
    driver = Driver("Rahul")
    rider = Rider("Ajay")

    for _ in range(6):
        rider.create_ride(50, 60, 1, driver)
        ride_amount = driver.close_ride()
        print(f"Rides count: {rider.rides_count}")
        print(f"Ride total fare:{ride_amount}")

        rider.create_ride(50, 60, 2, driver)
        ride_amount = driver.close_ride()
        print(f"Rides count: {rider.rides_count}")
        print(f"Ride total fare:{ride_amount}")
