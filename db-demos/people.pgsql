-- Schema
create table colors (
  name varchar primary key
);

create table people (
  id integer primary key,
  name varchar not null,
  fav_color varchar references colors (name)
);

-- Queries
insert into colors values ('green');
insert into colors values ('pink');
insert into colors values ('black');
insert into colors values ('white');
insert into colors values ('rainbow');

select * from colors;

insert into people values (1, 'Anya', 'green');
insert into people values (2, 'Krys', 'rainbow');

insert into colors values ('purple');
insert into people values (3, 'Pistacho', 'purple');
insert into people values (4, 'Unknown', 'purple');

select * from people;

update people SET fav_color = 'white' WHERE id = 3;
delete from people p using colors c where p.fav_color = c.name AND c.name = 'purple';
select * from people;

create table roles (
  id int primary key,
  name varchar not null,
  relation varchar
 );

 insert into roles (id, name) VALUES (1, 'mother');
 insert into roles VALUES (2, 'baby');

 select * from roles;

alter table people add column role int references roles (id);
 select * from people;

alter table roles drop column relation;
 select * from roles;

update people set role = 2 where fav_color = (SELECT name from colors c where c.name = 'white');
update people set role = 1 where role IS NULL;

select * from people;

  SELECT  p.name, fav_color, r.name
     FROM people p, roles r
     WHERE p.role = r.id;

 SELECT r.name, count(p.*)
 FROM roles r, people p
 WHERE p.role = r.id
 GROUP BY r.name;