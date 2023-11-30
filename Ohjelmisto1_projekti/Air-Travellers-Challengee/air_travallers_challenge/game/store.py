from colors import *

class Store:
    def __init__(self):
        self.items = {
            'power_ups': {
                'skip_question': ('Skip a question when playing', 100),
                'random_reward': ('Get a random reward', 160),
                'random_powerup': ('Get a random power-up', 130),
            },
            'plant_trees': {
                'plant_10_trees': ('Plant 10 trees', 30),
                'plant_20_trees': ('Plant 20 trees', 50),
                'plant_30_trees': ('Plant 30 trees', 65),
            }
        }
        self.player_inventory = {}

    def display_store_options(self):
        print('''
                    ╔══════════════════════════╗ 
                        Welcome to the store!
                    ╚══════════════════════════╝''')
        for category, items in self.items.items():
            print(f"{color_yellow}\n{'                1. Power ups: ' if category == 'power_ups' else '                2. Plant trees:'}{color_end}")
            for item  in items.items():
                print(f'                {item[1][0]}: {item[1][1]}$')

    def purchase_item(self, player, category, input_number):
        if category in self.items:
            try:
                item_choice = input_number
                item = list(self.items[category].keys())[item_choice - 1]


                # TODO: FIX POWER_UPS = HANDLING PURCHASING AND USING THEM 
                if category == 'power_ups':
                    # print("Choose an item:")
                    # for i, (item) in enumerate(self.items[category].items(), start=1):
                    #     print(f"{i}.{item[1][0]}: {item[1][1] }$")
                    
                    self.purchase_power_up(player)
                elif category == 'plant_trees':
                    self.purchase_plant_trees(player)
                
            except (ValueError, IndexError):
                print("Invalid input. Please enter a valid selection.")
        else:
            print("-------------[Invalid category choice.]-------------")


    def purchase_plant_trees(self, player):
        print('''
                    ╔══════════════════════════╗ 
                        STORE --> PLANT TREES
                    ╚══════════════════════════╝
              ''')
        print(f"{color_yellow}                Choose a tree planting option:{color_end}")
        print('')
        for i, item in enumerate(self.items['plant_trees'].items(), start=1):
            print(f"                {i}. {item[1][0]}: {item[1][1]}$")

        try:
            item_choice = int(input("\n               Enter the number of your choice: "))
            print('')
            item = list(self.items['plant_trees'].keys())[item_choice - 1]
            # Calculate CO2 reduction based on the chosen option
            if item == 'plant_10_trees':
                co2_reduction = 1.5
            elif item == 'plant_20_trees':
                co2_reduction = 3.5
            elif item == 'plant_30_trees':
                co2_reduction = 6.5
            else:
                print("                Invalid item choice.")
                return

            # Deduct the price from the player's budget
            price = self.items['plant_trees'][item][1]
            if player.budget >= price:
                player.budget -= price
                print(f"                You have spent {color_red}{price}${color_end}")
                # Apply CO2 reduction
                player.update_co2_emissions(co2_reduction)


            else:
                print(f"{color_red}Insufficient funds. Cannot purchase the item.{color_end}")
        except (ValueError, IndexError):
            print(f"{color_red}Invalid input. Please enter a valid selection.{color_end}")

    def purchase_power_up(self, player):
        print('''
                    ╔══════════════════════════╗ 
                         STORE --> POWER-UPS
                    ╚══════════════════════════╝
              ''')
        print(f'''
                {color_yellow}Choose a power-up:{color_end}''')
                    
        for i, item in enumerate(self.items['power_ups'].items(), start=1):
           print(f''' 
                {i}. {item[1][0]}: {item[1][1]}$''')

        try:
            item_choice = int(input("\n                Enter the number of your choice: "))
            item = list(self.items['power_ups'].keys())[item_choice - 1]

            if item == 'skip_question':
                player.buy_skip_question()
            elif item == 'random_reward':
                player.buy_random_reward()
            elif item == 'random_powerup':
                player.buy_random_powerup()
            else:
                print("Invalid item choice.")
                return   
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid selection.")


    def buy(self, player):
        category_choice = int(input(f'''{color_yellow}
                Choose a category 1-2: {color_end}'''))
        try:
            if category_choice in [1, 2]:
                if category_choice == 1:
                    self.purchase_item(player, 'power_ups', category_choice)
                elif category_choice == 2:
                    self.purchase_item(player, 'plant_trees', category_choice)
        except ValueError:
            print('Invalid input')


