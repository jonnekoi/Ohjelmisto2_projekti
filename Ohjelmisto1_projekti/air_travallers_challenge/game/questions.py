import random
from database.db_models import get_random_question_sql

def get_random_question(avatar_id):
    questions = get_random_question_sql(avatar_id)

    print(questions)


    