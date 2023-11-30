import random
from database.db_models import insert_player_sql 


class Player:
    def __init__(self, name, avatar_id):
        self.name = name
        self.airport = None
        self.budget = 500
        self.distance_traveled = 0
        self.avatar_id = avatar_id
        self.co2_consumed = 0


    def set_starting_airport(self):
        starting_airports = {
                "KATL": "Hartsfield-Jackson Atlanta International Airport, USA",
                "ZBAA": "Beijing Capital International Airport, China",
                "EGLL": "London Heathrow Airport, UK",
                "LFPG": "Paris Charles de Gaulle Airport, France",
                "RJTT": "Tokyo Haneda Airport, Japan",
                "CYYZ": "Toronto Pearson International Airport, Canada",
                "OMDB": "Dubai International Airport, UAE",
                "EDDF": "Frankfurt Airport, Germany",
                "RKSI": "Incheon International Airport, South Korea",
                "KLAX": "Los Angeles International Airport, USA",
            }
        
        random_airport = random.choice(list(starting_airports.keys()))
        self.airport = random_airport

    def update_airport(self, airport):
        self.airport = airport

    def insert_player_to_database(self):
            params = (
                        self.name,
                        self.avatar_id,
                        self.budget,
                        self.distance_traveled,
                        self.airport,
                        self.co2_consumed
                    )

            insert_player_sql(params)

    def update_database(self):
        asd = 'asd'
