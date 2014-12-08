V1:
CREATE TABLE schedules(Tag INTEGER PRIMARY KEY, Name TEXT, Amount REAL, Slot1 TEXT, Slot2 TEXT);
 INSERT INTO schedules VALUES(1, "Rex", 1, "08:00:00", "16:00:00");
 INSERT INTO schedules VALUES(2, "Rover", 0.5, "08:00:00", "17:00:00");
 INSERT INTO schedules VALUES(3, "Jake", 1.5, "09:00:00", "18:00:00");

V2:
CREATE TABLE settings(tagNo INT, tagID TEXT PRIMARY KEY, amount REAL, slot1Start INT, slot1End INT, slot2Start INT, slot2End INT); 