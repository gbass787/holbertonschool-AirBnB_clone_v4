#!/usr/bin/python3
""" retrieve an object into a valid JSON """

from flask import jsonify, abort, request, Response
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_places(city_id=None):
    """ focus on all the place objects """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return Response("Not a JSON", 400)
        if 'user_id' not in data:
            return Response("Missing user_id", 400)
        if 'name' not in data:
            return Response("Missing name", 400)
        user = storage.get(User, data.get('user_id'))
        if not user:
            abort(404)
        place = Place(city_id=city.id, user_id=user.id, name=data.get('name'))
        place.save()
        return jsonify(place.to_dict()), 201

    all_places = city.places
    places = []

    for place in all_places:
        places.append(place.to_dict())
    return jsonify(places), 200


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_place(place_id=None):
    """ focus only in a single place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            return Response("Not a JSON", 400)
        data['id'] = place.id
        data['user_id'] = place.user_id
        data['city_id'] = place.city_id
        data['created_at'] = place.created_at
        place.__init__(**data)
        place.save()
        return jsonify(place.to_dict()), 200

    return jsonify(place.to_dict()), 200
