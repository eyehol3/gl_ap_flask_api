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

def addInvitedUsers(e_id, invited_users):
    for u_id in invited_users:
        db.session.add(Invited_users(event_id=e_id, invited_user_uid=u_id))
    try:
        db.session.commit()
    except Exception as e:
        print(e)

def deleteInvitedUsers(e_id=None, invited_user=None):
    invited_rel = []
    if e_id:
        invited_rel += Invited_users.query.filter(Invited_users.event_id == e_id).all()
    if invited_user:
        invited_rel += Invited_users.query.filter(Invited_users.invited_user_uid == invited_user).all()
    # print(invited_rel)
    for r in invited_rel:
        db.session.delete(r)
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
        print(event, "DLSKFJLDSKFJ:DLSKFJD:SFKJ")
        db.session.add(event)
        db.session.commit()
        addInvitedUsers(e_id, invited_users)
        return "event created", 201

@api_blueprint.route("/events/<e_id>", methods=["DELETE"])
def deleteEventById(e_id):
    if not bool(Events.query.filter(Events.uid == e_id).first()):
        return "this event does not exist", 409
    else:
        event = Events.query.filter(Events.uid == e_id).first()
        deleteInvitedUsers(e_id)
        db.session.delete(event)
        db.session.commit()
        return "event deleted"

@api_blueprint.route("/events/<e_id>", methods=["PUT"])
def editEvent(e_id):
    if not bool(Events.query.filter(Events.uid == e_id).first()):
        return "this event does not exist", 409
    else:
        event = Events.query.filter(Events.uid == e_id).first()
        event, invited_users = handleEventRequest(request, e_id)
        db.session.commit()
        deleteInvitedUsers(e_id, invited_users)
        addInvitedUsers(e_id, invited_users)
        return "event updated"

def login(l,p):
    return True
def logout():
    return True
@api_blueprint.route("/user", methods=["POST"])
def createUser():
    username = request.args.get('username')
    password = request.args.get('password')
    if bool(Users.query.filter(Users.name == username).first()):
        return "user already exists", 409
    try:
        cred = Credentials().load({"username":username, "password": password})
    except ValidationError:
        return 'invalid input', 400
    db.session.add(Users(name=username))
    db.session.commit()
    login(username, password)
    return f"user {username} has been created"


@api_blueprint.route("/user/login", methods=["GET"])
def loginUser():
    username = request.args.get('username')
    password = request.args.get('password')
    if not bool(Users.query.filter(Users.name == username).first()):
        return "user does not exist", 409
    try:
        cred = Credentials().load({"username":username, "password": password})
    except ValidationError:
        return 'invalid input', 400
    if login(username, password):
        return f"succsessfully logged in"
    else:
        return "Invalid username/password supplied"

@api_blueprint.route("/user/logout", methods=["GET"])
def logoutUser():
    logout()
    return "logged out"

@api_blueprint.route("/user/<username>", methods=["GET"])
def getUserByUsername(username):
    user = Users.query.filter(Users.name == username).first()
    if user:
        result = UserData().dump(user)
        return pformat(result)
    else:
        return "user not found", 404

@api_blueprint.route("/user/<username>", methods=["PUT"])
def updateUser(username):
    user = Users.query.filter(Users.name == username).first()
    data = request.get_json()
    if not user:
        return "user not found", 404
    try:
        newuser = UserData().load(data)
        user.name = newuser.name
        db.session.commit()
        return "user updated"
    except ValidationError as e:
        print(e)
        return 'invalid input supplied', 400

@api_blueprint.route("/user/<username>", methods=["DELETE"])
def deleteUser(username):
    user = Users.query.filter(Users.name == username).first()
    if user:
        # result = UserData().dump(user)
        # pprint(result)
        deleteInvitedUsers(invited_user=user.uid)
        db.session.delete(user)
        db.session.commit()
        return "deleted user"
    else:
        return "user not found", 404
