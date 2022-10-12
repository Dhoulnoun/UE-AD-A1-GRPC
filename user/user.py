from flask import Flask, render_template, request, jsonify, make_response, url_for
import requests
import json
from werkzeug.exceptions import NotFound

import grpc
from concurrent import futures
# I saw the imports but relative to the tp's schema I don't see the need for them or at least for TP vert
# import booking_pb2
# import booking_pb2_grpc
import movie_pb2
import movie_pb2_grpc
from client.client import get_movie_by_id

app = Flask(__name__)

PORT = 3004
HOST = '0.0.0.0'

with open('{}/data/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/user/site_map", methods=['GET'])
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return make_response(jsonify(links), 200)


# root message
@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


# get all users
@app.route("/users", methods=['GET'])
def get_users():
    res = make_response(jsonify(users), 200)
    return res


# get user by id
@app.route("/users/<userid>", methods=['GET'])
def get_user_byid(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            res = make_response(jsonify(user), 200)
            return res
        return make_response(jsonify({"error": "User ID not found"}), 404)


# create user
@app.route("/users", methods=['POST'])
def create_user():
    user = request.get_json()
    for u in users:
        if u["id"] == user["id"]:
            return make_response(jsonify({"error": "User ID already exists"}), 400)
    users.append(user)
    res = make_response(jsonify(user), 201)
    return res


# update user
@app.route("/users/<userid>", methods=['PUT'])
def update_user(userid):
    newUser = request.get_json()
    for user in users:
        if str(user["id"]) == str(userid):
            user["name"] = newUser["name"]
            user["email"] = newUser["email"]
            users.append(newUser)
            res = make_response(jsonify(user), 200)
            return res


# get the bookings related to a user
@app.route("/bookedmovies/<userid>", methods=['GET'])
def get_booking_for_user(userid):
    with grpc.insecure_channel('localhost:3001') as channel:
        stub = movie_pb2_grpc.MovieStub(channel)
        for user in users:
            if str(user["id"]) == str(userid):
                res = requests.get(f'http://localhost:3003/bookings/{userid}')
                booking = res.json()
                dates = booking["dates"]
                all_movies = {'movies': []}
                for date in dates:
                    for movie_id in date["movies"]:
                        movieid = movie_pb2.MovieID(id=movie_id)
                        movie = get_movie_by_id(stub, movieid)
                        # Cette partie est super importante pour qu'on renvoie un json avec les infos du film
                        all_movies['movies'].append(
                            {"title": movie.title, "rating": movie.rating, "director": movie.director,
                             "id": movie.id})
                        print(all_movies)
            res = make_response(jsonify(all_movies), 200)
            channel.close()
            return res

    return make_response(jsonify({"error": "bad input parameter"}), 400)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT, debug=True)
