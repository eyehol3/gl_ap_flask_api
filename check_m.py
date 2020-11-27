from models import Session, Users, Events

session = Session()

user = Users(uid=1, name="Peter")
event1 = Events(uid=1, name="My birthday", datetime='tomorrow', owner=user)
event2 = Events(uid=2, name="Promotion on job", datetime='today', owner=user)

session.add(user)
session.add(event1)
session.add(event2)
session.commit()

print(session.query(Users).all())
print(session.query(Events).all())

session.close()
