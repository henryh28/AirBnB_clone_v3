#!/usr/bin/python3


from api.v1.views import app_views
from flask import jsonify
from models import storage

classes = {"User": "users", "Place": "places", "State": "states",
           "City": "cities", "Amenity": "amenities", "Review": "reviews"}


@app_views.route("/status")
def status():
    """ Returns a JSON of status """
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """ Retrieves the number of each objects by type """
    total_by_type = {}
    for entry in classes.keys():
        total_by_type[classes[entry]] = storage.count(entry)
    return jsonify(total_by_type)