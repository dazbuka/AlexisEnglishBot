from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup


class MenuStateParams:
    def __init__(self,
                 curr_call : str,
                 curr_menu : list,
                 curr_main_mess: str = None):

        self.curr_call : str = curr_call
        self.curr_menu : list = curr_menu #
        self.curr_main_mess : str = curr_main_mess #

    def __repr__(self):
        presentation = f' - {self.curr_call} - {self.curr_menu} - {self.curr_main_mess}'
        return presentation

