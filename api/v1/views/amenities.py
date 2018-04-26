#!/usr/bin/python3
""" RESTful routes for Amenity objects """

from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def all_amenities():
    """ Retrieves the list of all Amenity objects """
    amenity_list = []

    for entry in storage.all("Amenity").values():
        amenity_list.append(entry.to_dict())
    return jsonify(amenity_list)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieves an Amenity object """
    amenity = storage.get("Amenity", amenity_id)

    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes an Amenity object """
    amenity = storage.get("Amenity", amenity_id)

    if amenity:
        storage.delete(amenity)
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """ Creates a new Amenity object """
    param = request.get_json()

    if not param:
        return "Not a JSON", 400
    if "name" not in param.keys():
        return "Missing name", 400

    new_amenity = Amenity(**param)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Updates an Amenity object """

    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)

    param = request.get_json()
    if not param:
        return "Not a JSON", 400

    for key, value in param.items():
        setattr(amenity, key, value)

    amenity.save()
    return jsonify(amenity.to_dict()), 200
