#!/usr/bin/python3
"""
Cities API
"""
from models import storage
from models.state import City
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
import json


@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def all_cities():
    """
    Retrieves all cities in a state
    """
    result = []
    state = storage.get("State", state_id)
    for value in storage.all("City").values():
        if value = state:
            result.append(value.to_dict())
        return jsonify(result)
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city():
    """
    Retrieves city by id
    """
    city = storage.get("City", city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    city = storage.get("City", city_id)
    if city:
        storage.delete(city)
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def post_city(state_id):
    """
    Create city
    """
    
