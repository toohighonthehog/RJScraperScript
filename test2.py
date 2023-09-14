import os

def fix_file_code(input_string, deliminator = "-"):
    letters = ""
    numbers = ""
    suffix = ""
    filename, file_extension = os.path.splitext(input_string)
    filename = filename.upper()
    file_extension = file_extension.lower()

    counter = 0
    filename_length = len(filename)
    
    # get letters
    while counter < filename_length:
        char = filename[counter]

        if ord(char) in range(65, 90):
            letters = letters + char
        elif ord(char) != deliminator:
            counter = counter + 1
            break
        counter = counter + 1


    while counter < filename_length:
        char = filename[counter]
        counter = counter + 1
        if ord(char) in range(48, 57):
            numbers = numbers + char
        else:
            break
        

    while counter < filename_length:
        char = filename[counter]
        counter = counter + 1
        suffix = suffix + char


    # for char in filename:
    #     if ord(char) in range(65, 91):
    #         letters += char
    #     elif ord(char) in range(48, 58):
    #         numbers += char

    # letters = letters.upper()
    number = int(numbers)

    correct_name1 = f"{letters}{deliminator}{number:03}{suffix}{file_extension}" # needed?
    #correct_name3 = correct_name2

    #correct_name4 = correct_name3 + file_extension

    correct_name_final = correct_name1
    
    # print (letters)
    # print (numbers)
    # print (suffix)
    return correct_name_final


print(fix_file_code("miad283.mp4"))
print(fix_file_code("miad-283.mp4"))
print(fix_file_code("miad283abc.mp4"))
print(fix_file_code("miad-283ABC.mp4"))
print(fix_file_code("MIAD283.mp4"))
print(fix_file_code("MIAD-283.mp4"))
print(fix_file_code("MIAD283abc.mp4"))
print(fix_file_code("MIAD-283ABC.mp4"))
print(fix_file_code("MIAD283abc.mp4"))
print(fix_file_code("MIAD-283-ABC.mp4"))
print(fix_file_code("MIAD283-abc123.mp4"))
print(fix_file_code("MIAD-283-ABC123.mp4"))


#the code is at the beginning, always some letters, then some numbers
#after these have been found, stop processing

