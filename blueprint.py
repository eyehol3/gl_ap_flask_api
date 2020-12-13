from flask import Blueprint, jsonify, request
from app import db
from pprint import pformat, pprint
from models import Users, Events, Invited_users
from marshmallow import ValidationError
import datetime
from schemas import (
    Credentials,
    UserData,
    EventData
)

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route("/events", methods=["GET"])
def show_events():
    events = [e for e in Events.query.all()]
    schema = UserData(many=True)
    result = schema.dump(events)
    return pformat(result)

@api_blueprint.route("/events/<e_id>", methods=["GET"])
def getEventById(e_id):
    event = Events.query.filter(Events.uid == e_id).first()
    if event:
        result = EventData().dump(event)
        return pformat(result)
    else:
        return "event not found", 400

def handleEventRequest(request, e_id):
    data = request.get_json()
    try:
        event = EventData().load(data)
        event.datetime = datetime.datetime.now()
        event.uid = e_id
    except ValidationError as e:
            print(e)
            return 'invalid input, object invalid', 400
    # pprint(data)
    if data["invited_users"]:
        invited_users = data["invited_users"]
    else:
        invited_users = None 
    return event, invited_users

def handleInvitedUsers(e_id, invited_users):
    for u_id in invited_users:
        db.session.add(Invited_users(event_id=e_id, invited_user_uid=u_id))
    try:
        db.session.commit()
    except Exception as e:
        print(e)

@api_blueprint.route("/events/<e_id>", methods=["POST"])
def addEvent(e_id):
    if bool(Events.query.filter(Events.uid == e_id).first()):
        return "this event already exists", 409
    else:
        
        event, invited_users = handleEventRequest(request, e_id)
        db.session.add(event)
        db.session.commit()
        handleInvitedUsers(e_id, invited_users)
        return "event created", 201

@api_blueprint.route("/events/<e_id>", methods=["PUT"])
def editEvent(e_id):
    pass


# @api_blueprint.route("/user", methods=["GET"])
# @db_lifecycle
# def list_users():
    # args = ListUsersRequest().load(request.args)
    # users = db_utils.list_users(
        # args.get("email"), args.get("first_name"), args.get("last_name")
    # )
    # return jsonify(UserData(many=True).dump(users))
