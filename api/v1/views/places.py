#!/usr/bin/python3
'''
Create a new view for Place objects that handles all default HTTP methods
'''
from models.user import User
from models.city import City
from models.place import Place
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
# from flask import make_response


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def return_places(city_id):
    '''
    Retrieves the list of all Place objects of a City, use GET http method
    '''
    # retrieve the object based on the class and its ID, or None if not found
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def return_place_id(place_id):
    ''' Retrieve a Place object using its id, use GET http method '''
    # retrieve the object based on the class and its ID, or None if not found
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_id(place_id):
    ''' Delete a Place object using its id, ise DELETE http method '''
    # retrieve the object based on the class and its ID, or None if not found
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        # return an empty dictionary with the status code 200
        return (jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    ''' Create a Place object, use POST http method '''
    # transform the HTTP body request to a python dictionary
    body = request.get_json()
    if body is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    # retrieve the object based on the class and its ID, or None if not found
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    # if the body dictionary doesn’t contain the key user_id,
    # raise a 400 error with a message
    if 'user_id' not in body:
        return (jsonify({'error': 'Missing user_id'}), 400)
    # use the python method get to obtain the user_id from body dictionary
    user_id = body.get('user_id')
    # use our custom method get to
    # retrieve the object based on the class and its ID, or None if not found
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    # If the body dictionary doesn’t contain the key name,
    # raise a 400 error with a message
    if 'name' not in body:
        return (jsonify({'error': 'Missing name'}), 400)

    # save the city_id and user_id in the body dictionary
    body['city_id'] = city_id
    body['user_id'] = user_id
    # create a new instance of Place and pass body dictionary as **kwargs
    obj = Place(**body)
    storage.new(obj)
    storage.save()
    # return the new Place with the status code 201
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place_id(place_id):
    ''' Update a Place object using its id, use PUT http method '''
    # transform the HTTP body request to a python dictionary
    body = request.get_json()
    if body is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    # retrieve the object based on the class and its ID, or None if not found
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        ignore_key = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in body.items():
            if key not in ignore_key:
                setattr(place, key, value)
            else:
                pass
        storage.save()
        return (jsonify(place.to_dict()), 200)
