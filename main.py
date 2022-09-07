from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch


data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()

ORIGIN_CITY_IATA = "WAW"

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=180)

for destination in sheet_data:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_date=tomorrow,
        to_date=six_month_from_today
    )
    if flight.price < destination["lowestPrice"]:
        print(
            f"{flight.price} zł to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}.")
