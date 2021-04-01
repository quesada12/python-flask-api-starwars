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
from models import db, User, Planet, Character, Favorite
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

@app.route('/user', methods=['GET'])
def get_all_users():

    result = User.query.all()
    all_users = list(map(lambda x: x.serialize(), result))
    return jsonify(all_users), 200

@app.route('/planet', methods=['GET'])
def get_all_planets():
    result = Planet.query.all()
    all_planets = list(map(lambda x: x.serialize(), result))
    return jsonify(all_planets), 200

@app.route('/character', methods=['GET'])
def get_all_characters():
    result = Character.query.all()
    all_characters = list(map(lambda x: x.serialize(), result))
    return jsonify(all_characters), 200

@app.route('/favorite', methods=['GET'])
def get_all_favorites():
    result = Favorite.query.all()
    all_favorites = list(map(lambda x: x.serialize(), result))
    return jsonify(all_favorites), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
