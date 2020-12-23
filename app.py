from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import JWTManager

app = Flask(__name__)
jwt = JWTManager(app)
app.debug = True
DB_URI = "postgres://postgres:postgres@localhost:5432/postgres"
app.config['JWT_SECRET_KEY'] = '2F4A8B8690219C1841B865EB87E8EC40281F7784BA16AEF0408DC712A6F3B4D3'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

SessionFactory = sessionmaker(bind=engine)

BaseModel = declarative_base()

if __name__ == '__main__':

    from models import *
    from schemas import *
    from blueprint import *

    db.create_all()
    app.run()