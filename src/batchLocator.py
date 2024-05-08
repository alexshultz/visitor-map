import csv
import time
from services.geolocation import GeoLocator
from services.kml_manager import KMLManager
from services.GeoJSONManager import GeoJSONManager


def process_records(csv_path):
    # Initialize the managers
    geo_locator = GeoLocator()
    kml_manager = KMLManager()
    geojson_manager = GeoJSONManager()

    failed_records = []

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            date = row['Date']
            city = row['City']
            state = row['State']
            country = row['Country']
            # Throttle the requests to ensure one every two seconds
            time.sleep(2)
            print(f"Processing: {date},{city}, {state}, {country}")
            # Attempt to get the coordinates
            latitude, longitude, display_name = geo_locator.get_coordinates(city, state, country)
            if latitude and longitude:
                # Successful lookup
                print(f"Successful lookup: {row}")
                kml_manager.append_kml_placemark(latitude, longitude, date, city, state, country, display_name)
                geojson_manager.append_geojson_feature(latitude, longitude, date, city, state, country, display_name)
            else:
                # Failed lookup
                print(f"Failed lookup: {row}")
                failed_records.append(row)

    # Optional: Write failed records to a file or handle them as needed
    with open('failed_lookups.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(failed_records)


# Example usage
process_records('/Users/alex/Documents/Guestbook 9-1-2023/Sheet1-Table 1 sample.csv')
