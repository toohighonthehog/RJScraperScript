import os, re

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
        if ord(char) in range(65, 90):
            letters = letters + char
            counter = counter + 1
        if char == deliminator:
                counter = counter + 1
                break
        if (ord(char) in range(48, 57)):
                break

    while counter < filename_length:
        char = filename[counter]
        pass
        if ord(char) in range(48, 57):
            numbers = numbers + char
            counter = counter + 1
        else:
            break
    
    while counter < filename_length:
        char = filename_original[counter]
        counter = counter + 1
        suffix = suffix + char

    number = int(numbers)

    return f"{letters}{deliminator}{number:03}{suffix}{file_extension}"

def search_for_title(input_string, deliminator = "-"):
    filename, file_extension = os.path.splitext(input_string)
    filename = filename.upper()
    file_extension = file_extension.lower()
    pattern = r'^[A-Za-z]{4}\d{3}$'

    results = []

    filename = re.sub(deliminator, '', filename, flags=re.IGNORECASE)

    counter = 0
    filename_length = len(filename)

    while counter + 6 < filename_length:
        input_string = filename[counter:counter + 7]
        if (re.match(pattern, input_string)):
            if j.code exists:
                results.append(filename[counter:counter + 7])
        counter = counter + 1

        


    return results

options = search_for_title("aabc654de-fgh-ijk-lmno123p-q-rstu-vwxyz1a23")
print (len(options))

# print(fix_file_code("miad283.mp4"))
# print(fix_file_code("miad-283.mp4"))
# print(fix_file_code("miad283abc.mp4"))
# print(fix_file_code("miad-283ABC.mp4"))
# print(fix_file_code("MIAD283.mp4"))
# print(fix_file_code("MIAD-283.mp4"))
# print(fix_file_code("MIAD283abc.mp4"))
# print(fix_file_code("MIAD-283ABC.mp4"))
# print(fix_file_code("MIAD283abc.mp4"))
# print(fix_file_code("MIAD-283-ABC.mp4"))
# print(fix_file_code("MIAD283-abc123.mp4"))
# print(fix_file_code("MIAD-283-ABC123.mp4"))
# print(fix_file_code("MIAD283abc-EN.srt"))
# print(fix_file_code("MIAD-283-ABC-en.srt"))
# print(fix_file_code("MIAD283-abc123-en.srt"))
# print(fix_file_code("MIAD-283-ABC123-EN.srt"))
