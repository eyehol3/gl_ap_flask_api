from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
DB_URI = "postgres://postgres:123456@localhost:5432/flask_api"
app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_ECHO"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
db = SQLAlchemy(app)


if __name__ == "__main__":

    from sqlalchemy_utils import create_database, database_exists
    from models import Users, Events, Invited_users
    import blueprint

    if not database_exists(DB_URI):
        create_database(DB_URI)

    @app.route('/api/v1/hello-world-10')
    def hello_world():
        return 'Hello, World 10'

    @app.route('/')
    def index():
        return "fslkdjf;laskjf;l"

    # db.drop_all()
    # db.create_all()
    # db.drop_all()

    # me = Users(uid=1, name='nstr')
    

    app.register_blueprint(blueprint.api_blueprint)
    app.run()
