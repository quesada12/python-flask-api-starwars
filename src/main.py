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
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

app.config["JWT_SECRET_KEY"] = "darksiderules"
jwt = JWTManager(app)

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
    user = User.query.filter_by(email=email).first()
    if user is None:
        new_user=User()
        new_user.email=email
        new_user.password=password
        new_user.is_active=True
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msj":"User created"}),200
    else:
        return jsonify({"msj":"User already exists"}),401

@app.route('/login',methods=['POST'])
def login():
    email= request.json.get("email",None)
    password= request.json.get("password",None)
    user = User.query.filter_by(email=email,password=password).first()
    if user:
        access_token = create_access_token(identity=user.id)
        return jsonify({"token":access_token}),200
    else:
        return jsonify({"msj":"Error"}),401

@app.route('/user',methods=['POST'])
def get_user():
    email= request.json.get("email",None)
    password= request.json.get("password",None)
    user = User.query.filter_by(email=email,password=password).first()
    if user:
        return jsonify(user.serialize()),200
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
@jwt_required()
def get_user_favorite(tid):

    user = User.query.get(tid)

    if user is None:
        raise APIException('User not found', status_code=404)

    return jsonify(user.serializeFavorites()), 200  

#Insert a favorite
@app.route('/user/<int:tid>/favorites', methods=['POST'])
@jwt_required()
def post_user_favorite(tid):

    user = User.query.get(tid)

    if user is None:
        raise APIException('User not found', status_code=404)


    request_body = request.get_json()
    favorite = Favorite(user_id=tid, favorite_id=request_body["favorite_id"],favorite_name=request_body["favorite_name"],favorite_type=request_body["favorite_type"])
    db.session.add(favorite)
    db.session.commit()

    return jsonify(favorite.serialize()), 200 

#Delete a favorite
@app.route('/favorite/<int:fid>', methods=['DELETE'])
@jwt_required()
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

@app.route('/favorite',methods=['POST'])
@jwt_required()
def get_favorite():
    favorite_name= request.json.get("favorite_name",None)
    favorite_type= request.json.get("favorite_type",None)
    favorite_id= request.json.get("favorite_id",None)
    user_id= request.json.get("user_id",None)
    favorite = Favorite.query.filter_by(favorite_name=favorite_name,favorite_id=favorite_id,favorite_type=favorite_type,user_id=user_id).first()
    if favorite:
        return jsonify(favorite.serialize()),200
    else:
        return jsonify({"msj":"Error"}),401

#----------------------------------------------PLANET----------------------------------------

#Get all Planets
@app.route('/planet', methods=['GET'])
@jwt_required()
def get_all_planets():
    result = Planet.query.all()
    all_planets = list(map(lambda x: x.serialize(), result))
    return jsonify(all_planets), 200

#Get one Planet
@app.route('/planet/<int:id>', methods=['GET'])
@jwt_required()
def get_planet(id):

    planet = Planet.query.get(id)

    if planet is None:
        raise APIException('Planet not found', status_code=404)
  
    return jsonify(planet.serialize()), 200    

#----------------------------------------------CHARACTER----------------------------------------

#Get all characters
@app.route('/character', methods=['GET'])
@jwt_required()
def get_all_characters():
    result = Character.query.all()
    all_characters = list(map(lambda x: x.serialize(), result))
    return jsonify(all_characters), 200

#Get one Character
@app.route('/character/<int:id>', methods=['GET'])
@jwt_required()
def get_character(id):

    character = Character.query.get(id)

    if character is None:
        raise APIException('Character not found', status_code=404)
  
    return jsonify(character.serialize()), 200   

#----------------------------------------------SPECIE----------------------------------------

#Get all Species
@app.route('/specie', methods=['GET'])
@jwt_required()
def get_all_species():
    result = Specie.query.all()
    all_species = list(map(lambda x: x.serialize(), result))
    return jsonify(all_species), 200

#Get one Specie
@app.route('/specie/<int:id>', methods=['GET'])
@jwt_required()
def get_specie(id):

    specie = Specie.query.get(id)

    if specie is None:
        raise APIException('Specie not found', status_code=404)
  
    return jsonify(specie.serialize()), 200   


#----------------------------------------------FILM----------------------------------------

#Get all Films
@app.route('/film', methods=['GET'])
@jwt_required()
def get_all_film():
    result = Film.query.all()
    all_films = list(map(lambda x: x.serialize(), result))
    return jsonify(all_films), 200

#Get one Film
@app.route('/film/<int:id>', methods=['GET'])
@jwt_required()
def get_film(id):

    film = Film.query.get(id)

    if film is None:
        raise APIException('Film not found', status_code=404)
  
    return jsonify(film.serialize()), 200   



# #Insert a favorite
# @app.route('/data', methods=['GET'])
# def insert_test_data():

#     user = User(email="prueba@prueba.com",password="starwars",is_active=True)
#     db.session.add(user)
#     planet1 = Planet(name="Tattoine",diameter=10465,rotation_period=23,orbital_period=304,gravity="1 standard",population=200000,climate="arid",terrain="desert",surface_water=1)
#     db.session.add(planet1)
#     planet2 = Planet(name="Alderaan",diameter=12500,rotation_period=24,orbital_period=364,gravity="1 standard",population=2000000000,climate="temperate",terrain="grassland,mountains",surface_water=40)
#     db.session.add(planet2)

#     character = Character(name="Luke Skywalker",height=172,mass=77,hair_color="blond",skin_color="fair",eye_color="blue",birth_year="19BBY",gender="male",planet_id=1)
#     db.session.add(character)
#     character2 = Character(name="Leia Organa",height=150,mass=49,hair_color="brown",skin_color="light",eye_color="brown",birth_year="19BBY",gender="female",planet_id=2)
#     db.session.add(character2)
#     specie= Specie(name="Human",classification="mammal",designation="sentient",average_height=180,average_lifespan=120,hair_colors="blonde, brown, black, red",skin_colors="caucasian, black, asian, hispanic",eye_colors="brown, blue, green, hazel, grey, amber",language="Galactic Basic",planet_id=1)
#     db.session.add(specie)
#     film = Film(title="A New Hope",episode_id=4,producer="Gary Kurtz, Rick McCallum",director="George Lucas",release_date="1977-05-25",opening="It is a period of civil war. Rebel spaceships, striking from a hidden base, have won their first victory against the evil Galactic Empire. During the battle, Rebel spies managed to steal secret plans to the Empire's ultimate weapon, the DEATH STAR, an armored space station with enough power to destroy an entire planet. Pursued by the Empire's sinister agents, Princess Leia races home aboard her starship, custodian of the stolen plans that can save her people and restore freedom to the galaxy....")
#     db.session.add(film)

#     db.session.commit()
#     return jsonify({"msg","done"}), 200 


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
