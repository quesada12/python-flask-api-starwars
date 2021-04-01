from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship('Favorite',backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorites":list(map(lambda x: x.serialize(), self.favorites))
            # do not serialize the password, its a security breach
        }

#STAR WARS CLASSES

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    diameter = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    gravity = db.Column(db.String(250))
    population = db.Column(db.Integer, nullable=False)
    climate = db.Column(db.String(250))
    terrain = db.Column(db.String(250), nullable=False)
    surface_water = db.Column(db.Integer)  
    characters = db.relationship('Character',backref='planet', lazy=True)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter":self.diameter,
            "rotation_period":self.rotation_period,
            "orbital_period":self.orbital_period,
            "gravity":self.gravity,
            "population":self.population,
            "climate":self.climate,
            "terrain":self.terrain,
            "surface_water":self.surface_water,
            "characters": list(map(lambda x: x.serialize(), self.characters)),
            #"species": list(map(lambda x: x.serialize(), self.species))
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    mass = db.Column(db.Integer, nullable=False)
    hair_color = db.Column(db.String(250))
    skin_color = db.Column(db.String(250))
    eye_color = db.Column(db.String(250))
    birth_year = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(30), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'),nullable=True)

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "height":self.height,
            "mass":self.mass,
            "hair_color":self.hair_color,
            "skin_color":self.skin_color,
            "eye_color":self.eye_color,
            "birth_year":self.birth_year,
            "gender": self.gender,
            "planet_id":self.planet_id
        }

class Favorite(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=True)
    favorite_id=db.Column(db.Integer, nullable=False)
    favorite_name=db.Column(db.String(250),nullable=False)
    favorite_type = db.Column(db.String(1))

    def __repr__(self):
        return '<Favorite %r>' % self.user_id

    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "favorite_id": self.favorite_id,
            "favorite_name": self.favorite_name,
            "favorite_type": self.favorite_type
        }