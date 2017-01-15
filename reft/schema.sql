DROP TABLE IF EXISTS relation_entities;
DROP TABLE IF EXISTS relation_type;
CREATE TABLE relation_type (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  subject TEXT NOT NULL,
  object TEXT NOT NULL
);

CREATE TABLE relation_entities (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	subject TEXT NOT NULL,
  	object TEXT NOT NULL,
  	relation_type_id INTEGER,
	FOREIGN KEY(relation_type_id) REFERENCES relation_type(relation_type)
);

insert into relation_type(subject, object) values('ORGANIZATION',	'LOCATION');
insert into relation_type(subject, object) values('PERSON',			'LOCATION');
insert into relation_type(subject, object) values('GPE',			'LOCATION');
insert into relation_type(subject, object) values('PERSON',			'ORGANIZATION');
insert into relation_type(subject, object) values('PERSON',			'GPE');
insert into relation_type(subject, object) values('ORGANIZATION',	'GPE');