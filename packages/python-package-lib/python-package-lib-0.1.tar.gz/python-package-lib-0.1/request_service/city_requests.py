import requests


class CityRequests:
    def __init__(self):
        self.url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities"
        self.headers = {
            "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com",
            "X-RapidAPI-Key": "683f0a3f03mshaa9746439a463cap171381jsn59c0ca6bfcde"
        }

    def get_city(self):
        response = requests.request("GET", self.url, headers=self.headers)
        print(response.text)


if __name__ == "__main__":
    print("Hello, World!")
    req = CityRequests()
    req.get_city()
