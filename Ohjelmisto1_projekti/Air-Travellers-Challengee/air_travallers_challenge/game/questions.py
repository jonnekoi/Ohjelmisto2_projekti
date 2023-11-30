import random
import json
from database.db_models import get_questions_avatar_sql

color_yellow = "\033[93m"
color_red = "\033[91m"
color_end = "\033[0m"

# GET QUESTIONS FOR PLAYER
class Questions:
    def __init__(self):
        self.questions = {}

# SET QUESTIONS IN QUESTIONS INSTANCE
    def set_questions(self, avatar_id):
        questions = get_questions_avatar_sql(avatar_id)
        self.questions = questions

    def return_random_question(self):
        questions_dict = {}
        for i, question in enumerate(self.questions):
            question_json = json.dumps(question)
            questions_dict[f"question-{i+1}"] = f'{question_json}'

    
        random_question_key = random.choice(list(questions_dict.keys()))
        selected_question_json = questions_dict[random_question_key]

        # print(questions_dict)
        
        try:
            selected_question = json.loads(selected_question_json)
            return selected_question
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return {}  # Return an empty dictionary on error
    

    def ask_question(self, question):
        print(f'''
                        {color_yellow}[QUESTION]{color_end}
              ''')
        print(f'                {question["question_text"]}')

        # PUT QUESTIONS IN RANDOM ORDER & PRINT THEM
        rand = random.randint(0, 100)

        if rand < 33:
            print(f'''
                1. {question["answer"]}
                2. {question["wrong_answer"]} 
                3. {question["wrong_answer2"]}

                6. USE POWER-UP''')
            return 1
        elif rand > 66:
            print(f'''
                1. {question["wrong_answer"]}
                2. {question["answer"]}
                3. {question["wrong_answer2"]}

                6. USE POWER-UP ''')
            return 2
        else:
            print(f'''
                1. {question["wrong_answer2"]}
                2. {question["wrong_answer"]}
                3. {question["answer"]}

                6. USE POWER-UP''')
            return 3


    