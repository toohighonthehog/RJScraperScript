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

def search_for_title(input_string, deliminator = "-"):
    filename, file_extension = os.path.splitext(input_string)
    filename = filename.upper()
    file_extension = file_extension.lower()
    pattern1 = r'^[A-Za-z]{4}\d{3}$'
    pattern2 = r'^[A-Za-z]{3}\d{3}$'

    results = []

    filename = re.sub(deliminator, '', filename, flags=re.IGNORECASE)


    filename_length = len(filename)

    counter = 0
    while counter + 6 < filename_length:
        input_string = filename[counter:counter + 7]
        if (re.match(pattern1, input_string)):
            if my_javlibrary.search(input_string):
                results.append(filename[counter:counter + 7])
        counter = counter + 1

    counter = 0
    while counter + 5 < filename_length:
        input_string = filename[counter:counter + 6]
        if (re.match(pattern2, input_string)):
            if my_javlibrary.search(input_string):
                results.append(filename[counter:counter + 6])
        counter = counter + 1

    return results

# options = search_for_title("aabc6DoCP-094tek09754de-fgh-ijk-lmno123p-q-rstu-vwDOCP094xyz1a23.mkv")
# print (options)
# options = search_for_title("hjd2048.com-1129tek097-h264.mp4")
# print (options)

print(fix_file_code("DOCP094.mp4"))
print(fix_file_code("DOCP-094.mp4"))
print(fix_file_code("DOCP094abc.mp4"))
print(fix_file_code("DOCP-094ABC.mp4"))
print(fix_file_code("DOCP094.mp4"))
print(fix_file_code("DOCP-094.mp4"))
print(fix_file_code("DOCP094abc.mp4"))
print(fix_file_code("DOCP-094ABC.mp4"))
print(fix_file_code("DOCP094abc.mp4"))
print(fix_file_code("DOCP-094-ABC.mp4"))
print(fix_file_code("DOCP094-abc123.mp4"))
print(fix_file_code("DOCP-094-ABC123.mp4"))
print(fix_file_code("DOCP094abc-EN.srt"))
print(fix_file_code("DOCP-094-ABC-en.srt"))
print(fix_file_code("DOCP094-abc123-en.srt"))
print(fix_file_code("DOCP-094-ABC123-EN.srt"))
