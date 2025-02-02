from flask import Flask, request, jsonify
import rasterio
import numpy as np

app = Flask(__name__)

# Path to your NDVI raster file
NDVI_RASTER_PATH = "data/QGISgeneratedNDVIlayeroriginal_0.png"

@app.route('/query-ndvi', methods=['GET'])
def query_ndvi():
    lat = float(request.args.get('lat'))
    lng = float(request.args.get('lng'))

    # Open the raster file
    with rasterio.open(NDVI_RASTER_PATH) as src:
        # Convert latitude and longitude to raster coordinates
        row, col = src.index(lng, lat)

        # Read the value at the specified coordinates
        ndvi_value = src.read(1)[row, col]

        return jsonify({"ndvi_value": float(ndvi_value)})

if __name__ == "__main__":
    app.run(debug=True)
