from flask import Flask, jsonify, request
from urllib.parse import unquote

app = Flask(__name__, static_folder='src', static_url_path='/')

activities = {
    "Yoga Class": {
        "description": "Relaxing yoga session",
        "schedule": "Mondays 7 PM",
        "max_participants": 10,
        "participants": []
    },
    "Cooking Workshop": {
        "description": "Learn to cook Italian dishes",
        "schedule": "Wednesdays 6 PM",
        "max_participants": 15,
        "participants": []
    }
}

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/activities', methods=['GET'])
def get_activities():
    return jsonify(activities)

@app.route('/activities/<activity>/signup', methods=['POST'])
def signup(activity):
    activity = unquote(activity)
    email = request.args.get('email')
    if not email:
        return jsonify({"detail": "Email required"}), 400
    if activity not in activities:
        return jsonify({"detail": "Activity not found"}), 404
    if email in activities[activity]['participants']:
        return jsonify({"detail": "Already signed up"}), 400
    if len(activities[activity]['participants']) >= activities[activity]['max_participants']:
        return jsonify({"detail": "Activity is full"}), 400
    activities[activity]['participants'].append(email)
    return jsonify({"message": f"Signed up for {activity}"})

@app.route('/activities/<activity>/unregister', methods=['DELETE'])
def unregister(activity):
    activity = unquote(activity)
    email = request.args.get('email')
    if not email:
        return jsonify({"detail": "Email required"}), 400
    if activity not in activities:
        return jsonify({"detail": "Activity not found"}), 404
    if email not in activities[activity]['participants']:
        return jsonify({"detail": "Not signed up"}), 400
    activities[activity]['participants'].remove(email)
    return jsonify({"message": f"Unregistered from {activity}"})

if __name__ == '__main__':
    app.run(debug=True)
