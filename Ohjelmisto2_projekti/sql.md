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
INSERT INTO questions (question_text, wrong_answer2, wrong_answer, answer)
VALUES
('Kuinka suuri osuus maailman hiilidioksidipäästöistä on peräisin lentoliikenteestä?', '20-25%', '25-30%', '2-3%'),
('Mikä on suurin yksittäinen tekijä ilmakehän kasvihuonekaasupitoisuuden kasvussa?', 'Autoilu', 'Teollisuus', 'Fossiiliset polttoaineet'),
('Mikä matkustustapa tuottaa vähiten hiilidioksidipäästöjä?', 'Lentäminen', 'Autoilu', 'Junamatkailu'),
('Kuinka paljon vähemmän hiilidioksidipäästöjä syntyy lentokoneessa istuessasi turistiluokassa verrattuna bisnesluokkaan?', 'Ei eroa', '5 kertaa ', '2-3 kertaa'),
('Kuinka paljon hiilidioksidipäästöjä syntyy yhden henkilöauton valmistamisesta?', 'yli 30 tonnia', '10-30 tonnia', '5-20 tonnia'),
('Mikä on lentokoneiden suurin ympäristövaikutus?', 'Melusaaste', 'Ilmakehän reaktiot', 'Hiilidioksidipäästöt'),
('Kuinka paljon hiilidioksidipäästöjä syntyy per matkustajakilometri pitkällä lennolla?', '50-75 grammaa', '150-200 grammaa', '75–150 grammaa'),
('Kuinka paljon hiilidioksidipäästöjä syntyy per matkustajakilometri lyhyellä lennolla?', '30-90 grammaa', '125-300 grammaa', '90–250 grammaa'),
('Mikä on suurin osuus lentoliikenteen päästöistä?', 'Matkatavaroiden kuljettaminen', 'Lentokoneiden valmistus', 'Lentokoneiden käyttö'),
('Kuinka paljon hiilidioksidipäästöjä syntyy pienen lyhyen matkan lentokoneen yhden lentotunnin aikana?', '4-8 tonnia', '1-2 tonnia', '2-4 tonnia'),
('Kuinka paljon hiilidioksidipäästöjä syntyy suuren pitkän matkan lentokoneen yhden lentotunnin aikana?', '15-25 tonnia', '5-10 tonnia', '10-15 tonnia'),
('Kuinka paljon hiilidioksidipäästöjä syntyy yhden henkilöauton ajamisesta 100 kilometriä?', '15kg', '25kg', 'n. 20kg'),
('Mikä lentokoneiden polttoaineista aiheuttaa suurimmat kasvihuonekaasupäästöt?', 'Biopolttoaineet', 'Vety', 'Kerosiini'),
('Kuinka paljon päästöjä voidaan vähentää lentämällä suoraa reittiä?', 'Ei vaikutusta', '10%', '25%'),
('Mikä on lentomatkustuksen osuus yksittäisen henkilön hiilijalanjäljestä vuodessa?', '2%', '5%', '10-20%'),
('Mikä on suurin syy lentoliikenteen kasvaviin päästöihin?', 'Kerosiinin hinnan nousu', 'Lentokoneiden kasvava koko', 'Lentoliikenteen kasvu');

INSERT INTO questions(question_text, answer, wrong_answer, wrong_answer2)
VALUES
    ("Kuinka monta prosenttia maailman lentoliikenteen päästöistä on peräisin rahtikuljetuksista?", "30%", "50%", "10%"),

    ("Minkä lentokoneen polttoainejärjestelmä on kaikkein ympäristöystävällisin?", "Airbus A320neo", "Boeing 747", "Airbus A380"),

    ("Mikä on tyypillisen transatlanttisen lennon hiilidioksidipäästö per matkustaja?", "1 tonni", "500 kg", "1,5 tonnia"),

    ("Mikä on suurin haaste biopolttoaineiden käyttöönotossa lentoliikenteessä?", "Kustannukset", "Saatavuus", "Tehokkuus"),

    ("Kuinka monta kilogrammaa hiilidioksidia syntyy keskimäärin yhdellä lentokoneen istumapaikalla kilometriä kohti?", "90 grammaa", "150 grammaa", "50 grammaa"),

    ("Mikä maailman suurkaupungeista on ensimmäisenä julistanut tavoitteekseen hiilineutraalin lentoliikenteen?", "Oslo", "New York", "Tokio"),

    ("Kuinka paljon hiilidioksidia vapautuu tyypillisesti yhden matkustajan lomamatkasta Euroopasta Aasiaan?", "3 tonnia", "2 tonnia", "4 tonnia"),

    ("Mikä on suurin yksittäinen ilmastonmuutosta kiihdyttävä tekijä lentoliikenteessä?", "Kerosiinin poltto", "Ilmakehän saasteet", "Äänisaaste");

INSERT INTO questions (question_text, answer, wrong_answer, wrong_answer2)
VALUES
    ("Mikä on tyypillisen lentokoneen polttoaineenkulutus litroina tunnissa?", "2500 litraa", "500 litraa", "1000 litraa"),

    ("Mikä on suurin tekijä lentoliikenteen hiilidioksidipäästöjen vähentämisessä?", "Tehokkaammat moottorit", "Lyhyemmät lentoreitit", "Pienemmät lentokoneet"),

    ("Kuinka paljon hiilidioksidipäästöjä yksi puu voi keskimäärin sitoa vuodessa?", "21 kg", "5 kg", "50 kg"),

    ("Minkä maan lentokenttä on ensimmäisenä saavuttanut hiilineutraalin statuksen?", "Hollanti", "Yhdysvallat", "Australia"),

    ("Kuinka suuri osuus lentoliikenteen hiilidioksidipäästöistä on peräisin kansainvälisistä lennoista?", "60%", "30%", "80%"),

    ("Mikä on keskimääräinen hiilidioksidipäästö yhden tunnin kestävältä lentomatkalta?", "90 kg", "250 kg", "150 kg"),

    ("Mikä lentoyhtiö oli ensimmäinen, joka otti käyttöön biopolttoaineita kaupallisilla lennoilla?", "Lufthansa", "Qantas", "British Airways"),

    ("Mikä lentokonevalmistaja on kehittänyt polttoainetehokkaimman lentokonemallin?", "Airbus", "Boeing", "Bombardier");

INSERT INTO questions(question_text, answer, wrong_answer, wrong_answer2)
VALUES
    ("Kuinka monta prosenttia maailman lentokoneista käyttää biopolttoaineita vuonna 2023?", "5%", "20%", "1%"),

    ("Mikä maa tuotti eniten hiilidioksidipäästöjä lentoliikenteestä vuonna 2022?", "Yhdysvallat", "Kiina", "Intia"),

    ("Kuinka paljon hiilidioksidia keskimäärin vapautuu yhden henkilön yhdeltä Atlantin ylittävältä lennolta?", "1,6 tonnia", "3 tonnia", "500 kg"),

    ("Mikä on maailman energiatehokkain kaupallinen lentokonemalli?", "Boeing 787 Dreamliner", "Airbus A380", "Boeing 747"),

    ("Mikä teknologia vähentää tehokkaimmin lentokoneiden hiilijalanjälkeä?", "Sähköinen voimansiirto", "Hybridimoottorit", "Vetykäyttöiset moottorit"),

    ("Kuinka paljon globaaleista hiilidioksidipäästöistä on peräisin kansainvälisestä lentoliikenteestä?", "2%", "10%", "5%"),

    ("Mikä on keskimääräinen hiilidioksidipäästö yhdeltä Euroopan sisäiseltä lennolta per matkustaja?", "90 kg", "200 kg", "50 kg"),

    ("Minkä maan lentoyhtiöt ovat vähentäneet eniten päästöjään viimeisen viiden vuoden aikana?", "Ruotsi", "Yhdysvallat", "Saksa");