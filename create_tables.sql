CREATE TABLE users (
    uid SERIAL NOT NULL,
    name VARCHAR,
    PRIMARY KEY (uid)
);

CREATE TABLE events (
    uid SERIAL NOT NULL,
    name VARCHAR,
    datetime VARCHAR,
    owner_uid INTEGER,
    PRIMARY KEY (uid),
    FOREIGN KEY(owner_uid) REFERENCES users (uid)
);
