import random
# from player import Player 
from database.db_models import get_closest_airports

class Game:
    def __init__(self):
        self.closest_airports = None
        self.player = None
        self.current_airport = None

    def set_player(self, player):
        self.player = player

    def set_current_airport(self):
        self.current_airport = self.player.airport

    def set_closest_airports(self):
        self.closest_airports = get_closest_airports(self.current_airport)

    def print_avatars(self):
        avatars = ('Donald J. Trump', 'Hillary Clinton', 'Sanna Marin')

        index = 1
        print(f'Select avatar from {index}-{len(avatars)}: ')
        for index, avatar in enumerate(avatars):
            print(f'{index+1}. {avatar}')

