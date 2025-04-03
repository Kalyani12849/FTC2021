from Airport import *

class MaintenanceRecord:
    def __init__(self, input_line, all_flights, all_airports):
        components = [c.strip() for c in input_line.strip().split("-")]

        if len(components) != 5:
            raise ValueError("Invalid data string")

        flight_code = f"{components[0]}-{components[1]}"
        airport_code = components[2]

        try:
            duration = float(components[3])
            cost_per_hour = float(components[4])
        except ValueError:
            raise ValueError("Invalid data string")

        # Find the correct Flight object from all_flights
        flight_obj = None
        for flights in all_flights.values():
            for flight in flights:
                if hasattr(flight, 'get_number') and flight.get_number() == flight_code:
                    flight_obj = flight
                    break
            if flight_obj:
                break

        if not flight_obj:
            raise ValueError("Flight not found")

        if airport_code not in all_airports:
            raise ValueError("Airport not found")

        self._flight = flight_obj
        self._maintenance_airport = all_airports[airport_code]
        self._maintenance_duration = duration
        self._maintenance_cost_per_hour = cost_per_hour

    def get_total_cost(self):
        return self._maintenance_duration * self._maintenance_cost_per_hour

    def get_duration(self):
        return self._maintenance_duration

    def __str__(self):
        flight_code = self._flight.get_number()
        origin = self._flight.get_origin()
        destination = self._flight.get_destination()
        trip_type = "domestic" if origin.get_country() == destination.get_country() else "international"

        return (
            f"{flight_code} ({origin.get_city()} to {destination.get_city()} ({trip_type}) "
            f"[{round(self._flight.get_duration())}h]) from {origin.get_code()} [{origin.get_city()}, {origin.get_country()}] "
            f"to be maintained at {self._maintenance_airport.get_code()} "
            f"[{self._maintenance_airport.get_city()}, {self._maintenance_airport.get_country()}] "
            f"for {int(self._maintenance_duration)} hours @ ${self._maintenance_cost_per_hour:.1f}/hour "
            f"(${self.get_total_cost():.1f})"
        )

    def __eq__(self, other):
        if not isinstance(other, MaintenanceRecord):
            return False
        return (
            self._flight == other._flight and
            self._maintenance_airport == other._maintenance_airport and
            self._maintenance_duration == other._maintenance_duration and
            self._maintenance_cost_per_hour == other._maintenance_cost_per_hour
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if not isinstance(other, MaintenanceRecord):
            return NotImplemented
        return self.get_total_cost() < other.get_total_cost()

    def __le__(self, other):
        if not isinstance(other, MaintenanceRecord):
            return NotImplemented
        return self.get_total_cost() <= other.get_total_cost()

    def __gt__(self, other):
        if not isinstance(other, MaintenanceRecord):
            return NotImplemented
        return self.get_total_cost() > other.get_total_cost()

    def __ge__(self, other):
        if not isinstance(other, MaintenanceRecord):
            return NotImplemented
        return self.get_total_cost() >= other.get_total_cost()


