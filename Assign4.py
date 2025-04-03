from Flight import *
from Airport import *
from MaintenanceRecord import *

all_airports = {}
all_flights = {}
maintenance_records = []


def load_flight_files(airport_file, flight_file):
    global all_airports, all_flights  # Add this line!
    all_airports = {}
    all_flights = {}
    try:
        with open(airport_file, 'r') as air_file:
            for line in air_file:
                parts = [p.strip() for p in re.split(r'-+', line.strip()) if p.strip()]
                if len(parts) != 3:
                    continue
                code, country, city = parts
                airport = Airport(country, city, code)
                all_airports[code] = airport

        with open(flight_file, 'r') as f_file:
            for line in f_file:
                parts = [p.strip() for p in re.split(r'-+', line.strip()) if p.strip()]
                if len(parts) != 4:
                    continue
                flight_number, origin_code, dest_code, duration_str = parts
                try:
                    duration = float(duration_str)
                except ValueError:
                    continue
                if origin_code in all_airports and dest_code in all_airports:
                    origin = all_airports[origin_code]
                    destination = all_airports[dest_code]
                    flight = Flight(origin, destination, flight_number, duration)
                    if origin_code not in all_flights:
                        all_flights[origin_code] = []
                    all_flights[origin_code].append(flight)

        return True, all_airports, all_flights

    except Exception as e:
        print(f"Error loading flight files: {e}")
        return False, {}, {}


def get_airport_using_code(code):
    if code in all_airports:
        return all_airports[code]
    raise ValueError("No airport with the given code: " + code)

def find_all_flights_city(city):
    result = []
    for flights in all_flights.values():
        for flight in flights:
            if flight.get_origin().get_city() == city or \
               flight.get_destination().get_city() == city:
                result.append(flight)
    return result

def find_all_flights_country(country):
    result = []
    for flights in all_flights.values():
        for flight in flights:
            if flight.get_origin().get_country() == country or \
               flight.get_destination().get_country() == country:
                result.append(flight)
    return result

def has_flight_between(orig_airport, dest_airport):
    if not isinstance(orig_airport, Airport) or not isinstance(dest_airport, Airport):
        return False

    origin_code = orig_airport.get_code()
    if origin_code in all_flights:
        for flight in all_flights[origin_code]:
            if flight.get_destination().get_code() == dest_airport.get_code():
                return True
    return False

def shortest_flight_from(orig_airport):
    if not isinstance(orig_airport, Airport):
        return None

    origin_code = orig_airport.get_code()
    if origin_code not in all_flights or not all_flights[origin_code]:
        return None

    shortest = all_flights[origin_code][0]
    for flight in all_flights[origin_code]:
        if flight.get_duration() < shortest.get_duration():
            shortest = flight
    return shortest

def find_return_flight(flight):
    if not isinstance(flight, Flight):
        raise ValueError("Invalid flight object")

    origin = flight.get_origin()
    destination = flight.get_destination()
    origin_code = origin.get_code()
    destination_code = destination.get_code()

    if destination_code in all_flights:
        for return_flight in all_flights[destination_code]:
            if return_flight.get_destination().get_code() == origin_code:
                return return_flight

    raise ValueError("There is no flight from " + destination_code + " to " + origin_code)

def create_maintenance_records(file_name, flights_dict, airports_dict):
    success = True
    try:
        with open(file_name, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = MaintenanceRecord(line, flights_dict, airports_dict)
                    if isinstance(record, MaintenanceRecord) and \
                       record not in maintenance_records:
                        maintenance_records.append(record)
                except ValueError as e:
                    print(f"Skipping invalid record: {line}. Error: {e}")
                    success = False
        return success
    except Exception as e:
        print(f"Error reading maintenance records from {file_name}: {e}")
        return False

def find_total_cost(records):
    total = 0.0
    for record in records:
        if isinstance(record, MaintenanceRecord):
            total += record.get_total_cost()
    return total

def find_total_duration(records):
    total = 0.0
    for record in records:
        if isinstance(record, MaintenanceRecord):
            total += record.get_duration()
    return total

def sort_maintenance_records(records):
    clean_records = [r for r in records if isinstance(r, MaintenanceRecord)]
    return sorted(clean_records)

