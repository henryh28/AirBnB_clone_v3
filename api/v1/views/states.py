#!/usr/bin/python3
""" States object """

from models import storage
from models.state import State
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def all_states():
    """ Retrieves the list of all State objects """
    state_list = []

    for entry in storage.all("State").values():
        state_list.append(entry.to_dict())
    return jsonify(state_list)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def one_state(state_id):
    """ Retrieves a State object """
    state = storage.get("State", state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """ Deletes a State object """
    state = storage.get("State", state_id)
    if state:
        storage.delete(state)
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/states/", methods=["POST"], strict_slashes=False)
def create_state():
    """ Create a new State object """
    param = request.get_json()
    if not param:
        return "Not a JSON", 400
    elif "name" not in param.keys():
        return "Missing name", 400

    new_state = State(**param)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """ Updates a State object """
    state = storage.get("State", state_id)
    params = request.get_json()
    if not state:
        abort(404)
    if not params:
        return "Not a JSON", 400

    for key, value in params.items():
        setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
