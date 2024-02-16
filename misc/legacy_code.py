# def old_search_for_title(f_input_string, f_delimiter="-"):
#     # This can probably be simplified with some good regular expressions.
#     p_filename, p_file_extension = os.path.splitext(f_input_string)
#     p_filename = p_filename.upper()
#     p_file_extension = p_file_extension.lower()
#     p_patternX = r'^[A-Za-z]{7}\d{3}$'
#     p_pattern9 = r'^[A-Za-z]{6}\d{3}$'
#     p_pattern8 = r'^[A-Za-z]{5}\d{3}$'
#     p_pattern7 = r'^[A-Za-z]{4}\d{3}$'
#     p_pattern6 = r'^[A-Za-z]{3}\d{3}$'
#     p_pattern5 = r'^[A-Za-z]{2}\d{3}$'
#     p_results = []
#     p_filename = re.sub(f_delimiter, '', p_filename, flags=re.IGNORECASE)
#     p_filename_length = len(p_filename)

#     # Search for 10 character codes.
#     p_counter = 0
#     while p_counter + 9 < p_filename_length:
#         f_input_string = p_filename[p_counter:p_counter + 10]
#         if (re.match(p_patternX, f_input_string)):
#             if my_javlibrary_new_getvideo(f_input_string):
#                 p_results.append(p_filename[p_counter:p_counter + 10])
#         p_counter += 1

#     # Search for 9 character codes.
#     p_counter = 0
#     while p_counter + 8 < p_filename_length:
#         f_input_string = p_filename[p_counter:p_counter + 9]
#         if (re.match(p_pattern9, f_input_string)):
#             if my_javlibrary_new_getvideo(f_input_string):
#                 p_results.append(p_filename[p_counter:p_counter + 9])
#         p_counter += 1

#     # Search for 8 character codes.
#     p_counter = 0
#     while p_counter + 7 < p_filename_length:
#         f_input_string = p_filename[p_counter:p_counter + 8]
#         if (re.match(p_pattern8, f_input_string)):
#             if my_javlibrary_new_getvideo(f_input_string):
#                 p_results.append(p_filename[p_counter:p_counter + 8])
#         p_counter += 1

#     # Search for 7 character codes.
#     p_counter = 0
#     while p_counter + 6 < p_filename_length:
#         f_input_string = p_filename[p_counter:p_counter + 7]
#         if (re.match(p_pattern7, f_input_string)):
#             if my_javlibrary_new_getvideo(f_input_string):
#                 p_results.append(p_filename[p_counter:p_counter + 7])
#         p_counter += 1

#     # Search for 6 character codes.
#     p_counter = 0
#     while p_counter + 5 < p_filename_length:
#         f_input_string = p_filename[p_counter:p_counter + 6]
#         if (re.match(p_pattern6, f_input_string)):
#             if my_javlibrary_new_getvideo(f_input_string):
#                 p_results.append(p_filename[p_counter:p_counter + 6])
#         p_counter += 1

#     # Search for 5 character codes.
#     p_counter = 0
#     while p_counter + 4 < p_filename_length:
#         f_input_string = p_filename[p_counter:p_counter + 5]
#         if (re.match(p_pattern5, f_input_string)):
#             if my_javlibrary_new_getvideo(f_input_string):
#                 p_results.append(p_filename[p_counter:p_counter + 5])
#         p_counter += 1

#     pass

#     p_results = remove_substrings(p_results)

#     return p_results


# def generate_substrings(f_input_string):
#     f_my_javlibrary = JAVLibrary()
#     p_input_string = f_input_string.upper()
#     p_input_string = re.sub(r'[^A-Z0-9]', '', p_input_string)
#     p_input_string += "Z"
#     p_pattern = r'([A-Z]){2,}[0-9]{3,}([A-Z])'

#     p_substrings = set()
#     for p_loop in range(len(p_input_string)):
#         p_substring = p_input_string[p_loop:]
#         if re.match(p_pattern, p_substring):
#             p_matched_value = ((re.match(p_pattern, p_substring)).group())
#             p_matched_value = p_matched_value[:-1]
#             p_get_video = (f_my_javlibrary.get_video(p_matched_value))
#             if (p_get_video):
#                 p_substrings.add(p_get_video.code)

#     return list(p_substrings)


# def my_javlibrary_new_getvideo(f_input_string):
#     p_my_javlibrary = JAVLibrary()
#     p_count = 0
#     p_results = None
#     while p_results == None and p_count <= 5:
#         try:
#             p_results = p_my_javlibrary.get_video(f_input_string)
#             p_count = 6
#         except:
#             pass
#         time.sleep(0.25 * p_count)
#         p_count += 1

#     if p_results != None:
#         if p_count > 0:
#             p_value1 = search_for_title(p_results.code)
#             p_value2 = search_for_title(f_input_string)

#             if (p_value1 != p_value2):
#                 p_results = ""

#     pass

#     return p_results



# def my_javlibrary_new_search(f_input_string):
#     p_my_javlibrary = JAVLibrary()
#     p_count = 0
#     p_results = []
#     while p_results == [] and p_count <= 5:
#         try:
#             p_results = p_my_javlibrary.search(f_input_string)
#             p_count = 6
#         except:
#             time.sleep(0.25 * p_count)
#         p_count += 1

#         if p_my_javlibrary.getvideo(f_input_string) == "":
#             p_results = []

#         pass

#     return p_results
