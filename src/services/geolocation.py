import requests


class GeoLocator:
    def __init__(self, base_url="https://nominatim.openstreetmap.org/search", user_agent="Pony Express Barn and Museum Visitor Map"):
        self.base_url = base_url
        self.headers = {'User-Agent': user_agent}

    def get_coordinates(self, city, state, country):
        params = {'format': 'json', 'q': f"{city}, {state}, {country}"}
        response = requests.get(self.base_url, params=params, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            if data:
                file_message = "Coordinates found"
                summary = self.create_summary(city, state, country, data[0]['lat'], data[0]['lon'], data[0]['display_name'], file_message)
                print(summary)
                print(f"Data: {data}")
                return data[0]['lat'], data[0]['lon'], data[0]['display_name']
        file_message = "Coordinates not found"
        summary = self.create_summary(city, state, country, None, None, None, file_message)
        print(summary)
        return None, None, None

    def create_summary(self, city, state, country, latitude, longitude, display_name, file_message):
        parts = []
        parts.append(f"Original Input: ")
        if city:
            parts.append(f"{city}, ")
        if state:
            parts.append(f"{state}, ")
        if country:
            parts.append(f"{country}, ")
        if latitude:
            parts.append(f"\nLatitude: {latitude}, ")
        else:
            parts.append(f"\nNo Latitude found, ")
        if longitude:
            parts.append(f"\nLongitude: {longitude}, ")
        else:
            parts.append(f"\nNo Longitude found, ")
        if display_name:
            parts.append(f"\nDisplay Name: {display_name}")
        parts.append(f"\nInfo: {file_message}")
        return ", ".join(parts)
