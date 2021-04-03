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
from models import db, User, Planet, Character, Favorite, Specie, Film
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


@app.route('/register', methods=['POST'])
def create_user():
    email= request.json.get("email",None)
    password= request.json.get("password",None)
    user = User.query.filter_by(email=email,password=password).first()
    if user:
        return jsonify({"msj":"User already exists"}),401
    else:
        new_user=User()
        new_user.email=email
        new_user.password=password
        new_user.is_active=True
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msj":"User created"}),200

@app.route('/login',methods=['GET'])
def login():
    email= request.json.get("email",None)
    password= request.json.get("password",None)
    user = User.query.filter_by(email=email,password=password).first()
    if user:
        return jsonify({"msj":"Welcome"}),200
    else:
        return jsonify({"msj":"Error"}),401


#Return all users
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

#Get all Planets
@app.route('/planet', methods=['GET'])
def get_all_planets():
    result = Planet.query.all()
    all_planets = list(map(lambda x: x.serialize(), result))
    return jsonify(all_planets), 200

#Get one Planet
@app.route('/planet/<int:id>', methods=['GET'])
def get_planet(id):

    planet = Planet.query.get(id)

    if planet is None:
        raise APIException('Planet not found', status_code=404)
  
    return jsonify(planet.serialize()), 200    

#----------------------------------------------CHARACTER----------------------------------------

#Get all characters
@app.route('/character', methods=['GET'])
def get_all_characters():
    result = Character.query.all()
    all_characters = list(map(lambda x: x.serialize(), result))
    return jsonify(all_characters), 200

#Get one Character
@app.route('/character/<int:id>', methods=['GET'])
def get_character(id):

    character = Character.query.get(id)

    if character is None:
        raise APIException('Character not found', status_code=404)
  
    return jsonify(character.serialize()), 200   

#----------------------------------------------SPECIE----------------------------------------

#Get all Species
@app.route('/specie', methods=['GET'])
def get_all_species():
    result = Specie.query.all()
    all_species = list(map(lambda x: x.serialize(), result))
    return jsonify(all_species), 200

#Get one Specie
@app.route('/specie/<int:id>', methods=['GET'])
def get_specie(id):

    specie = Specie.query.get(id)

    if specie is None:
        raise APIException('Specie not found', status_code=404)
  
    return jsonify(specie.serialize()), 200   


#----------------------------------------------FILM----------------------------------------

#Get all Films
@app.route('/film', methods=['GET'])
def get_all_film():
    result = Film.query.all()
    all_films = list(map(lambda x: x.serialize(), result))
    return jsonify(all_films), 200

#Get one Film
@app.route('/film/<int:id>', methods=['GET'])
def get_film(id):

    film = Film.query.get(id)

    if film is None:
        raise APIException('Film not found', status_code=404)
  
    return jsonify(film.serialize()), 200   




# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
