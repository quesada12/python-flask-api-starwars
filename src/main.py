"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, Favorite, Specie
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#----------------------------------------------USER & FAVORITES----------------------------------------

#Return user's info
@app.route('/user', methods=['GET'])
def get_all_users():

    result = User.query.all()
    all_users = list(map(lambda x: x.serialize(), result))
    return jsonify(all_users), 200

#Return favorites of a user
@app.route('/user/<int:tid>/favorites', methods=['GET'])
def get_user_favorite(tid):

    user = User.query.get(tid)

    if user is None:
        raise APIException('User not found', status_code=404)

    return jsonify(user.serializeFavorites()), 200  

#Insert a favorite
@app.route('/user/<int:tid>/favorites', methods=['POST'])
def post_user_favorite(tid):

    user = User.query.get(tid)

    if user is None:
        raise APIException('User not found', status_code=404)

    request_body = request.get_json()
    favorite = Favorite(user_id=tid, favorite_id=request_body["favorite_id"],favorite_name=request_body["favorite_name"],favorite_type=request_body["favorite_type"])
    db.session.add(favorite)
    db.session.commit()

    return jsonify(user.get_user_favorites()), 200 

#Delete a favorite
@app.route('/favorite/<int:fid>', methods=['DELETE'])
def delete_favorite(fid):

    favorite = Favorite.query.get(fid)

    if favorite is None:
        raise APIException('Favorite not found', status_code=404)
    db.session.delete(favorite)
    db.session.commit()

    response = {
        "msg":"Favorite deleted"
    }

    return jsonify(response), 200    

#----------------------------------------------PLANET----------------------------------------

@app.route('/planet', methods=['GET'])
def get_all_planets():
    result = Planet.query.all()
    all_planets = list(map(lambda x: x.serialize(), result))
    return jsonify(all_planets), 200

#----------------------------------------------CHARACTER----------------------------------------

@app.route('/character', methods=['GET'])
def get_all_characters():
    result = Character.query.all()
    all_characters = list(map(lambda x: x.serialize(), result))
    return jsonify(all_characters), 200

#----------------------------------------------SPECIE----------------------------------------

@app.route('/specie', methods=['GET'])
def get_all_species():
    result = Specie.query.all()
    all_species = list(map(lambda x: x.serialize(), result))
    return jsonify(all_species), 200



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
