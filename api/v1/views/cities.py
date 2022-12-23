#!/usr/bin/python3
"""
Create a new view for cities objects that handles all default HTTP methods
"""
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
# from flask import make_response


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def return_cities(state_id):
    """Retrieves the list of all State objects, use GET method"""
    # save all the objects in State class from database
    states = storage.get(State, state_id)
    # If the state_id is not linked to any State object, raise a 404 error
    if states is None:
        abort(404)

    cities = []
    for city in states.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def return_cities_id(city_id):
    """
    Return City objects by id or 404 if the id does not exist
    """
    cities = storage.get(City, city_id)

    # If the city_id is not linked to any City object, raise a 404 error
    if cities is None:
        abort(404)
    return jsonify(cities.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_cities_id(city_id):
    """Delete a city object using a specific id"""
    # save the object with the specific id from database
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        # return an empty dictionary with the status code 200
        return (jsonify({}), 200)


@app_views.route('/states/<state_id>/cities/', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    ''' Create a State object '''
    # transform the HTTP body request to a python dictionary
    body = request.get_json()
    if body is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    # create a new instance of State and pass body dict as **kwargs
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    if 'name' not in body:
        return (jsonify({'error': 'Missing name'}), 400)

    body['state_id'] = state_id
    obj = City(**body)

    storage.new(obj)
    storage.save()

    return (jsonify(obj.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_cities_id(city_id):
    ''' Update a State object '''
    body = request.get_json()
    if body is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        ignore_key = ['id', 'state_at', 'created_at' 'updated_at']
        for key, value in body.items():
            if key not in ignore_key:
                setattr(city, key, value)
            else:
                pass
        storage.save()
        return (jsonify(city.to_dict()), 200)
