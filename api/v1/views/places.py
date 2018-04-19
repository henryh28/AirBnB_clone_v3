#!/usr/bin/python3
""" RESTful routes for Place objects """

from models import storage
from models.place import Place
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def all_places(city_id):
    """ Retrieves the list of all Place objects of a City object"""
    place_list = []

    city = storage.get("City", city_id)
    for entry in city.places:
        place_list.append(entry.to_dict())
    return jsonify(place_list)


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
def get_place(place_id):
    """ Retrieves a Place object """
    place = storage.get("Place", place_id)

    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object """
    place = storage.get("Place", place_id)

    if place:
        storage.delete(place)
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """ Creates a new Place object """
    param = request.get_json()
    if not param:
        return "Not a JSON", 400
    if "user_id" not in param.keys():
        return "Missing user_id", 400
    if "name" not in param.keys():
        return "Missing name", 400

    city = storage.get("City", city_id)
    user = storage.get("User", param["user_id"])
    if not city or not user:
        abort(404)

    new_place = Place(**param)
    new_place.city_id = city_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def update_place(place_id):
    """ Updates a Place object """

    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    param = request.get_json()
    if not param:
        return "Not a JSON", 400

    for key, value in param.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict()), 200
