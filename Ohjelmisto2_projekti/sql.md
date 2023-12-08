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

ALTER TABLE country DROP COLUMN keywords;
ALTER TABLE country DROP COLUMN wikipedia_link;

ALTER TABLE game RENAME player;
CREATE TABLE player (
    co2_consumed INT(8),
    current_airport VARCHAR(10),
    name VARCHAR(255),
    distance_traveled INT(11),
    id INT(11) NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (id)
);


CREATE TABLE scoreboard (
     player VARCHAR (200) NOT NULL,
     co2_emissions int NOT NULL,
     distance int not null
);

-- Create the 'questions' table
CREATE TABLE questions (
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

-- Clear the 'questions' table

DELETE FROM questions;

-- Insert sample questions into the 'questions' table
INSERT INTO questions (question_text, wrong_answer2, wrong_answer, answer) VALUES
('Kuinka suuri osuus maailman hiilidioksidipäästöistä on peräisin lentoliikenteestä?', '20%', '30%', '2%'),
('Mikä on suurin yksittäinen tekijä ilmakehän kasvihuonekaasupitoisuuden kasvussa?', 'Autoilu', 'Teollisuus', 'Fossiiliset polttoaineet'),
('Kuinka paljon hiilidioksidipäästöjä syntyy yhden lentokilometrin aikana?', '50 grammaa', '100 grammaa', '200 grammaa'),
('Mikä on lentomatkustuksen osuus maailmanlaajuisista hiilidioksidipäästöistä?', '5%', '10%', '2%'),
('Mikä matkustustapa tuottaa vähiten hiilidioksidipäästöjä?', 'Lentäminen', 'Autoilu', 'Junamatkailu'),
('Kuinka paljon päästöjä voidaan vähentää lentämällä suoraa reittiä?', 'Ei vaikutusta', '10%', '25%'),
('Mikä on suurin syy lentoliikenteen kasvaviin päästöihin?', 'Vanhat lentokoneet', 'Lentoyhtiöiden kilpailu', 'Liikenteen kasvu'),
('Kuinka paljon hiilidioksidipäästöjä syntyy yhden lentotunnin aikana?', '500 kg', '1 tonni', '2 tonnia'),
('Mikä on lentomatkustuksen osuus yksittäisen henkilön hiilijalanjäljestä vuodessa?', '10%', '20%', '2%'),
('Mikä on suurin syy lentoliikenteen kasvaviin päästöihin?', 'Kerosiinin hinnan nousu', 'Lentokoneiden kasvava koko', 'Liikenteen kasvu'),
('Kuinka paljon hiilidioksidia vapautuu yhden matkustajan lentokoneesta?', '100 kg', '200 kg', '400 kg'),
('Kuinka paljon hiilidioksidipäästöjä syntyy keskimäärin yhden maailmanympärimatkan aikana lentäen?', '2 tonnia', '5 tonnia', '10 tonnia'),
('Mikä lentokoneiden polttoaineista aiheuttaa suurimmat kasvihuonekaasupäästöt?', 'Biopolttoaineet', 'Kerosiini', 'Vety'),
('Kuinka paljon hiilidioksidipäästöjä syntyy yhden lentomatkustajan tyypillisestä liikematkasta?', '500 kg', '1 tonni', '2 tonnia'),
('Mikä on lentokoneiden suurin ympäristövaikutus?', 'Melusaaste', 'Ilmakehän reaktiot', 'Hiilidioksidipäästöt'),
('Kuinka paljon hiilidioksidia vapautuu yhden matkustajan lentomatkan aikana?', '100 kg', '200 kg', '400 kg'),
('Mikä on suurin osuus lentoliikenteen päästöistä?', 'Matkatavaroiden kuljettaminen', 'Lentokoneiden valmistus', 'Lentokoneiden käyttö'),
('Kuinka paljon hiilidioksidipäästöjä syntyy yhden henkilöauton ajamisesta 100 kilometriä?', '10 kg', '20 kg', '30 kg'),
('Mikä on suurin yksittäinen syy lentoliikenteen päästöjen kasvuun?', 'Lentokoneiden määrän lisääntyminen', 'Polttomoottorien kehitys', 'Lentokoneiden keski-ikä'),
('Kuinka paljon vähemmän hiilidioksidipäästöjä syntyy lentokoneessa istuessasi bisnesluokassa verrattuna turistiluokkaan?', 'Ei eroa', '10%', '50%'),
('Mikä on suurin osuus lentoliikenteen päästöistä?', 'Matkustajien hengitys', 'Lentokoneiden valmistus', 'Lentokoneiden käyttö'),
('Kuinka paljon hiilidioksidipäästöjä syntyy yhden pitkän matkan lennon aikana?', '1 tonni', '2 tonnia', '3 tonnia'),
('Mikä on suurin syy lentoliikenteen päästöjen kasvuun?', 'Lentokoneiden käyttöikä', 'Matkustajien määrän kasvu', 'Lentoyhtiöiden fuusiot'),
('Kuinka paljon hiilidioksidipäästöjä syntyy yhden henkilöauton valmistamisesta?', '5 tonnia', '10 tonnia', '15 tonnia'),
('Mikä on lentokoneiden suurin ympäristövaikutus?', 'Ilmakehän reaktiot', 'Hiilidioksidipäästöt', 'Kerosiinin valmistus'),
('Kuinka paljon hiilidioksidipäästöjä syntyy yhden matkustajan keskimääräisestä lentomatkan aikana?', '500 kg', '1 tonni', '2 tonnia'),
('Mikä on lentokoneiden suurin ympäristövaikutus?', 'Melusaaste', 'Ilmakehän reaktiot', 'Hiilidioksidipäästöt'),
('Kuinka paljon hiilidioksidipäästöjä syntyy yhden lentokoneen valmistuksesta?', '100 tonnia', '200 tonnia', '300 tonnia'),
('Mikä on lentomatkustuksen osuus maailmanlaajuisista hiilidioksidipäästöistä?', '10%', '20%', '5%'),
('Kuinka paljon hiilidioksidipäästöjä syntyy yhden matkustajan tyypillisestä lomamatkasta lentäen?', '1 tonni', '2 tonnia', '3 tonnia'),
('Mikä on lentoliikenteen osuus maailman hiilidioksidipäästöistä?', '10%', '15%', '2%'),
('Kuinka paljon hiilidioksidia vapautuu yhden matkustajan lentomatkan aikana?', '100 kg', '200 kg', '400 kg'),
('Mikä on suurin syy lentoliikenteen päästöjen kasvuun?', 'Lentokoneiden käyttöikä', 'Matkustajien määrän kasvu', 'Lentoyhtiöiden fuusiot'),
('Kuinka paljon hiilidioksidipäästöjä syntyy yhden henkilöauton valmistamisesta?', '5 tonnia', '10 tonnia', '15 tonnia'),
('Mikä on lentokoneiden suurin ympäristövaikutus?', 'Ilmakehän reaktiot', 'Hiilidioksidipäästöt', 'Kerosiinin valmistus'),
('Kuinka paljon hiilidioksidipäästöjä syntyy yhden lentokoneen valmistuksesta?', '100 tonnia', '200 tonnia', '300 tonnia'),
('Mikä on suurin osuus lentoliikenteen päästöistä?', 'Matkustajien hengitys', 'Lentokoneiden valmistus', 'Lentokoneiden käyttö'),
('Kuinka paljon hiilidioksidipäästöjä syntyy yhden pitkän matkan lennon aikana?', '1 tonni', '2 tonnia', '3 tonnia'),
('Mikä on lentoliikenteen osuus maailman hiilidioksidipäästöistä?', '10%', '15%', '2%'),
('Kuinka paljon hiilidioksidipäästöjä syntyy yhden matkustajan keskimääräisestä lentomatkan aikana?', '500 kg', '1 tonni', '2 tonnia'),
('Mikä on lentokoneiden suurin ympäristövaikutus?', 'Melusaaste', 'Ilmakehän reaktiot', 'Hiilidioksidipäästöt'),
('Kuinka paljon hiilidioksidia vapautuu yhden matkustajan lentomatkan aikana?', '100 kg', '200 kg', '400 kg'),
('Mikä on suurin osuus lentoliikenteen päästöistä?', 'Matkatavaroiden kuljettaminen', 'Lentokoneiden valmistus', 'Lentokoneiden käyttö'),
('Kuinka paljon hiilidioksidipäästöjä syntyy yhden henkilöauton ajamisesta 100 kilometriä?', '10 kg', '20 kg', '30 kg'),
('Mikä on suurin yksittäinen syy lentoliikenteen päästöjen kasvuun?', 'Lentokoneiden määrän lisääntyminen', 'Polttomoottorien kehitys', 'Lentokoneiden keski-ikä'),
('Kuinka paljon hiilidioksidipäästöjä syntyy keskimäärin yhden maailmanympärimatkan aikana lentäen?', '2 tonnia', '5 tonnia', '10 tonnia'),
('Mikä lentokoneiden polttoaineista aiheuttaa suurimmat kasvihuonekaasupäästöt?', 'Biopolttoaineet', 'Kerosiini', 'Vety'),
('Kuinka paljon päästöjä voidaan vähentää lentämällä suoraa reittiä?', 'Ei vaikutusta', '10%', '25%'),
('Mikä on lentomatkustuksen osuus yksittäisen henkilön hiilijalanjäljestä vuodessa?', '10%', '20%', '2%'),
('Kuinka suuri osuus maailman hiilidioksidipäästöistä on peräisin lentoliikenteestä?', '20%', '30%', '2%');

