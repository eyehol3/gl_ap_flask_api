CREATE TABLE users (
    uid SERIAL NOT NULL,
    name VARCHAR,
    PRIMARY KEY (uid)
);

CREATE TABLE events (
    uid SERIAL NOT NULL,
    name VARCHAR,
    datetime VARCHAR,
    description VARCHAR,
    owner_uid INTEGER,

    PRIMARY KEY (uid),
    FOREIGN KEY(owner_uid) REFERENCES users (uid)
);

CREATE TABLE invited_users (
    event_id SERIAL NOT NULL REFERENCES events(uid),
    invited_user_uid INTEGER REFERENCES users(uid)
    PRIMARY KEY(event_id, invited_user_uid)
);

