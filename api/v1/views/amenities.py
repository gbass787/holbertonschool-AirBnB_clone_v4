#!/usr/bin/python3
''' Module that handles all default RESTFul API '''

from flask import jsonify, abort, request, Response
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def get_amenities():
    """ focus on all the amenity objects """

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return Response("Not a JSON", 400)
        if 'name' not in data:
            return Response("Missing name", 400)
        amenity = Amenity(name=data.get('name'))
        amenity.save()
        return jsonify(amenity.to_dict()), 201

    all_amenities = storage.all('Amenity')
    amenities = []

    for amenity in all_amenities.values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_amenity(amenity_id=None):
    """ focus on just a single state object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            return Response("Not a JSON", 400)
        data['id'] = amenity.id
        data['created_at'] = amenity.created_at
        amenity.__init__(**data)
        amenity.save()
        return jsonify(amenity.to_dict()), 200

    return jsonify(amenity.to_dict())
