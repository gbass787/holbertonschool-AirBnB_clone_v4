#!/usr/bin/python3
'''
Create a new view for Review object that handles all default HTTP methods
'''
from models.user import User
from models.city import City
from models.place import Place
from models.review import Review
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
# from flask import make_response


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def return_reviews(place_id):
    '''
    Retrieves the list of all Review objects of a Place, use GET http method
    '''
    # retrieve the object based on the class and its ID, or None if not found
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def return_review_id(review_id):
    ''' Retrieve a Review object using its id, use GET http method '''
    # retrieve the object based on the class and its ID, or None if not found
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review_id(review_id):
    ''' Delete a Review object using its id, ise DELETE http method '''
    # retrieve the object based on the class and its ID, or None if not found
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        # return an empty dictionary with the status code 200
        return (jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    ''' Create a Review object, use POST http method '''
    # transform the HTTP body request to a python dictionary
    body = request.get_json()
    if body is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    # retrieve the object based on the class and its ID, or None if not found
    place = storage.get(Place, place_id)
    if place is None:
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
    if 'text' not in body:
        return (jsonify({'error': 'Missing text'}), 400)

    # save the place_id and user_id in the body dictionary
    body['place_id'] = place_id
    body['user_id'] = user_id
    # create a new instance of Review and pass body dictionary as **kwargs
    obj = Review(**body)
    storage.new(obj)
    storage.save()
    # return the new Review with the status code 201
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review_id(review_id):
    ''' Update a Review object using its id, use PUT http method '''
    # transform the HTTP body request to a python dictionary
    body = request.get_json()
    if body is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    # retrieve the object based on the class and its ID, or None if not found
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        ignore_key = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for key, value in body.items():
            if key not in ignore_key:
                setattr(review, key, value)
            else:
                pass
        storage.save()
        return (jsonify(review.to_dict()), 200)
