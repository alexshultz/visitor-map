import json
import os


class GeoJSONManager:
    def __init__(self, filepath="data/geojson/current_data.geojson"):
        self.filepath = filepath
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as file:
                json.dump({
                    "type": "FeatureCollection",
                    "features": []
                }, file, indent=4)

    def append_geojson_feature(self, latitude, longitude, date, city, state, country, display_name):
        new_feature = self.generate_geojson_feature(latitude, longitude, date, city, state, country, display_name)
        with open(self.filepath, 'r+') as file:
            data = json.load(file)
            data['features'].append(new_feature)
            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=4)

    def generate_geojson_feature(self, latitude, longitude, date, city, state, country, display_name):
        return {
            "type": "Feature",
            "properties": {
                "name": display_name,
                "date": date,
                "city": city,
                "state": state,
                "country": country
            },
            "geometry": {
                "type": "Point",
                "coordinates": [longitude, latitude]
            }
        }
