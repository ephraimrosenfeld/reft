DROP TABLE IF EXISTS relation_entities;
DROP TABLE IF EXISTS relations;
CREATE TABLE relations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  subject TEXT NOT NULL,
  object TEXT NOT NULL
);

CREATE TABLE relation_entities (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	subject TEXT NOT NULL,
  	object TEXT NOT NULL,
  	relations_id INTEGER,
	FOREIGN KEY(relations_id) REFERENCES relations(relations)
);

insert into relations(subject, object) values('ORGANIZATION',	'LOCATION');
insert into relations(subject, object) values('PERSON',			'LOCATION');
insert into relations(subject, object) values('GPE',			'LOCATION');
insert into relations(subject, object) values('PERSON',			'ORGANIZATION');
insert into relations(subject, object) values('PERSON',			'GPE');