     
                                    
                _________      .__    ___________      __________              
               /   _____/ _____|  |   \__    ___/___   \______   \__ __  ____  
               \_____  \ / ____/  |     |    | /  _ \   |       _/  |  \/    \ 
               /        < <_|  |  |__   |    |(  <_> )  |    |   \  |  /   |  \
              /_______  /\__   |____/   |____| \____/   |____|_  /____/|___|  /
                      \/    |__|                               \/           \/ 

Lataa flight_game tietokanta: 
https://moodle2.metropolia.fi/pluginfile.php/1561494/mod_resource/content/1/lp.sql

SEN JÄLKEEN JUOKSE MYSQL-KONSOLISSA:


DROP TABLE IF EXISTS goal_reached;
DROP TABLE IF EXISTS goal;

ALTER TABLE airport DROP COLUMN elevation_ft;
ALTER TABLE airport DROP COLUMN iso_region;
ALTER TABLE airport DROP COLUMN municipality;
ALTER TABLE airport DROP COLUMN scheduled_service;
ALTER TABLE airport DROP COLUMN gps_code;
ALTER TABLE airport DROP COLUMN iata_code;
ALTER TABLE airport DROP COLUMN local_code;
ALTER TABLE airport DROP COLUMN home_link;
ALTER TABLE airport DROP COLUMN keywords;
ALTER TABLE airport DROP COLUMN wikipedia_link;

ALTER TABLE game DROP COLUMN co2_budget;
ALTER TABLE game CHANGE COLUMN `screen_name` `name` varchar(255);
ALTER TABLE game ADD budget int NOT NULL DEFAULT(0);
ALTER TABLE game CHANGE COLUMN `location` `current_airport` varchar(10);
ALTER TABLE game RENAME player;

ALTER TABLE country DROP COLUMN keywords;
ALTER TABLE country DROP COLUMN wikipedia_link;
ALTER TABLE player ADD avatar_id int NOT NULL DEFAULT(0);

CREATE TABLE questions (
     avatar_id INT DEFAULT(0),
     question_text VARCHAR(500) NOT NULL,
     clue1 VARCHAR(255),
     clue2 VARCHAR(255),
     answer VARCHAR(255) NOT NULL,
     wrong_answer VARCHAR(255) NOT NULL
);

ALTER TABLE player ADD distance_traveled INT DEFAULT(0);
ALTER TABLE player ADD points INT DEFAULT(0);

ALTER TABLE player MODIFY COLUMN id INT AUTO_INCREMENT;


DELETE FROM player;


INSERT INTO questions (avatar_id, question_text, clue1, clue2, answer, wrong_answer) VALUES
(1, 'Mikä on Pythonin peruslauseke?', 'Se on yksinkertainen ohje', 'Se suorittaa tietyn tehtävän', 'Peruslauseke Pythonissa on "print()"', 'Se on banaani'),
(1, 'Mikä on luokka (class) Python-ohjelmoinnissa?', 'Se on objekti, joka voi sisältää toiminnallisuutta', 'Se on Pythonin avainsana', 'Luokka on objekti, joka voi sisältää toiminnallisuutta', 'Se on funktio'),
(1, 'Mikä on merkkijonon (string) tärkein ominaisuus Pythonissa?', 'Se voi sisältää tekstiä', 'Se on vain numero', 'Merkkijono voi sisältää tekstiä', 'Se voi sisältää vain yhden merkin');

INSERT INTO questions (avatar_id, question_text, clue1, clue2, answer, wrong_answer) VALUES
(2, 'Miten Pythonissa tulostetaan teksti näytölle?', 'Käyttämällä "print()" -funktiota', 'Käyttämällä "input()" -funktiota', 'Pythonissa teksti tulostetaan näytölle käyttämällä "print()" -funktiota', 'Käyttämällä "scan()" -funktiota'),
(2, 'Mikä on Pythonin lista (list)?', 'Se on tietorakenne, joka voi sisältää useita alkioita', 'Se on Pythonin versio sanakirjasta', 'Lista on tietorakenne, joka voi sisältää useita alkioita', 'Se on luku'),
(2, 'Mikä on Pythonin if-lauseen (ehtolauseen) tarkoitus?', 'Se mahdollistaa ehtoisen suorituksen', 'Se lopettaa ohjelman suorituksen', 'If-lause mahdollistaa ehtoisen suorituksen riippuen annetusta ehdosta', 'Se tulostaa aina "Hello, World!"');

INSERT INTO questions (avatar_id, question_text, clue1, clue2, answer, wrong_answer) VALUES
(3, 'Mikä on funktio Python-ohjelmoinnissa?', 'Se on nimetty lohko koodia', 'Se on tietorakenne', 'Funktio on nimetty lohko koodia, joka suorittaa tietyn tehtävän', 'Se on luku'),
(3, 'Mitä tarkoittaa "for"-silmukka Pythonissa?', 'Se toistaa koodilohkoa useita kertoja', 'Se lopettaa ohjelman suorituksen', '"for"-silmukka toistaa koodilohkoa useita kertoja annetun ehdon perusteella', 'Se tulostaa aina "Hello, World!"');

INSERT INTO questions (avatar_id, question_text, clue1, clue2, answer, wrong_answer) VALUES
(4, 'Mikä on Pythonin sanakirja (dictionary)?', 'Se on tietorakenne, joka sisältää avain-arvo -pareja', 'Se on lista', 'Sanakirja on tietorakenne, joka sisältää avain-arvo -pareja', 'Se on funktio'),
(4, 'Mikä on Pythonin moduuli?', 'Se on Pythonin kirjasto', 'Se on tietoturvaominaisuus', 'Moduuli on Pythonin tiettyjen toimintojen tai ominaisuuksien kokoelma', 'Se on luku');

INSERT INTO questions (avatar_id, question_text, clue1, clue2, answer, wrong_answer) VALUES
(5, 'Kuinka Pythonissa käsitellään poikkeuksia (exceptions)?', 'Käyttämällä try ja except lohkoja', 'Poikkeuksia ei voi käsitellä Pythonissa', 'Pythonissa poikkeuksia käsitellään try ja except lohkoilla', 'Käyttämällä if-lauseita'),
(5, 'Mikä on Pythonin while-silmukka?', 'Se on toistorakenne, joka toistaa koodilohkoa niin kauan kuin ehto on tosi', 'Se on Pythonin funktio', 'While-silmukka on toistorakenne, joka toistaa koodilohkoa niin kauan kuin ehto on tosi', 'Se on lista');
                                                                                                                              
![alt text](https://github.com/Konsta00/Air-Travellers-Challenge/blob/main/ER.png)  
