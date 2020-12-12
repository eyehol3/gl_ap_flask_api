from flask import Flask
from pprint import pprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
# from models import BaseModel
# from models import BaseModel
DB_URI = "postgres://qwerty:123456@localhost:5432/postgres"

# import sqlalchemy as db
# engine = db.create_engine(DB_URI)
# connection = engine.connect()
# Session = db.orm.sessionmaker(bind=engine)
# session = Session()
# BaseModel.metadata.create_all(engine)



app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
db = SQLAlchemy(app)


@app.route('/api/v1/hello-world-10')
def hello_world():
    return 'Hello, World 10'
@app.route('/')
def index():
    return "fslkdjf;laskjf;l"

# db.create_all()
if __name__ == "__main__":
    import blueprint
    app.register_blueprint(blueprint.api_blueprint)
    app.run()