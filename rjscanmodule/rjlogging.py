import logging, sys, os, datetime
from datetime import datetime
#import rich
from rich.logging import RichHandler
#from rich.console import RichConsole
#from rich.theme import RichTheme

__all__ = ["logt", "get_console_handler", "get_file_handler", "get_logger"]

def logt(f_left = "", f_right = "", f_middle = " ", f_width = 0):

    # logging width - minimum of 80 and maximum of 140
    # We need to work out these numbers properly - its a bit of a mess.
    # FYI, the log preamble is 29 characters.

    p_text_width = (os.get_terminal_size().columns - 49)

    if f_width > 0: p_width = f_width
    if f_width == 0: p_width = p_text_width
    if f_width < 0: p_width =  p_text_width + f_width
    if len(f_left) == 1:
        f_result = f_left * p_width
        return (f_result)
    
    p_middle_length = p_width - (len(f_left) + len(f_right))

    f_result = f_left + (p_middle_length * f_middle) + f_right
    return (f_result)

def get_console_handler():
    p_text_width = (os.get_terminal_size().columns - 47)
    #p_text_width = (max((min(p_display_width, 100), 60)))
    p_console_handler = RichHandler(show_path=False)

    p_formatter = "%(message)-." + str(p_text_width) + "s"
    #p_formatter = "%(message)-." + str(20) + "s"
    #print (p_formatter)
    p_console_handler.setFormatter(logging.Formatter(p_formatter))
    p_console_handler.setLevel(logging.INFO)
    return p_console_handler

def get_file_handler():
    if not os.path.exists('./logs'):
        os.makedirs('./logs', exist_ok=True)
    
    p_file_handler = logging.FileHandler('./logs/{:%Y-%m-%d_%H.%M.%S}.log'.format(datetime.now()), mode='w')
    p_file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    p_file_handler.setLevel(logging.DEBUG)
    return p_file_handler

def get_logger():
    p_logger = logging.getLogger()
    p_logger.setLevel(logging.DEBUG)
    p_logger.addHandler(get_console_handler())
    p_logger.addHandler(get_file_handler())
    return p_logger

