"""
The user menu shown at start of the app
"""
import os
from abc import ABC, abstractmethod
from typing import Tuple, List


class MenuSection(ABC):
    """
    Abstract menu section. Responsible for displaying menu section, verifying and formatting input
    """

    N_RETRIES = 3
    MESSAGE_USER_WRONG_USE_MENU = \
        f'No valid entry provided after {N_RETRIES} retries. Using default.'

    def __init__(self, prompt_message: str):
        self.prompt_message = prompt_message

    @abstractmethod
    def verify(self, user_input: str) -> Tuple[bool, str]:
        """Verify user input"""

    @abstractmethod
    def format(self, user_input: str) -> object:
        """Format user input"""

    def show(self):
        """Display the menu section and process user input"""

        for _ in range(self.N_RETRIES):
            raw_user_input = input(self.prompt_message)
            valid_input, message = self.verify(raw_user_input)
            if valid_input:
                break
            print(message + '\n')

        if not valid_input:
            print(self.MESSAGE_USER_WRONG_USE_MENU)
            return None

        return self.format(raw_user_input)


class PositiveIntegerInputMenuSection(MenuSection):
    """Menu section for number input of positive integers"""

    def verify(self, user_input: str) -> Tuple[bool, str]:
        """Verify user input"""

        valid = True
        advise_message = 'positive integer number input required.'

        try:
            user_input = int(user_input)
        except ValueError:
            valid = False
        except TypeError:
            valid = False

        if not valid:
            return valid, advise_message

        if user_input < 1:
            valid = False
            return valid, advise_message

        return valid, None

    def format(self, user_input: str) -> object:
        """Format user input"""
        return int(user_input)


class FilePathInputMenuSection(MenuSection):
    """Menu section of file path input from user."""

    def verify(self, user_input: str) -> Tuple[bool, str]:
        """Verify user input"""

        advise_message = 'File path to existing json file required.'

        valid = user_input.endswith('.json')
        if not valid:
            return valid, advise_message

        valid = os.path.exists(user_input)
        if not valid:
            return valid, advise_message

        return valid, None

    def format(self, user_input: str) -> object:
        """Format user input"""
        return user_input


class YesNoInputMenuSection(MenuSection):
    """Menu section for user input that is either yes or no. Chose no if input ambiguous"""

    def verify(self, user_input: str) -> Tuple[bool, str]:
        """Verify user input"""
        return True, None

    def format(self, user_input: str) -> object:
        """Format user input"""

        return user_input.lower() in ('yes', 'y')


class Menu:
    """Menu composed of one or more menu sections. Responsible for sequentially showing menu
    sections, evaluating input and collecting formatted input"""

    def __init__(self, sections: List):
        self.sections = sections

    def show(self):
        """Sequentially show menu sections if conditions are met"""
        user_choices = {}
        for section in self.sections:

            # if conditions are not met, skip this section
            break_flag = False
            if 'condition' in section:
                for _key, _value in section['condition'].items():
                    if user_choices[_key] != _value:
                        break_flag = True
                        break
            if break_flag:
                continue

            menu_section = section['menu_section']
            user_response = menu_section.show()
            user_response = section['default'] if user_response is None else user_response
            user_choices[section['parameter']] = user_response
        return user_choices

    def get_parameters(self):
        """Return list of parameters of all menu sections"""
        return [section['parameters'] for section in self.sections]
