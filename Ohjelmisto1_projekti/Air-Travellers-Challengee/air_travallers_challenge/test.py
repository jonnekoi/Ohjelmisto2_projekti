from game import Game, Player, Questions
from game.store import Store
import random
from colors import *

print(f'''{color_red}
 █████  ██ ██████      ████████ ██████   █████  ██    ██ ███████ ██      ██      ███████ ██████  ███████     
██   ██ ██ ██   ██        ██    ██   ██ ██   ██ ██    ██ ██      ██      ██      ██      ██   ██ ██          
███████ ██ ██████         ██    ██████  ███████ ██    ██ █████   ██      ██      █████   ██████  ███████     
██   ██ ██ ██   ██        ██    ██   ██ ██   ██  ██  ██  ██      ██      ██      ██      ██   ██      ██     
██   ██ ██ ██   ██        ██    ██   ██ ██   ██   ████   ███████ ███████ ███████ ███████ ██   ██ ███████     
                                                                                                             
                                                                                                             
                 ██████ ██   ██  █████  ██      ██      ███████ ███    ██  ██████  ███████                   
                ██      ██   ██ ██   ██ ██      ██      ██      ████   ██ ██       ██                        
                ██      ███████ ███████ ██      ██      █████   ██ ██  ██ ██   ███ █████                     
                ██      ██   ██ ██   ██ ██      ██      ██      ██  ██ ██ ██    ██ ██                        
                 ██████ ██   ██ ██   ██ ███████ ███████ ███████ ██   ████  ██████  ███████                   
                                                                                                                                  
{color_end}''')
def setup_game():
    game = Game()
    input_name = input(f"{color_yellow}                Enter your name: {color_end} ")
    rules = input(f"{color_yellow}                Do you want to read the rules? YES or NO? {color_end}")
    if rules.upper() == 'YES':
        print(f'''{color_bright_magenta}
                ╭──────────────────────────────────────────────────────────────────────╮
                │                              Game Rules                              │
                ╰──────────────────────────────────────────────────────────────────────╯
        
                In this game, your mission is to travel between airports and accumulate points while minimizing your carbon emissions. 
        
                Your journey begins at your chosen starting airport, depending on your avatar:
                -  Donald Trump plays in the United States.
                -  Mona Lisa plays in France.
                -  Felipe IV plays in Spain.
        
                The difficulty level is also determined by your avatar:
                -  Donald Trump represents the easiest level.
                -  Mona Lisa provides a medium challenge.
                -  Felipe IV offers the hardest experience.
        
                Your objective is to reach 1000 points by answering questions and keeping your CO2 emissions as low as possible.
                As you are playing you earn point and money by answering correctly. Wrong answers deducts your points.
        
                You have the power to make a positive impact by planting trees to reduce your emissions. 
                Additionally, there are power-ups available for purchase to help you skip questions and avoid losing points.
        {color_end}
        ''')
    else:
        print('')
        print(f"{color_yellow}                You chose not to read the rules. Let's start the game!{color_end}")
    player = None
    while player is None:
        try:
            game.display_avatars()
            print('')
            input_avatar = int(input(f"{color_yellow}                Select an avatar 1-3: {color_end}"))
            if input_avatar in [1, 2, 3]:
                player = Player(input_name, input_avatar)
                player.set_starting_airport(player.avatar_id)
            else:
                print(f'{color_bright_red}                Invalid avatar. Select from 1-3.{color_end}')
        except ValueError:
            print(f'{color_bright_red}                Invalid input{color_end}')

    game.set_player(player)
    game.set_current_airport()
    game.load_closest_airports()

    questions = Questions()
    questions.set_questions(player.avatar_id)

    store = Store()

    return game, player, questions, store

def main():
    game, player, questions, store = setup_game()

    # PRINT THE QUESTIONS, RANDOMIZE ORDER OF THE QUESTIONS AND
    # RETURN THE RIGHT VALUE THAT MATCHES THE CORRECT ANSWERS INPUT
    def ask_question():
        input_ = None
        while input_ is None:
            try:
                question = questions.return_random_question()
                question_bool = questions.ask_question(question)

                input_answer = int(input('                Select correct answer by typing the corresponding number: '))
                if input_answer in [1,2,3,6]:
                    input_ = True
                    if input_answer == 6:
                        #
                        bool = player.use_question_powerup()

                        if bool == 2:
                            game.print_available_airports()
                            game.travel()

                    elif question_bool == input_answer:
                        print('''
                    ╔══════════════════════════╗ 
                      Air Travellers Challenge
                    ╚══════════════════════════╝''')

                        print(f'''
                        {color_bright_green}
                [CORRECT ANSWER] \n 
                100 points added to player.
                $75 dollars added to player\'s wallet.
                        {color_end}
                    ''')
                        player.update_points(100)
                        player.update_budget(75)
                        player.update_questions()
                        random_bool = random.randint(0, 250)
                        if random_bool < 40:
                            player.random_powerup()

                    elif question_bool != input_answer:
                        print('''
                    ╔══════════════════════════╗ 
                      Air Travellers Challenge
                    ╚══════════════════════════╝''')
                        print(f'''
                        {color_bright_red}
                [INCORRECT ANSWER] \n 
                Points deducted by 65.
                        {color_end}''')
                        player.update_points(-65)
                        player.current_answered += 1

                    else:
                        print(f'{color_bright_red}Choose the right number from the options!{color_end}')
            except ValueError:
                print(f'{color_bright_red}                Invalid input{color_end}')

    def game_loop():
        # CHECK THAT POINTS & BUDGET DON'T GO UNDER 0. SET THEM TO 0 IF THEY DO
        player.check_values(game)

        if player.current_answered > 2:
            game.display_options()
            input_continue = int(input('                Select 1-3: '))

            try:
                if input_continue:
                    if input_continue == 1:
                        game.print_available_airports()
                        game.travel()
                        game.update_game()
                    elif input_continue == 2:
                        player.display_powerups()
                    elif input_continue == 3:
                        store.display_store_options()
                        store.buy(player)
            except ValueError:
                print(f'{color_bright_red}Invalid input. Please enter a valid selection.{color_end}')
        else:
            if player.current_answered == 0:
                ask_question()

            game.display_options()

            # ASK USER TO SELECT BETWEEN THE OPTIONS
            ask = True
            while ask is True:
                try:
                    input_continue = int(input('                Select 1-4: '))
                    if input_continue:
                        if input_continue == 1:
                            ask_question()
                            ask = False
                        elif input_continue == 2:
                            game.print_available_airports()
                            game.travel()
                            game.update_game()
                            ask = False
                        elif input_continue == 3:
                            player.display_powerups()
                            ask = False
                        elif input_continue == 4:
                            store.display_store_options()
                            store.buy(player)
                            ask = False
                        else:
                            print(f'''
                            {color_bright_red}INPUT IS NOT IN THE AVAILABLE RANGE!{color_end} ''')
                            ask = False
                except ValueError:
                    print(f'{color_bright_red}                Invalid input. Please enter a valid selection.{color_end}')


    while game.game_over is not True:
        game_loop()
    print(f"""{color_bright_cyan}
      ▄████  ▄▄▄       ███▄ ▄███▓▓█████     ▒█████   ██▒   █▓▓█████  ██▀███  
     ██▒ ▀█▒▒████▄    ▓██▒▀█▀ ██▒▓█   ▀    ▒██▒  ██▒▓██░   █▒▓█   ▀ ▓██ ▒ ██▒
    ▒██░▄▄▄░▒██  ▀█▄  ▓██    ▓██░▒███      ▒██░  ██▒ ▓██  █▒░▒███   ▓██ ░▄█ ▒
    ░▓█  ██▓░██▄▄▄▄██ ▒██    ▒██ ▒▓█  ▄    ▒██   ██░  ▒██ █░░▒▓█  ▄ ▒██▀▀█▄  
    ░▒▓███▀▒ ▓█   ▓██▒▒██▒   ░██▒░▒████▒   ░ ████▓▒░   ▒▀█░  ░▒████▒░██▓ ▒██▒
     ░▒   ▒  ▒▒   ▓▒█░░ ▒░   ░  ░░░ ▒░ ░   ░ ▒░▒░▒░    ░ ▐░  ░░ ▒░ ░░ ▒▓ ░▒▓░
      ░   ░   ▒   ▒▒ ░░  ░      ░ ░ ░  ░     ░ ▒ ▒░    ░ ░░   ░ ░  ░  ░▒ ░ ▒░
    ░ ░   ░   ░   ▒   ░      ░      ░      ░ ░ ░ ▒       ░░     ░     ░░   ░ 
          ░       ░  ░       ░      ░  ░       ░ ░        ░     ░  ░   ░     
                                                         ░                      

            {color_end}""")

if __name__ == "__main__":
    main()


# TODO: POWERUP OSTO JA KÄYTTÖ ERI PELIN TILANTEISSA
# TODO: KYSYMYKSET MUUTTUVAT AINA KUN PELAAJA SYÖTTÄÄ KYSYMYSTEN VASTAUSTEN VAIHTOEHTOJEN ULKOPUOLELTA. VOIKO KYSYMYKSIÄ PITÄÄ SAMANA ETTEI PELAAJA SAA ILMAISEKSI VAIHDETTUA KYSYMYSTÄ.
# tTODO: RANDOM POWER UP SKIP QUESTION EI TOIMI, EI VÄHENNÄ POWERUPPIA
# tTODO: LOOPPAA SAMAJA KYSYMYKSIÄ KOKOAJAN?




