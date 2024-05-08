import datetime
import os
import glob
import shutil


class KMLManager:
    def __init__(self, directory=None, filepath="data/kml/current_data.kml"):
        self.filepath = filepath
        if not os.path.exists(self.filepath):  # Initialize KML if it does not exist
            with open(self.filepath, 'w') as file:
                file.write("""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
</Document>
</kml>""")

        if directory is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.directory = os.path.join(base_dir, '..', '..', 'data', 'kml')
        else:
            self.directory = directory

        self.backup_directory = os.path.join(self.directory, 'backups')
        os.makedirs(self.directory, exist_ok=True)  # Ensure main directory exists
        os.makedirs(self.backup_directory, exist_ok=True)  # Ensure backup directory exists

    def append_kml_placemark(self, latitude, longitude, date, city, state, country, display_name):
        placemark = self.generate_kml_placemark(latitude, longitude, date, city, state, country, display_name)

        # Append the placemark before the closing tags
        with open(self.filepath, 'r+') as file:
            file.seek(0, os.SEEK_END)  # Go to the end of file
            pos = file.tell() - len('</Document>\n</kml>')  # Adjust back to before the closing tags
            file.seek(pos)  # Reposition to start of closing tags
            file.write(placemark)  # Write new placemark
            file.write('\n</Document>\n</kml>')  # Re-write closing tags

    def finalize_kml(self):
        # This method may not be necessary unless you need to finalize the file in a special way
        pass

    def write_kml_data(self, latitude, longitude, date, city, state, country, display_name):
        print(f"Writing KML data for {city}, {state} {country} (aka {display_name}) at coordinates {latitude}, {longitude} on {date}")
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"data_{timestamp}.kml"
        filepath = os.path.join(self.directory, filename)

        kml_content = self.generate_single_location_kml_file_content(latitude, longitude, date, city, state, country, display_name)
        with open(filepath, 'w') as file:
            file.write(kml_content)
            print(f"File written: {filepath}")
        return filepath

    def generate_kml_placemark(self, latitude, longitude, date, city, state, country, display_name):
        return f"""
    <Placemark>
        <name>{display_name}</name>
        <form>
            <city>{city}</city>,
            <state>{state}</state>,
            <country>{country}</country>,
            <date>{date}</date>        
        </form>,
        <Point>
            <coordinates>{longitude},{latitude}</coordinates>
        </Point>
    </Placemark>\n"""

    def generate_single_location_kml_file_content(self, latitude, longitude, date, city, state, country, display_name):
        placemark = self.generate_kml_placemark(latitude, longitude, date, city, state, country, display_name)
        kml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
    {placemark}
</Document>
</kml>
"""
        return kml_content

    def merge_kml_files(self, static_filename="static_data.kml"):
        static_filepath = os.path.join(self.directory, static_filename)
        kml_files = sorted(glob.glob(os.path.join(self.directory, "data_*.kml")))

        with open(static_filepath, 'a') as main_file:
            for kml_file in kml_files:
                with open(kml_file, 'r') as file:
                    content = file.readlines()[2:-2]  # Adjust indices based on your KML structure
                    if content:  # Check if there is anything to write
                        main_file.writelines(content)
                    os.remove(kml_file)  # Delete the short-term file after merging

    def read_kml_file(self, filename):
        filepath = os.path.join(self.directory, filename)
        with open(filepath, 'r') as file:
            return file.read()

    def clear_backup_directory(self):
        for file in os.listdir(self.backup_directory):
            file_path = os.path.join(self.backup_directory, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

    def backup_current_files(self):
        for file in glob.glob(os.path.join(self.directory, '*.kml')):
            shutil.copy(file, self.backup_directory)

    def update_static_data(self):
        self.clear_backup_directory()
        self.backup_current_files()
        self.merge_kml_files()


if __name__ == "__main__":
    manager = KMLManager()
    manager.update_static_data()
