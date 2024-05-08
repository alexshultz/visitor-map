# Visitor Map Application

## Project Overview

This application provides a digital visualization of visitors to the Pony Express Barn and Museum using a web-based interface. The application gathers visitor data through an HTML form, plots the data on a map using OpenLayers, and visualizes visitor locations dynamically as they are recorded.

## Features

- **Visitor Form**: Collects visitor data including city, state, and country.
- **Interactive Map**: Displays the location of visitors using clustering to manage multiple visitors from similar locations.
- **Data Management**: Uses GeoJSON and KML to manage and display geographic data.

## Technologies Used

- **Flask**: Serves the web application and handles backend logic.
- **OpenLayers**: Manages and displays geographic information on a web map.
- **Gunicorn**: Acts as the WSGI HTTP Server to host the application in production.
- **Systemd**: Ensures the application remains running and starts automatically upon system reboots.

## Setup and Installation

### 1. Clone the Repository
```
git clone https://github.com/yourusername/visitor-map.git
cd visitor-map
```

### 2. Install Dependencies
```
pip install -r requirements.txt
```

### 3. Run the Application Locally
```
python src/flask_server.py
```

### For production environments (not quite working yet):
```
gunicorn -c config/gunicorn_config.py src.flask_server:app
```

### 4. Access the Application
- Open a web browser and navigate to `http://localhost:5000` to view the data form.
- Open a web browser and navigate to `http://localhost:5000/map` to view the map.

## Configuration

The application can be configured via the `config/gunicorn_config.py` for Gunicorn settings and `src/flask_server.py` for Flask application settings.

## Contributing

Contributions to the project are welcome! Please fork the repository and submit pull requests with any enhancements. Ensure to follow the existing code style and add unit tests for any new or changed functionality.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any further questions or to report issues, please open an issue on GitHub or contact the repository owner directly.
# visitor-map
