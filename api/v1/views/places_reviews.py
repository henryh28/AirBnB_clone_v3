#!/usr/bin/python3
""" RESTful routes for Review objects """

from models import storage
from models.review import Review
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def all_reviews(place_id):
    """ Retrieves the list of all Review objects of a Place object"""
    review_list = []

    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    for entry in place.reviews:
        review_list.append(entry.to_dict())
    return jsonify(review_list)


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def get_review(review_id):
    """ Retrieves a Review object """
    review = storage.get("Review", review_id)

    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a Review object """
    review = storage.get("Review", review_id)

    if review:
        storage.delete(review)
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """ Creates a new Review object """
    param = request.get_json()
    if not param:
        return "Not a JSON", 400
    if "user_id" not in param.keys():
        return "Missing user_id", 400
    if "text" not in param.keys():
        return "Missing text", 400

    place = storage.get("Place", place_id)
    user = storage.get("User", param["user_id"])
    if not place or not user:
        abort(404)

    new_review = Review(**param)
    new_review.place_id = place_id
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def update_review(review_id):
    """ Updates a Review object """

    review = storage.get("Review", review_id)
    if not review:
        abort(404)

    param = request.get_json()
    if not param:
        return "Not a JSON", 400

    for key, value in param.items():
        if key not in ["id", "user_id", "place_id", "created_at",
                       "updated_at"]:
            setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict()), 200
