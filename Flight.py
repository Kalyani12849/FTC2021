from Airport import *

class Flight:
    def __init__(self, origin, destination, flight_number, duration):
        if not isinstance(origin, Airport) or not isinstance(destination, Airport):
            raise TypeError("The origin and destination must be Airport objects")

        self._origin = origin
        self._destination = destination
        self._flight_number = flight_number
        self._duration = duration

    def __str__(self):
        if self._origin.get_country() == self._destination.get_country():
            return f"{self._origin.get_city()} to {self._destination.get_city()} (domestic) [{round(self._duration)}h]"
        else:
            return f"{self._origin.get_city()} to {self._destination.get_city()} (international) [{round(self._duration)}h]"

    def __eq__(self, other):
        if isinstance(other, Flight):
            return self._origin == other._origin and self._destination == other._destination
        return False

    def __add__(self, conn_flight):
        if not isinstance(conn_flight, Flight):
            raise TypeError("The connecting_flight must be a Flight object")
        if self._destination != conn_flight._origin:
            raise ValueError("These flights cannot be combined")

        return Flight(self._origin, conn_flight._destination, self._flight_number, self._duration + conn_flight._duration)

    def get_number(self):
        return self._flight_number

    def get_origin(self):
        return self._origin

    def get_destination(self):
        return self._destination

    def get_duration(self):
        return self._duration

    def is_domestic(self):
        return self._origin.get_country() == self._destination.get_country()

    def set_origin(self, origin):
        if isinstance(origin, Airport):
            self._origin = origin
        else:
            raise TypeError("The origin must be an Airport object")

    def set_destination(self, destination):
        if isinstance(destination, Airport):
            self._destination = destination
        else:
            raise TypeError("The destination must be an Airport object")









