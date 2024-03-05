import os, re, requests, hashlib, time, json, shutil, sys
from requests_html import HTMLSession
from datetime import datetime
from javscraper import *

# region Main Functions

# endregion
    
# region General Utility Functions



# endregion

# region Probably unused functions



# def remove_substrings(f_strings):
#     # Sort the strings by length in descending order
#     f_strings.sort(key=len, reverse=True)
#     p_result = []
#     # Iterate through the sorted strings
#     for s in f_strings:
#         # Check if the current string is a substring of any previously added string
#         is_substring = any(s in r for r in p_result)
#         # If it's not a substring of any previous string, add it to the result
#         if not is_substring:
#             p_result.append(s)
#     return p_result


# def value_in_list(f_list, f_value):
#     p_results = False

#     for i in f_list:
#         if f_value in i['code']:
#             p_results = i
#             break
#         else:
#             p_results = {'code': f_value, 'status': 0, 'location': None}

#     return p_results

# def fix_file_code(f_input_string, f_delimiter="-"):
#     # This can probably be simplified with some good regular expressions.
#     p_letters = ""
#     p_numbers = ""
#     p_suffix = ""
#     p_filename, p_file_extension = os.path.splitext(f_input_string)
#     p_filename_original = p_filename
#     p_filename = p_filename.upper()
#     p_file_extension = p_file_extension.lower()
#     p_counter = 0
#     p_filename_length = len(p_filename)

#     # get letters
#     while p_counter < p_filename_length:
#         p_char = p_filename[p_counter]

#         if ord(p_char) in range(64, 91):
#             p_letters = p_letters + p_char
#             p_counter += 1
#         if ord(p_char) in range(47, 58):
#             break
#         if ord(p_char) not in range(64, 91):
#             p_counter += 1
#             break

#     # get numbers
#     while p_counter < p_filename_length:
#         p_char = p_filename[p_counter]

#         if ord(p_char) in range(47, 58):
#             p_numbers = p_numbers + p_char
#         else:
#             break
#         p_counter += 1

#     while p_counter < p_filename_length:
#         p_char = p_filename_original[p_counter]
#         p_counter += 1
#         p_suffix = p_suffix + p_char

#     p_number = int(p_numbers)

#     return f"{p_letters}{f_delimiter}{p_number:03}{p_suffix}{p_file_extension}"

# endregion