
CREATE TABLE channel(
   id TEXT PRIMARY KEY,
   title TEXT
);

CREATE TABLE video(
   id TEXT PRIMARY KEY,
   date TEXT,
   title TEXT,
   channelid TEXT
);

CREATE TABLE rating(
   userchannelid TEXT NOT NULL,
   videoid TEXT NOT NULL,
   rating TEXT,
   date TEXT,
   PRIMARY KEY (userchannelid, videoid)
);

CREATE TABLE watched(
   userchannelid TEXT NOT NULL,
   videoid TEXT NOT NULL,
   date TEXT,
   PRIMARY KEY (userchannelid, videoid)
);

CREATE TABLE subscribed(
   userchannelid TEXT NOT NULL,
   channelid TEXT NOT NULL,
   date TEXT,
   PRIMARY KEY (userchannelid, channelid)
);


--,FOREIGN KEY(channelid) REFERENCES channel(id)
--ALTER TABLE rating ADD date TEXT;
            conn.execute("INSERT INTO channel (id,title) VALUES(?,?) ON CONFLICT(id) DO UPDATE SET date=? WHERE (date=='' OR date>?) AND ?!='';",
                         (cid,cdate,ctitle,cdate,cdate,cdate))

UPDATE channel SET date='' WHERE date='9999-01-01T00:00:00Z';

INSERT INTO channel (id, date, title)
VALUES ('', '', '');


INSERT INTO channel (id, date, title)
VALUES ('testchannelid', '2018-12-13T16:05:16.83931Z', 'testchanneltitle');

INSERT INTO video (id, date, title, rating, channelid)
VALUES ('testvideoid', '1981-3-4', 'testvideotitle','','testchannelid');


INSERT INTO channel (id, date, title)
VALUES('testid', '2018-09-20T15:59:28.55012Z', 'yyy')
ON CONFLICT(id) DO UPDATE SET date = '2018-09-20T15:59:28.55012Z'
WHERE date > '2018-09-20T15:59:28.55012Z';

INSERT OR REPLACE INTO channel (id, date, title) VALUES('testid', '1980-1-1', 'y');
INSERT INTO channel (id, date, title) VALUES('testid', '1980-1-1', 'z') ON DUPLICATE KEY UPDATE date=VALUES('1980-1-1');


CREATE TRIGGER channel_insert_trigger INSTEAD OF INSERT ON channel
WHEN EXISTS(SELECT id FROM channel where id = NEW.id)
BEGIN
END;

======


UPDATE video
SET title = 'VIDEOTITLE'
WHERE
    id='VIDEOID'; 