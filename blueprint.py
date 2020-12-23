from flask import jsonify, request
from app import db, app
from pprint import pformat
from models import Users, Events, Invited_users
from marshmallow import ValidationError
import datetime
import hashlib
from flask_jwt import current_identity
from flask_jwt_extended import (
     jwt_required, create_access_token, get_jwt_identity
)

from schemas import (
    Credentials,
    UserData,
    EventData
)


def get_current_user():
    return Users.query.filter_by(name=get_jwt_identity()).first()


@app.route('/logout', methods=['GET'])
def logout():
    return jsonify({"msg": "Successfully, you have logged out"}), 200


@app.route('/protected')
@jwt_required
def protected():
    return '%s' % current_identity


def handleEventRequest(request, e_id=None):
    data = request.get_json()
    try:
        event = EventData().load(data)
        event.datetime = datetime.datetime.now()
        if e_id:
            event.uid = e_id
    except ValidationError as e:
        print(e)
        return 'invalid input, object invalid', 400
    if data["invited_users"]:
        invited_users = data["invited_users"]
    else:
        invited_users = None
    return event, invited_users


def addInvitedUsers(e_id, invited_users):
    if not invited_users:
        return
    for u_id in invited_users:
        db.session.add(Invited_users(event_id=e_id, invited_user_uid=u_id))
    try:
        db.session.commit()
    except Exception as e:
        print(e)


def deleteInvitedUsers(e_id=None, invited_user=None):
    invited_rel = []
    if e_id:
        invited_rel += Invited_users.query.filter(
            Invited_users.event_id == e_id).all()
    if invited_user:
        invited_rel += Invited_users.query.filter(
            Invited_users.invited_user_uid == invited_user).all()
    for r in invited_rel:
        db.session.delete(r)
    try:
        db.session.commit()
    except Exception as e:
        print(e)


@app.route("/events", methods=["GET"])
@jwt_required
def show_events():
    events = [e for e in Events.query.outerjoin(Invited_users)
        .filter((Events.owner_uid == get_current_user().uid) | (Invited_users.invited_user_uid == get_current_user().uid))]
    schema = UserData(many=True)
    result = schema.dump(events)
    return pformat(result)


@app.route("/events", methods=["POST"], endpoint='addEvent')
@jwt_required
def addEvent():
    event, invited_users = handleEventRequest(request)
    event.owner_uid = get_current_user().uid
    db.session.add(event)
    db.session.commit()
    addInvitedUsers(e_id=event.uid, invited_users=invited_users)
    return "event created", 201


@app.route("/events/<e_id>", methods=["GET"])
def getEventById(e_id):
    event = Events.query.filter(Events.uid == e_id).first()
    if event:
        result = EventData().dump(event)
        return pformat(result)
    else:
        return "event not found", 400


@app.route("/events/<e_id>", methods=["DELETE"])
@jwt_required
def deleteEventById(e_id):
    if not bool(Events.query.filter(Events.uid == e_id).first()):
        return "this event does not exist", 409
    else:
        event = Events.query.filter(Events.uid == e_id).first()
        deleteInvitedUsers(e_id)
        db.session.delete(event)
        db.session.commit()
        return "event deleted"


@app.route("/events/<e_id>", methods=["PUT"])
@jwt_required
def editEvent(e_id):
    if not bool(Events.query.filter(Events.uid == e_id).first()):
        return "this event does not exist", 409
    else:
        event = Events.query.filter(Events.uid == e_id).first()
        newevent, invited_users = handleEventRequest(request, e_id)
        event.name = newevent.name
        event.description = newevent.description
        db.session.commit()
        deleteInvitedUsers(e_id=e_id)
        addInvitedUsers(e_id, invited_users)
        return "event updated"


@app.route("/user", methods=["POST"])
def createUser():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if bool(Users.query.filter(Users.name == username).first()):
        return "user already exists", 409
    try:
        cred = Credentials().load({"username": username, "password": password})
    except ValidationError:
        return 'invalid input', 400
    db.session.add(Users(name=username, password=hashlib.md5(password.encode()).hexdigest()))
    db.session.commit()
    return f"user {username} has been created with password : {hashlib.md5(password.encode()).hexdigest()}"


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    current_user = Users.query.filter_by(name=username)
    if current_user is None:
        return jsonify({"msg": "Not Found"}), 404
    for i in current_user:
        if i.password == password:
            return jsonify(access_token=create_access_token(identity=username)), 200
    else:
        return jsonify({"Error": "Wrong password"}), 401


@app.route("/user/logout", methods=["GET"])
def logoutUser():
    logout()
    return "logged out"


@app.route("/user", methods=["GET"])
def getUserByUsername():
    user_id = get_jwt_identity()
    user = Users.query.filter(Users.uid == user_id).first()
    if user:
        result = UserData().dump(user)
        return pformat(result)
    else:
        return "user not found", 404


@app.route("/user/<username>", methods=["PUT"])
@jwt_required
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


@app.route("/user/<username>", methods=["DELETE"])
@jwt_required
def deleteUser(username):
    user = Users.query.filter(Users.name == username).first()
    if user:
        deleteInvitedUsers(invited_user=user.uid)
        db.session.delete(user)
        db.session.commit()
        return "deleted user"
    else:
        return "user not found", 404