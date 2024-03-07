import logging, sys, os, datetime
from datetime import datetime

__all__ = ["logt", "get_console_handler", "get_file_handler", "get_logger"]

def logt(f_left = "", f_right = "", f_middle = " ", f_width = 0):

    # logging width - minimum of 80 and maximum of 140
    # We need to work out these numbers properly - its a bit of a mess.
    # FYI, the log preamble is 29 characters.
    p_display_width = (os.get_terminal_size().columns - 40)
    p_text_width = (max((min(p_display_width, 100), 60)))

    if f_width > 0: p_width = f_width
    if f_width == 0: p_width = p_text_width
    if f_width < 0: p_width =  p_text_width + f_width
    if len(f_left) == 1:
        f_result = f_left * p_width
        return (f_result)
    
    p_middle_length = p_width - (len(f_left) + len(f_right))

    f_result = f_left + (p_middle_length * f_middle) + f_right
    return (f"x{f_result}x")

def get_console_handler():
    p_console_handler = logging.StreamHandler(sys.stdout)
    p_console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    p_console_handler.setLevel(logging.INFO)
    return p_console_handler

def get_file_handler():
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

