from flask import Flask, request, render_template, jsonify, send_from_directory, abort
from flask_socketio import SocketIO, emit
from datetime import datetime, timedelta, timezone
from services.geolocation import GeoLocator
from services.kml_manager import KMLManager
from services.GeoJSONManager import GeoJSONManager
import os

app = Flask(__name__, template_folder='../frontend')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
geo_locator = GeoLocator(user_agent='Pony Express Barn and Museum Visitor Map')
kml_manager = KMLManager()  # Instantiate the KMLManager


@app.route("/submit", methods=["POST"])
def submit():
    try:
        city = request.form.get('city', '').strip()
        state = request.form.get('state', '').strip() or 'KS'
        country = request.form.get('country', '').strip() or 'US'
        date = request.form.get('date', '').strip()
        latitude, longitude, display_name = geo_locator.get_coordinates(city, state, country)
        summary = create_summary(city, state, country, date, latitude, longitude, display_name)

        if latitude and longitude:
            geo_manager = GeoJSONManager()
            geo_manager.append_geojson_feature(latitude, longitude, date, city, state, country, display_name)
            kml_manager = KMLManager()
            kml_manager.append_kml_placemark(latitude, longitude, date, city, state, country, display_name)
            # Trigger the update map event to all connected clients
            socketio.emit('update_map', {'data': 'new_data_available'}, namespace='/')
            return jsonify({"message": "Data added successfully", "summary": summary})
        else:
            return jsonify({"message": "Data not added", "summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@app.route('/update_data')
def update_data():
    # Assume this endpoint is hit whenever new data is available
    socketio.emit('update_map', {'data': 'new_data_available'})
    return jsonify(success=True)

@app.route("/data/geojson")
def serve_geojson():
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/geojson')  # Adjust path as necessary
    filename = 'current_data.geojson'
    try:
        response = send_from_directory(directory, filename, as_attachment=False)
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'  # Prevent caching
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    except FileNotFoundError:
        abort(404)  # If the file is not found, return a 404 error

@app.route('/test')
def test():
    return render_template('test.html')

@app.route("/map")
def show_map():
    return render_template("map.html")

@app.route("/")
def form():
    return render_template("visitor_form.html")


@app.route('/kml/<filename>')
def serve_kml(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
    directory = os.path.join(base_dir, '../data/kml')  # Use os.path.join to handle path construction
    delta = timedelta(seconds=5)
    expiration_time = datetime.now(timezone.utc) + delta  # Example: Expire in 5 minutes

    try:
        response = send_from_directory(directory, filename, as_attachment=False,
                                       mimetype='application/vnd.google-earth.kml+xml')
        # Control caching behavior here:
        response.headers['Cache-Control'] = 'no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = expiration_time.strftime('%a, %d %b %Y %H:%M:%S GMT')
        # Ensure the directory path and file are accessible and correct
        return response
    except FileNotFoundError:
        abort(404)  # Return a 404 error if the file is not found


def create_summary(city, state, country, date, latitude, longitude, display_name):
    parts = []
    parts.append(f"Original Input: ")
    if city:
        parts.append(f"{city}")
    if state:
        parts.append(f"{state}")
    if country:
        parts.append(f"{country}")
    parts.append(f"Date: {date}")
    if latitude:
        parts.append(f"Latitude: {latitude}")
    else:
        parts.append(f"No Latitude found")
    if longitude:
        parts.append(f"Longitude: {longitude}")
    else:
        parts.append(f"No Longitude found")
    if display_name:
        parts.append(f"Display Name: {display_name}")

    return ", ".join(parts)


@app.route("/live_data.kml")
def live_kml_data():
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/kml')  # Adjust path as necessary
    filename = 'current_data.kml'
    try:
        response = send_from_directory(directory, filename, as_attachment=False,
                                       mimetype='application/vnd.google-earth.kml+xml')
        # Set headers to ensure no caching occurs
        response.headers['Cache-Control'] = 'no-cache, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'  # Forces clients to get a new version each time
        print(f"Sending live_data.kml")
        return response
    except FileNotFoundError:
        abort(404)  # Return a 404 error if the file is not found


def validate_state(input_state):
    return input_state or 'KS'


def validate_country(input_country):
    return input_country or 'US'


def validate_number(input_number):
    try:
        number = int(input_number)
        return max(1, number)
    except ValueError:
        return 1


def validate_date(input_date, yesterday_flag):
    if yesterday_flag:
        return (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    return input_date


if __name__ == "__main__":
    app.run(debug=True)