import requests


class CountryRequests:
    def __init__(self):
        self.url = "https://wft-geo-db.p.rapidapi.com/v1/geo/countries"

        self.headers = {
            "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com",
            "X-RapidAPI-Key": "683f0a3f03mshaa9746439a463cap171381jsn59c0ca6bfcde"
        }

    def get_country(self):
        response = requests.request("GET", self.url, headers=self.headers)
        print(response.text)


if __name__ == "__main__":
    print("Hello, World!")
    req = CountryRequests()
    req.get_country()
