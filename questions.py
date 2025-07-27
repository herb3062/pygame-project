import pygame
import random 
from main_character import Player

def questions():
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    op = random.choice(['+', '-', '*'])

    if op == '+':
        question = f"What is {a} + {b}?"
        answer = str(a + b)
    elif op == '-':
        question = f"What is {a} - {b}?"
        answer = str(a - b)
    else:
        question = f"What is {a} * {b}?"
        answer = str(a * b)

    prompt = f"Would you like to answer this question for a power-up?\nType your answer or 'no' to skip.\n{question}"
    return prompt, answer