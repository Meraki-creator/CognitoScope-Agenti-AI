from questions import QUESTION_BANK
import random

def generate_question(assessment_type):
    return random.choice(
        QUESTION_BANK[assessment_type]
    )