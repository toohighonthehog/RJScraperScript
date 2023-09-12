import os

def insert_hyphen_between_letters_and_numbers(input_string, delim = "-"):
    letters = ""
    numbers = ""

    file_name, file_extension = os.path.splitext(input_string)
    file_name = file_name.upper()
    file_extension = file_extension.lower()

    for char in file_name:
        if ord(char) in range(65, 91):
            letters += char
        elif ord(char) in range(48, 58):
            numbers += char

    number = int(numbers)
    return f"{letters}{delim}{number:03}{file_extension}"

print(insert_hyphen_between_letters_and_numbers("DOCP000094.mp4"))