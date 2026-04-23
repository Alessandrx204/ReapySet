import functools

from src.ReadySet.window_reshaping_logic import LangSetup

def d_with_common_window_resizing_logic(func):
    @functools.wraps(func)
    def wrapper(p_window, p_buttons, *args, **kwargs):
        LangSetup.disable_language_buttons(p_buttons)
        LangSetup.common_window_update(p_window, p_buttons)
        return func(*args, **kwargs)  # init_python non ne ha bisogno
    return wrapper


class LangSpecificButtons:
    @staticmethod
    @d_with_common_window_resizing_logic
    def init_python():
        print("Initializing Python")