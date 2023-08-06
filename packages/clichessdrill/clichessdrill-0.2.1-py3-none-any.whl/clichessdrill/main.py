"""
cli entrypoint
"""
import os
import time
import json
import random
from clichessdrill.menu import Menu, PositiveIntegerInputMenuSection, YesNoInputMenuSection, \
    FilePathInputMenuSection

from clichessdrill.game import Game
from clichessdrill.pieces import Pieces

THIS_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
DEFAULT_GAME_PLAN = os.path.join(THIS_DIRECTORY, '..', 'game_plans', 'default.json')

random.seed(int(time.time()))


def main():
    """Main entry point. Start drill."""

    menu = Menu([
        {
            'menu_section': PositiveIntegerInputMenuSection(
                prompt_message='How many drill rounds? '),
            'parameter': 'n_rounds',
            'default': 1
        },
        {
            'menu_section': YesNoInputMenuSection(
                prompt_message='Would you like to use your own custom game plan (y/n): '),
            'parameter': 'custom_game_plan',
            'default': False,
        },
        {
            'menu_section': FilePathInputMenuSection(
                prompt_message='File path to your custom game plan: '),
            'parameter': 'game_plan_file_path',
            'default': DEFAULT_GAME_PLAN,
            'condition': {
                'custom_game_plan': True
            }
        },
    ])
    user_choices = menu.show()

    training_file_path = user_choices.get('game_plan_file_path', DEFAULT_GAME_PLAN)
    n_rounds = user_choices['n_rounds']

    with open(training_file_path, encoding='utf-8') as _f:
        plan = json.loads(_f.read())

    for _ in range(n_rounds):
        user_pieces = random.choice([Pieces.WHITE, Pieces.BLACK])
        game = Game(plan=plan, user_pieces=user_pieces)
        game.run()
        time.sleep(1)
