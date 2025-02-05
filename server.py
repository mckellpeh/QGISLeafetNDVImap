from flask import Flask, request, jsonify
from flask_cors import CORS
import rasterio
from rasterio.transform import rowcol
import os
from firebase_admin import credentials, initialize_app

# Get the key file path from the environment variable
cred_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# Initialize Firebase
cred = credentials.Certificate(cred_path)
initialize_app(cred)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow requests from JavaScript

# Load the NDVI raster file (Update this path to match your file location)
NDVI_RASTER_PATH = "data/NDVI layer generated image final.tif"

# Function to get NDVI value at a specific lat/lon
def get_ndvi(lat, lon):
    try:
        with rasterio.open(NDVI_RASTER_PATH) as dataset:
            # Convert lat/lon to row/col of the raster
            row, col = rowcol(dataset.transform, lon, lat)

            # Read NDVI value at that pixel
            ndvi_value = dataset.read(1)[row, col]  # Band 1 (NDVI data)
            if ndvi_value == 255:  # Handle NoData values
                return None
            ndvi_value = ((ndvi_value / 127.5) - 1) * -1  # Convert 0-255 range back to -1 to 1 AND invert # Scale to -1 to 1

            return float(ndvi_value)  # Convert to normal number
    except Exception as e:
        print(f"Error retrieving NDVI value: {e}")
        return None  # If error, return None

# API Route: Get NDVI Value
@app.route("/get_ndvi", methods=["GET"])
def get_ndvi_api():
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)

    if lat is None or lon is None:
        return jsonify({"error": "Invalid coordinates"}), 400

    ndvi_value = get_ndvi(lat, lon)

    if ndvi_value is None:
        return jsonify({"error": "NDVI value not found"}), 404

    return jsonify({"lat": lat, "lon": lon, "ndvi": ndvi_value})

# Run the Flask server
if __name__ == "__main__":
    app.run(debug=True, port=5000)
