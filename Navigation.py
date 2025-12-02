from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Placeholder for internal state
last_location = {}
destination_location = {}
last_summary = None

@app.route('/receive_location', methods=['POST'])
def receive_location():
    """
    Receives user location and destination.
    Currently returns a sample response for demonstration purposes.
    """
    data = request.json
    user_location = data.get("current_location", "unknown")
    destination = data.get("destination", "unknown")

    # Update internal state (stub)
    last_location['lat'] = user_location if user_location != "unknown" else None
    destination_location['lat'] = destination if destination != "unknown" else None

    # Placeholder response
    route_summary = {
        "status": "processing",
        "next_step": "Move forward 10 meters",
        "eta": "5 minutes"
    }

    # Update last summary for demo purposes
    global last_summary
    last_summary = route_summary

    return jsonify({
        "message": "Navigation processing stub.",
        "route_summary": route_summary
    }), 200

@app.route('/last_summary', methods=['GET'])
def get_summary():
    """
    Returns the last calculated route summary.
    """
    if last_summary is None:
        return jsonify({"summary": "No navigation data yet."}), 200
    return jsonify({"summary": last_summary}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
