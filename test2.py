import os, re
from javscraper import *
my_javlibrary = JAVLibrary()

def fix_file_code(input_string, deliminator = "-"):
    letters = ""
    numbers = ""
    suffix = ""
    filename, file_extension = os.path.splitext(input_string)
    filename_original = filename
    filename = filename.upper()
    file_extension = file_extension.lower()

    counter = 0
    filename_length = len(filename)
    
    # get letters
    while counter < filename_length:
        char = filename[counter]
        pass
        if ord(char) in range(64, 91):
            letters = letters + char
            counter = counter + 1
        if char == deliminator:
                counter = counter + 1
                break
        if (ord(char) in range(47, 58)):
                break

    while counter < filename_length:
        char = filename[counter]
        pass
        if ord(char) in range(47, 58):
            numbers = numbers + char
            counter = counter + 1
        else:
            break
    
    while counter < filename_length:
        char = filename_original[counter]
        counter = counter + 1
        suffix = suffix + char

    number = int(numbers)
    result = f"{letters}{deliminator}{number:03}{suffix}{file_extension}"
    pass

    return f"{letters}{deliminator}{number:03}{suffix}{file_extension}"

def search_for_title(input_string, delimiter = "-"):
    filename, file_extension = os.path.splitext(input_string)
    filename = filename.upper()
    file_extension = file_extension.lower()
    pattern1 = r'^[A-Za-z]{5}\d{3}$'
    pattern2 = r'^[A-Za-z]{4}\d{3}$'
    pattern3 = r'^[A-Za-z]{3}\d{3}$'

    results = []

    filename = re.sub(delimiter, '', filename, flags=re.IGNORECASE)

    filename_length = len(filename)

    # Search for 8 character codes.
    counter = 0
    while counter + 7 < filename_length:
        input_string = filename[counter:counter + 8]
        if (re.match(pattern1, input_string)):
            if my_javlibrary.search(input_string):
                results.append(filename[counter:counter + 8])
        counter = counter + 1    
    
    # Search for 7 character codes.
    counter = 0
    while counter + 6 < filename_length:
        input_string = filename[counter:counter + 7]
        if (re.match(pattern2, input_string)):
            if my_javlibrary.search(input_string):
                results.append(filename[counter:counter + 7])
        counter = counter + 1

    # Search for 6 character codes.
    counter = 0
    while counter + 5 < filename_length:
        input_string = filename[counter:counter + 6]
        if (re.match(pattern3, input_string)):
            if my_javlibrary.search(input_string):
                results.append(filename[counter:counter + 6])
        counter = counter + 1

    results = remove_substrings(results)

    return results

def remove_substrings(strings):
    # Sort the strings by length in descending order
    strings.sort(key=len, reverse=True)
    
    # Initialize a list to store non-substring strings
    result = []
    
    # Iterate through the sorted strings
    for s in strings:
        # Check if the current string is a substring of any previously added string
        is_substring = any(s in r for r in result)
        
        # If it's not a substring of any previous string, add it to the result
        if not is_substring:
            result.append(s)
    
    return result

options = search_for_title("MIAD283")
print (options)

print(my_javlibrary.search("DOCP044")) 
#print (my_javlibrary.get_video ("MIAD283"))
# options = search_for_title("hjd2048.com-1129tek097-h264.mp4")
# print (options)

# print(fix_file_code("DOCP094.mp4"))
# print(fix_file_code("DOCP-094.mp4"))
# print(fix_file_code("DOCP094abc.mp4"))
# print(fix_file_code("DOCP-094ABC.mp4"))
# print(fix_file_code("DOCP094.mp4"))
# print(fix_file_code("DOCP-094.mp4"))
# print(fix_file_code("DOCP094abc.mp4"))
# print(fix_file_code("DOCP-094ABC.mp4"))
# print(fix_file_code("DOCP094abc.mp4"))
# print(fix_file_code("DOCP-094-ABC.mp4"))
# print(fix_file_code("DOCP094-abc123.mp4"))
# print(fix_file_code("DOCP-094-ABC123.mp4"))
# print(fix_file_code("DOCP094abc-EN.srt"))
# print(fix_file_code("DOCP-094-ABC-en.srt"))
# print(fix_file_code("DOCP094-abc123-en.srt"))
# print(fix_file_code("DOCP-094-ABC123-EN.srt"))
