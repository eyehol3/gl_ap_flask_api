from models import Session, Users, Events, Invited_users

session = Session()

user = Users(uid=3, name="Nestor")
event1 = Events(uid=3, name="My funeral", datetime='tomorrow', owner=user)
event2 = Events(uid=4, name="I was fired from job", datetime='today', owner=user)
inv_user = Invited_users(uid=5, event_id=3, invited_user_uid=9)

session.commit()

print(session.query(Users).all())
print(session.query(Events).all())

session.close()
