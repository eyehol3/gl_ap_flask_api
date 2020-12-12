
from flask import Blueprint, jsonify, request
# from sqlalchemy.orm import Session
from app import db

from models import Users, Events
# from schemas import (
#     Credentials,
#     UserData,
#     EventData
# )
# from flask import Flask

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route("/events", methods=["GET"])
def show_events():
    return jsonify(Events.query.all())
    # return jsonify(session.query(Events).all())
    # return jsonify(dump(Events))

# @api_blueprint.route("/auth", methods=["POST"])
# def auth():
#     Credentials().load(request.json)
#     return jsonify(AccessToken().dump({"access_token": ""}))


# @api_blueprint.route("/user", methods=["GET"])
# @db_lifecycle
# def list_users():
    # args = ListUsersRequest().load(request.args)
    # users = db_utils.list_users(
        # args.get("email"), args.get("first_name"), args.get("last_name")
    # )
    # return jsonify(UserData(many=True).dump(users))
