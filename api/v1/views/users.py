#!/usr/bin/python3
""" RESTful routes for User objects """

from models import storage
from models.user import User
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def all_users():
    """ Retrieves the list of all User objects """
    user_list = []

    for entry in storage.all("User").values():
        user_list.append(entry.to_dict())
    return jsonify(user_list)


@app_views.route("/users/<user_id>", methods=["GET"],
                 strict_slashes=False)
def get_user(user_id):
    """ Retrieves a User object """
    user = storage.get("User", user_id)

    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes a User object """
    user = storage.get("User", user_id)

    if user:
        storage.delete(user)
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """ Creates a new User object """
    param = request.get_json()

    if not param:
        return "Not a JSON", 400
    if "email" not in param.keys():
        return "Missing email", 400
    if "password" not in param.keys():
        return "Missing password", 400

    new_user = User(**param)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    """ Updates a User object """

    user = storage.get("User", user_id)
    if not user:
        abort(404)

    param = request.get_json()
    if not param:
        return "Not a JSON", 400

    for key, value in param.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)

    user.save()
    return jsonify(user.to_dict()), 200
