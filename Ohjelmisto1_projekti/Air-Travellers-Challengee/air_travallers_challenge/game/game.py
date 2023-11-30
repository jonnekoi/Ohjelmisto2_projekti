import random
# from player import Player 
from database.db_models import get_closest_airports
from database.db_models import calculate_co2_used
from geopy.distance import geodesic
from colors import *

class Game:
    def __init__(self):
        self.game_over = False
        self.closest_airports = None
        self.player = None
        self.current_airport = None
        self.old_airport = None

# SET GAME INSTANCE PLAYER
    def set_player(self, player):
        self.player = player

# SET GAME CURRENT AIRPORT TO PLAYER AIRPORT (CURRENT)
    def set_current_airport(self):
        self.current_airport = self.player.airport

# SET 10 CLOSEST AIRPORT TO GAME FROM DATABASE
    def load_closest_airports(self):
        self.closest_airports = get_closest_airports(self.current_airport)

    def print_available_airports(self):
        # SET THE COORDINATES OF THE CLOSEST AIRPORT
        lat = self.closest_airports[0]['latitude_deg']
        lon = self.closest_airports[0]['longitude_deg']
        coords = lat, lon
    
        print(f'{color_yellow}\nSELECT FROM THE AIRPORTS TO WHICH YOU WANT TO TRAVEL TO:\n{color_end}')
        print('')
        for i, airport in enumerate(self.closest_airports, start=0):
            # SET THE COORDINATES OF THE OTHER AIRPORTS
            lat = airport['latitude_deg'] 
            lon = airport['longitude_deg']
            coords2 = lat, lon
            distance = geodesic(coords, coords2).kilometers
            print(f'{color_yellow}{"CURRENT AIRPORT:" if i == 0 else f"{color_end}{i}."} {airport["name"]} | {airport["ident"]} | {distance:.0f}KM to airport')
            print('─────────────────────────────────────────────────────────────────────')

# PRINT AVATARS ON SCREEN 
    def display_avatars(self):
        avatars = ('Donald Trump', 'Mona Lisa', 'Felipe VI')
        print('')
        for index, avatar in enumerate(avatars, start=1):
            print(f'                {index}. {avatar}')

# UPDATE GAME WITH NEW VALUES
    def update_game(self):
        old = self.old_airport
        new = self.current_airport
        # CALCULATE AND UPDATE PLAYER CO2 CONSUMED
        co2_used, distance = calculate_co2_used(old, new)
        self.player.co2_consumed += co2_used
        self.player.distance_traveled += distance

# CHANGE GAME INSTANCE & PLAYER INSTANCE AIRPORT TO NEW AIRPORT BASED ON PLAYER INPUT TODO: UNUSED
    def travel_to_new_airport(self, input_airport):
        for i, airport in enumerate(self.closest_airports):
            if i == input_airport:
                self.old_airport = self.current_airport
                self.current_airport = airport['ident']
                self.player.airport = airport['ident']
                self.load_closest_airports()

    def display_options(self):
        print(f'''
                ───────────────────────────────────────────
                [PLAYER {color_red}{self.player.name.upper()}{color_end}]\n
                Points: {color_yellow}{self.player.points}{color_end}
                Budged: {color_yellow}{self.player.budget}${color_end}
                Emissions: {color_yellow}{self.player.co2_consumed:.2f} KG/C02{color_end}
                Distance traveled: {color_yellow}{self.player.distance_traveled:.2f}KM{color_end}
                Current airport: {color_yellow}{self.player.airport}{color_end}
                Total questions answered correctly: {color_yellow}{self.player.total_questions_answered}{color_end}
                ────────────────────────────────────────────
            ''')
        if self.player.current_answered <= 2:
            print(f'''
                {color_yellow}WHAT DO YOU WANT TO DO:{color_end}
                1. ANSWER ANOTHER QUESTION
                2. TRAVEL TO NEW AIRPORT
                3. SHOW AVAILABLE POWER UPS
                4. VISIT THE STORE
                ''')
        else: 
            print(f'''
                {color_yellow}WHAT DO YOU WANT TO DO:{color_end}
                1. TRAVEL TO NEW AIRPORT
                2. SHOW AVAILABLE POWER UPS
                3. VISIT THE STORE

                ''')
            
    def travel(self):
        try:
            input_airport = int(input(f'{color_yellow}SELECT AIRPORT BY TYPING 1-{len(self.closest_airports)-1}:{color_end} '))
            if 1 <= input_airport <= len(self.closest_airports) - 1:
                print(f'''
                        {color_bright_cyan}
                Travelled to {self.closest_airports[input_airport]["name"]}
                        {color_end}''')
                self.travel_to_new_airport(input_airport)
                
                self.player.current_answered = 0
            else: 
                print(f'''{color_bright_red}
                Invalid airport selection.'
                            {color_end}''')
        except ValueError:
            print(f'{color_bright_red}Invalid input. Please enter a valid airport number.{color_end}')




