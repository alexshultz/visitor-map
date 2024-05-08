import xml.etree.ElementTree as ET
import json

class GeoConverter:
    @staticmethod
    def kml_to_geojson(kml_content):
        # Parse KML content using ElementTree
        root = ET.fromstring(kml_content)
        features = []

        for placemark in root.findall('.//{http://www.opengis.net/kml/2.2}Placemark'):
            coordinates = placemark.find('.//{http://www.opengis.net/kml/2.2}coordinates').text.strip().split(',')
            features.append({
                "type": "Feature",
                "properties": {
                    "name": placemark.find('.//{http://www.opengis.net/kml/2.2}name').text
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(coordinates[0]), float(coordinates[1])]
                }
            })

        return json.dumps({
            "type": "FeatureCollection",
            "features": features
        }, indent=4)

    @staticmethod
    def geojson_to_kml(geojson_content):
        geojson = json.loads(geojson_content)
        kml_elements = []

        kml_elements.append('<?xml version="1.0" encoding="UTF-8"?>')
        kml_elements.append('<kml xmlns="http://www.opengis.net/kml/2.2">')
        kml_elements.append('<Document>')

        for feature in geojson['features']:
            coords = feature['geometry']['coordinates']
            kml_elements.append('<Placemark>')
            kml_elements.append(f'<name>{feature["properties"]["name"]}</name>')
            kml_elements.append('<Point>')
            kml_elements.append(f'<coordinates>{coords[0]},{coords[1]},0</coordinates>')
            kml_elements.append('</Point>')
            kml_elements.append('</Placemark>')

        kml_elements.append('</Document>')
        kml_elements.append('</kml>')

        return '\n'.join(kml_elements)

# Example Usage:
converter = GeoConverter()
geojson = converter.kml_to_geojson(kml_data)
kml = converter.geojson_to_kml(geojson_data)
