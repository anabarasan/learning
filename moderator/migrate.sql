ALTER TABLE vote RENAME TO sqlitestudio_temp_table;

CREATE TABLE vote (
    id     INTEGER NOT NULL,
    topic  INTEGER,
    voter  INTEGER,
    [like] INTEGER DEFAULT (0),
    PRIMARY KEY (
        id
    ),
    FOREIGN KEY (
        topic
    )
    REFERENCES topic (id),
    FOREIGN KEY (
        voter
    )
    REFERENCES user (id) 
);

INSERT INTO vote (
                     id,
                     topic,
                     voter
                 )
                 SELECT id,
                        topic,
                        voter
                   FROM sqlitestudio_temp_table;

DROP TABLE sqlitestudio_temp_table;
