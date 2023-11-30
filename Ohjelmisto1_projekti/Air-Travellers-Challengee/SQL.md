     
                                    
                _________      .__    ___________      __________              
               /   _____/ _____|  |   \__    ___/___   \______   \__ __  ____  
               \_____  \ / ____/  |     |    | /  _ \   |       _/  |  \/    \ 
               /        < <_|  |  |__   |    |(  <_> )  |    |   \  |  /   |  \
              /_______  /\__   |____/   |____| \____/   |____|_  /____/|___|  /
                      \/    |__|                               \/           \/ 

```markdown
# SQL Database Setup

In this section, we'll provide instructions for setting up the flight_game database and making necessary schema changes. 

## Download the flight_game Database

To get started, download the flight_game database using the following link:
[Download flight_game Database]
https://moodle2.metropolia.fi/pluginfile.php/1561494/mod_resource/content/1/lp.sql

## MySQL Console Commands

After downloading the database, run the following MySQL commands in your console to make the required modifications:

```sql
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
ALTER TABLE game CHANGE COLUMN `screen_name` `name` VARCHAR(255);
ALTER TABLE game ADD budget INT NOT NULL DEFAULT(0);
ALTER TABLE game CHANGE COLUMN `location` `current_airport` VARCHAR(10);
ALTER TABLE game RENAME player;

ALTER TABLE country DROP COLUMN keywords;
ALTER TABLE country DROP COLUMN wikipedia_link;
ALTER TABLE player ADD avatar_id INT NOT NULL DEFAULT(0);

-- Create the 'questions' table
CREATE TABLE questions (
     avatar_id INT DEFAULT(0),
     question_text VARCHAR(500) NOT NULL,
     answer VARCHAR(255) NOT NULL,
     wrong_answer VARCHAR(255) NOT NULL,
     wrong_answer2 VARCHAR(255) NOT NULL
);

ALTER TABLE player ADD distance_traveled INT DEFAULT(0);
ALTER TABLE player ADD points INT DEFAULT(0);

ALTER TABLE player MODIFY COLUMN id INT AUTO_INCREMENT;

-- Clear the 'player' table
DELETE FROM player;

-- Insert sample questions into the 'questions' table
INSERT INTO questions (avatar_id, question_text, wrong_answer2, wrong_answer, answer) VALUES
(1, 'Mikä seuraavista tulostaa Pythonissa?', 'Input().', 'self.print()()', 'print()'),
(1, 'Mikä on luokka (class) Python-ohjelmoinnissa?', 'Se on koiran nimi', 'Se on Pythonin avainsana', 'Luokka on objekti, joka voi sisältää toiminnallisuutta'),
(2, 'Mikä on Pythonin lista (list)?', 'Se on while rakenne ', 'Se on Pythonin versio sanakirjasta', 'Lista on tietorakenne, joka voi sisältää useita alkioita'),
(2, 'Mikä on Pythonin if-lauseen (ehtolauseen) tarkoitus?', 'Se looppaa kysymykset läpi', 'Se lopettaa ohjelman suorituksen', 'If-lause mahdollistaa ehtoisen suorituksen riippuen annetusta ehdosta'),
(2, 'Kuinka Pythonissa käsitellään poikkeuksia (exceptions)?', 'Käyttämällä print komentoa', 'Poikkeuksia ei voi käsitellä Pythonissa', 'Pythonissa poikkeuksia käsitellään try ja except lohkoilla'),
(3, 'Mikä on funktio Python-ohjelmoinnissa?', 'Se on luokka', 'Se on tietorakenne', 'Funktio on nimetty lohko koodia, joka suorittaa tietyn tehtävän'),
(3, 'Mitä tarkoittaa "for"-silmukka Pythonissa?', 'Se on lista', 'Se lopettaa ohjelman suorituksen', '"for"-silmukka toistaa koodilohkoa useita kertoja annetun ehdon perusteella'),
(3, 'Mikä on Pythonin sanakirja (dictionary)?', 'Se on kirjastobussi', 'Se on lista', 'Sanakirja on tietorakenne, joka sisältää avain-arvo -pareja'),
(1, 'Mikä on Quicksort-algoritmi?', 'Hidas lajittelualgoritmi', 'Nopea internet-yhteys', 'Tehokas lajittelualgoritmi'),
(1, 'Mitä tarkoittaa HTML?', 'Helsingin Tietomatka Läksyt', 'High Tech Machine Learning', 'HTML on lyhenne sanoista HyperText Markup Language'),
(1, 'Mikä on CSS?', 'Se on tyypillinen backend kieli', 'Computer Style System', 'CSS on lyhenne sanoista Cascading Style Sheets'),
(1, 'Mikä on JavaScript?', 'Urheiluvälinemerkki', 'Käyttöjärjestelmä', 'JavaScript on ohjelmointikieli, joka mahdollistaa vuorovaikutuksen verkkosivujen kanssa'),
(1, 'Mikä on tietokanta?', 'Pilvipalvelu', 'Matemaattinen kaava', 'Tietokanta on järjestelmä tietojen tallentamiseen, hallintaan ja haettavaksi tekemiseen'),
(2, 'Mikä on MapReduce?', 'Kartta ja kompassi', 'Ohjelmointiparadigma', 'Funktionaalinen ohjelmointikieli'),
(2, 'Mikä on P vs NP -ongelma?', 'Pieni vs. normaali', 'Algoritmin suoritusaika vs. ei-polynominen aika', 'Matemaattinen pähkinä'),
(2, 'Mikä on Turingin kone?', 'Monimutkainen laite', 'Teoreettinen laskentamalli', 'Nopea tietokone'),
(2, 'Mikä on Chomskyn hierarkia?', 'Lingvistinen teoria', 'Tietorakenteiden luokitus', 'Ohjelmointikielen syntaksi'),
(2, 'Mikä on Shannonin entropia?', 'Kosminen voima', 'Tiedon epävarmuusmittari', 'Kvanttifysiikan laki'),
(2, 'Mikä on Hilbertin ongelma?', 'Matemaattinen arvoitus', 'Tiedon tallennusmenetelmä', 'Avaruuden geometria'),
(2, 'Mikä on Riemannin hypoteesi?', 'Fysiikan sääntö', 'Matemaattinen arvaus', 'Matemaattinen lause'),
(2, 'Mikä on Ackermannin funktio?', 'Matemaattinen laskentamalli', 'Ohjelmointikielen funktio', 'Nopeasti kasvava matemaattinen funktio'),
(3, 'Mikä on Byzantine Fault Tolerance?', 'Kaupunki Bysantissa', 'Virhkeenkestävyysjärjestelmä', 'Historiallinen tapahtuma'),
(3, 'Mikä on Gödelin epätäydellisyyslause?', 'Logiikan periaate', 'Matemaattinen paradoksi', 'Matemaattinen lause'),
(3, 'Mikä on Fermat\'n suuri lause?', 'Fysiikan sääntö', 'Matemaattinen arvoitus', 'Matemaattinen lause'),
(3, 'Mikä on Turingin kone?', 'Monimutkainen laite', 'Teoreettinen laskentamalli', 'Nopea tietokone'),
(3, 'Mikä on Kolmogorovin monimutkaisuus?', 'Luonnon ilmiö', 'Algoritmin monimutkaisuusmittari', 'Matemaattinen käsite'),
(3, 'Mikä on MapReduce?', 'Kartta ja kompassi', 'Ohjelmointiparadigma', 'Funktionaalinen ohjelmointikieli'),
(3, 'Mikä on P vs NP -ongelma?', 'Pieni vs. normaali', 'Algoritmin suoritusaika vs. ei-polynominen aika', 'Matemaattinen pähkinä'),
(3, 'Mikä on Turingin kone?', 'Monimutkainen laite', 'Teoreettinen laskentamalli', 'Nopea tietokone'),
(3, 'Mikä on Chomskyn hierarkia?', 'Lingvistinen teoria', 'Tietorakenteiden luokitus', 'Ohjelmointikielen syntaksi'),
(3, 'Mikä on Shannonin entropia?', 'Kosminen voima', 'Tiedon epävarmuusmittari', 'Kvanttifysiikan laki'),
(1, 'Mikä on Yhdysvaltojen pääkaupunki?', 'New York', 'Los Angeles', 'Washington D.C.'),
(1, 'Missä sijaitsee Yhdysvaltojen korkein vuori?', 'Rocky Mountains', 'Appalakit', 'Alaska'),
(1, 'Mikä on Yhdysvaltojen virallinen kieli?', 'Espanja', 'Ranska', 'Englanti'),
(1, 'Mikä on Yhdysvaltojen kansallinen juhlapäivä?', 'Kiitospäivä', 'Memorial Day', 'Itsenäisyyspäivä'),
(1, 'Mikä on Yhdysvaltojen kansallisurheilu?', 'Jalkapallo', 'Koripallo', 'Baseball'),
(2, 'Mikä on Ranskan pääkaupunki?', 'Madrid', 'Rooma', 'Pariisi'),
(2, 'Mikä on Ranskan korkein vuori?', 'Pyreneet', 'Alpit', 'Mont Blanc'),
(2, 'Mikä on Ranskan virallinen kieli?', 'Espanja', 'Italia', 'Ranska'),
(2, 'Mikä on Ranskan kansallinen juhlapäivä?', 'Ranskan vallankumouspäivä', 'Armistice Day', 'Bastiljin päivä'),
(2, 'Mikä on Ranskan tunnetuin ruokalaji?', 'Paella', 'Pizza', 'Ranskalainen sipulikeitto'),
(3, 'Mikä on Espanjan pääkaupunki?', 'Barcelona', 'Valencia', 'Madrid'),
(3, 'Missä sijaitsee Espanjan korkein vuori?', 'Pyreneet', 'Sierra Nevada', 'Alpit'),
(3, 'Mikä on Espanjan virallinen kieli?', 'Katalaani', 'Baski', 'Espanja'),
(3, 'Mikä on Espanjan kansallinen juhlapäivä?', 'San Juanin päivä', 'Pyhän Jaakobin päivä', 'Espanjan kansallispäivä'),
(3, 'Mikä on Espanjan perinteinen tanssi?', 'Sardana', 'Sevillanas', 'Flamenco'),
(1, 'Kuinka paljon on Yhdysvaltojen asukasluku?', '310milj.', '270milj.', '332milj.');








## Database Schema Diagram

Below is a database schema diagram for reference:

![Database Schema](https://raw.githubusercontent.com/Konsta00/Air-Travellers-Challenge/main/images/ER_V2.png)

