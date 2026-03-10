INSERT INTO
    users
VALUES
    (
        1,
        'alban@mail.com',
        '$argon2id$v=19$m=65536,t=3,p=4$d9xEDNiyH/cdO+6fn9k7iw$Eiwz24u4dtvRa1OMH6MPL620vG4uv2XcqQjpiPx1H/w',
        'Alban'
    );

INSERT INTO
    universe ("creator_id", "name", "description", "version")
VALUES
    (
        1,
        'My First Universe',
        'This is my first universe. I enjoy creating it !',
        '0.1'
    );

INSERT INTO
    entities ("name", "universe_id", "creator_id")
VALUES
    ('Alban', 1, 1);

INSERT INTO
    text_blocks ("title", "content", "creator_id", "entity_id")
VALUES
    (
        'Id',
        'First Name : Alban\nFamily Name : GENTA\nAge : 25',
        1,
        1
    );