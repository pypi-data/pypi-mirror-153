from request_service.city_requests import CityRequests
from request_service.country_requests import CountryRequests


class FormatService:
    def __init__(self):
        self.city = CityRequests()
        self.country = CountryRequests()

    def get_all_cities(self):
        json_cities = self.city.get_city()
        print(json_cities)
