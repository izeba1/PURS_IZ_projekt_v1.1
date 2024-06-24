DROP DATABASE IF EXISTS projektdb;
CREATE DATABASE projektdb;
USE projektdb;

CREATE TABLE zadana_vrijednost (
	id INT PRIMARY KEY AUTO_INCREMENT,
    vrijednost INT
);

INSERT INTO zadana_vrijednost(vrijednost) VALUES
	('300');


CREATE TABLE co_vrijednost (
	id INT PRIMARY KEY AUTO_INCREMENT,
    datum DATETIME,
    vrijednost INT
);
INSERT INTO co_vrijednost(datum, vrijednost) VALUES
	('2023-10-10 12:20:35', '23'),
    ('2023-10-11 11:20:35', '20'),
    ('2023-10-12 10:20:35', '22'),
    ('2023-10-13 09:20:35', '18'),
    ('2023-10-13 09:20:35', '18'),
    ('2023-10-13 09:20:35', '18'),
    ('2023-10-13 09:20:35', '18'),
    ('2023-10-13 09:20:35', '18'),
    ('2023-10-13 09:20:35', '18'),
    ('2023-10-13 09:20:35', '18'),
    ('2023-10-13 09:20:35', '18'),
    ('2023-10-13 09:20:35', '18'),
    ('2023-10-13 09:20:35', '18'),
    ('2023-10-13 09:20:35', '18'),
    ('2023-10-13 09:20:35', '18'),
    ('2023-10-13 09:20:35', '18'),
    ('2023-10-13 09:20:35', '18'),
    ('2023-10-13 09:20:35', '18'),
    ('2023-10-13 09:20:35', '18'),
    ('2023-10-13 09:20:35', '18'),
    ('2023-10-13 09:20:35', '18'),
    ('2023-10-13 09:20:35', '18'),
    ('2023-10-13 09:20:35', '18'),
    ('2023-10-13 09:20:35', '18'),
    ('2023-10-13 09:20:35', '18'),
    ('2023-10-13 09:20:35', '18'),
    ('2023-10-13 09:20:35', '18'),
    ('2023-10-13 09:20:35', '18'),
    ('2023-10-13 09:20:35', '18');
 
CREATE TABLE ovlasti (
	id INT PRIMARY KEY AUTO_INCREMENT,
    ovlast VARCHAR(100)
);
INSERT INTO ovlasti (ovlast) VALUES
	('Administrator'),
    ('Korisnik');

CREATE TABLE korisnik (
	id INT PRIMARY KEY AUTO_INCREMENT,
    ime CHAR(50),
    prezime CHAR(50),
    username VARCHAR(50),
    password BINARY(32),
    id_ovlasti INT,
    FOREIGN KEY (id_ovlasti) REFERENCES ovlasti(id) ON UPDATE CASCADE ON DELETE SET NULL
);
INSERT INTO korisnik(ime, prezime, username, password, id_ovlasti) VALUES
	('Ladislav','Kovač', 'lkovac', UNHEX(SHA2('1234', 256)), '1'),
	('Valentina', 'Ilić', 'vilic', UNHEX(SHA2('abcd', 256)), '1'),
	('Danko','Kovac', 'dkovac', UNHEX(SHA2('ab12', 256)), '2'),
    ('Danko','Kovac', 'dkovac', UNHEX(SHA2('ab12', 256)), '2'),
    ('Danko','Kovac', 'dkovac', UNHEX(SHA2('ab12', 256)), '2'),
    ('Danko','Kovac', 'dkovac', UNHEX(SHA2('ab12', 256)), '2'),
    ('Danko','Kovac', 'dkovac', UNHEX(SHA2('ab12', 256)), '2'),
    ('Danko','Kovac', 'dkovac', UNHEX(SHA2('ab12', 256)), '2'),
    ('Danko','Kovac', 'dkovac', UNHEX(SHA2('ab12', 256)), '2'),
    ('Danko','Kovac', 'dkovac', UNHEX(SHA2('ab12', 256)), '2'),
    ('Danko','Kovac', 'dkovac', UNHEX(SHA2('ab12', 256)), '2'),
    ('Danko','Kovac', 'dkovac', UNHEX(SHA2('ab12', 256)), '2'),
    ('Danko','Kovac', 'dkovac', UNHEX(SHA2('ab12', 256)), '2'),
    ('Danko','Kovac', 'dkovac', UNHEX(SHA2('ab12', 256)), '2'),
    ('Danko','Kovac', 'dkovac', UNHEX(SHA2('ab12', 256)), '2'),
    ('Danko','Kovac', 'dkovac', UNHEX(SHA2('ab12', 256)), '2'),
    ('Danko','Kovac', 'dkovac', UNHEX(SHA2('ab12', 256)), '2'),
    ('Danko','Kovac', 'dkovac', UNHEX(SHA2('ab12', 256)), '2'),
    ('Danko','Kovac', 'dkovac', UNHEX(SHA2('ab12', 256)), '2'),
    ('Danko','Kovac', 'dkovac', UNHEX(SHA2('ab12', 256)), '2'),
	('Katija', 'Kolar', 'kkolar', UNHEX(SHA2('12ab', 256)), '2');
    

DROP USER IF EXISTS app;
CREATE USER app@'%' IDENTIFIED BY '1234';
GRANT SELECT, INSERT, UPDATE, DELETE ON projektdb.* TO app@'%';

    