import os
from flask import Flask, request,jsonify
from backend.models import Events
from backend import create_app,db
app = create_app()

from flask import request  # Make sure to import request

@app.after_request
def apply_cors(response):
    origin = request.headers.get('Origin')
    allowed_origins = [
        "http://localhost:8080",
        "http://localhost:3000",
        "http://localhost:5000"
    ]
    
    # Check if the origin is in our allowed list
    if origin in allowed_origins:
        # Set the specific origin that made the request
        response.headers["Access-Control-Allow-Origin"] = origin
    else:
        # For development, you might want to allow all origins (not recommended for production)
        response.headers["Access-Control-Allow-Origin"] = "*"
    
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


@app.route("/")
def index():
    return "Hello, World!"

@app.route('/events')
def get_events():
    events = Events.query.all()
    # Convert each event object to a dictionary
    events_list = [{
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'date': event.date.isoformat(),  # Convert datetime to string
        'location': event.location,
        'tags': event.tags
    } for event in events]
    
    return jsonify(events_list)

@app.route("/events/<int:id>")
def get_event(id):
    event = Events.query.get(id)
    return jsonify(event)

@app.route("/create-events", methods=["POST"])
def create_events():
    data = request.json()
    new_event = Events(title=data["title"], description=data["description"], date=data["date"], location=data["location"], tags=data["tags"])
    db.session.add(new_event)
    db.session.commit()
    return jsonify(new_event)

if __name__ == "__main__":
    app.run(debug=True, port=8080)