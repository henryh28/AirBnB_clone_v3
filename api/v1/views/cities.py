#!/usr/bin/python3
"""
Cities API
"""
from models import storage
from models.city import City
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views


@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def all_cities(state_id):
    """
    Retrieves all cities in a state
    """
    result = []
    state = storage.get("State", state_id)

    if not state:
        abort(404)

    for value in state.cities:
        result.append(value.to_dict())
    return jsonify(result)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
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
    """
    Delete a city object
    """
    city = storage.get("City", city_id)
    if city:
        storage.delete(city)
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def create_city(state_id):
    """
    Create a new city object
    """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    params = request.get_json()
    if not params:
        return "Not a JSON", 400

    if "name" not in params:
        return "Missing name", 400

    city = City(**params)
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<cities_id>", methods=["PUT"], strict_slashes=False)
def update_city(cities_id):
    """
    Updates parameters of a city object
    """
    city = storage.get("City", cities_id)
    if not city:
        abort(404)
    params = request.get_json()
    if not params:
        return "Not a JSON", 400

    for key, value in params.items():
        setattr(city, key, value)
        city.save()
    return jsonify(city.to_dict()), 200
