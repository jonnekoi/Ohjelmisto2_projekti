import random
import json
from database.db_models import insert_player_sql 
from database.db_models import get_airports_iso_sql
from database.db_models import update_points
from colors import *

class Player:
    def __init__(self, name, avatar_id):
        self.id = None
        self.name = name
        self.airport = None
        self.budget = 100
        self.distance_traveled = 0
        self.avatar_id = avatar_id
        self.co2_consumed = 0
        self.points = 0
        self.powerups = []
        self.total_questions_answered = 0
        self.current_answered = 0

    def print_player(self):
        print('ID: ', self.id)
        print('Name: ', self.name)
        print('Points: ', self.points)
        print('Budget: ', self.budget)
        print('Airport: ', self.airport)
        print('Co2 consumed: ', self.co2_consumed)
        print('Avatar ID: ', self.avatar_id)

# GET ALL AIRPORTS FROM SELECTED AVATAR AND SET STARTING AIRPORT FOR PLAYER 
    def set_starting_airport(self, avatar_id):
        iso = ''

        if avatar_id == 1:
            # avatar_id = 1 = Donald Trump
            iso = 'US'
        elif avatar_id == 2:
            # avatar_id = 2 = Mona Lisa
            iso = 'FR'
        elif avatar_id == 3:
            # avatar_id = 3 = Felipe IV
            iso = 'ES'

# AIRPORTS DICTIONARY
        airports_dict = {}
        airports = get_airports_iso_sql(iso)

        for airport in airports:
            airports_dict[f'{airport["ident"]}'] = f'{airport["name"]}'

        starting_airport = random.choice(list(airports_dict.keys()))
        self.airport = starting_airport
        

# UPDATE PLAYERS AIRPORT TO CURRENT AIRPORT[ GETS PASSED IN AS A PARAMETER ]
    def update_airport(self, airport):
        self.airport = airport

# INSERT PLAYER INTO DATABASE
    def insert_player_to_database(self):
            params = (
                        self.name,
                        self.avatar_id,
                        self.budget,
                        self.distance_traveled,
                        self.airport,
                        self.co2_consumed
                    )
            try:
                self.id =  insert_player_sql(params)
                print(self.id)
            except Exception as error:
                print('Error inserting player to database: {error}')

# TODO: UPDATE PLAYER INFO TO DABASE ALMOST EVERYTIME SOMETHING GETS CHANGED
    def check_values(self, game):
        if self.budget < 0:
            self.budget = 0
        if self.points < 0:
            self.points = 0
        if self.points >= 1000:
            game.game_over = True

    def update_budget(self, amount):
        if bool(amount):
            self.budget += amount
        elif not bool(amount):
            self.budget -= amount

# DONE: UPDATE PLAYER POINTS
    def update_points(self, points_to_add):
        if bool(points_to_add):
            self.points += points_to_add
        elif not bool(points_to_add):
            self.points -= points_to_add
            if self.points < 0: self.points = 0

# DONE: UPDATE CO2 REDUCTION
    def update_co2_emissions(self, co2_reduction):
        self.co2_consumed -= co2_reduction
        print(f"                CO2 emission reduced by {color_yellow}{co2_reduction}kg{color_end}\n"
              f"                Current CO2 emission: {color_yellow}{self.co2_consumed:.2f}kg{color_end}")

    def update_distance(self, distance_to_add):
        if bool(distance_to_add):
            self.distance += distance_to_add
        else:
            self.distance -= distance_to_add

# TODO: SELECT RANDOM POWERUP AND AND IT TO PLAYER INSTANCE DICTIONARY
    def random_powerup(self):
        power_ups = ('skip_question', 'random_reward')
        random_choice = random.choice(list(power_ups))
        self.powerups += (random_choice,)

    def use_powerup(self, powerup):
        if powerup == 'random_reward':
            random_num = random.randint(0, 15)
            if random_num < 2:
                self.budget += 200
                return self.budget
            elif random_num >2 and random_num < 6:
                self.budget += 150
                return self.budget
            else:
                self.budget += 100
                return self.budget
        elif powerup == 'skip_question':
            self.update_questions()
            self.skip_question1(powerup)
            return 2

    def skip_question1(self, powerup):
        self.powerups.remove(powerup)
        print(f'''
                {color_bright_green}QUESTION SKIPPED (1 answering chance used before flying){color_end}''')


    def use_question_powerup(self):
        print('')
        print(f"{color_bright_yellow}                Available powerups to use: {color_end}")
        print('')
        skip_powerups = ()
        index = 0
        for i, powerup_ in enumerate(self.powerups, start=1):
            if powerup_ == 'skip_question':
                print(f'                {i}. Skip question')
                skip_powerups += (powerup_, )
                index += 1
        try:
            input_powerup = int(input(f'''
                Select the powerup you want to use by typing the corresponding number: '''))

            for i, powerup in enumerate(skip_powerups, start=1):
                if i == input_powerup:
                    return self.use_powerup(powerup)
        except ValueError:
            print('')
            print(f"{color_red}                Invalid Input.{color_end} ")

    def update_questions(self):
        self.total_questions_answered += 1
        self.current_answered += 1

    def buy_random_reward(self):
        if self.budget > 160:
            self.budget -= 160
            b = self.budget
            new_b = self.use_powerup('random_reward')
            reward = new_b - b
            print(f'''
                {self.name} used {color_bright_red}160${color_end} 
                Balance remaining {color_bright_green}{self.budget}${color_end}
                You have received {color_bright_green}{reward}${color_end}
                ''')

    def buy_skip_question(self):
        if self.budget > 100: 
            self.budget -= 100
            self.powerups += ('skip_question',)
            print(f'''
                Purchased {color_blue}SKIP QUESTION{color_end} successfully!
                You have spent {color_bright_red}100${color_end}
                Balance remaining {color_bright_green}{self.budget}${color_end}
                ''')
        
    def buy_random_powerup(self):
        if self.budget > 130: 
            self.budget -= 130
            self.random_powerup()
            
            print(f'''
                You have spent {color_bright_red}130${color_end}
                Balance remaining {color_bright_green}{self.budget}${color_end}''')
            last_inserted_power_up = self.powerups[-1]
            b = self.budget
            reward = None
            if last_inserted_power_up == 'random_reward':
                new_b = self.use_powerup('random_reward')
                reward = new_b - b
                print(f'                You received {color_bright_green}{reward}${color_end}')
                print(f'                Total balance:{color_bright_green}{self.budget}{color_end}')
            else:
                print(f'                You received {color_bright_green}skip question power-up{color_end}')
                self.powerups = ('skip_question',)

    def display_powerups(self):
        print(f'''
            {color_yellow}  [AVAILABLE POWER UPS]{color_end}''')
        for i, p in enumerate(self.powerups, start=1):
            if p == 'skip_question':
                print(f'                {i}. Skip question')
            elif p == 'random_reward':
                print(f'                {i}. Random reward')
            else:
                print(f'                {i}. Random powerup')

