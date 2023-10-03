import re

# Define the allowed extensions in an array
SOURCE_EXTENSIONS = [".mkv", ".mp4", ".avi", ".xxx", ".txt"]

# Create the regular expression pattern
#pattern = r'^[A-Z]{2,4}-\d{3}\.(?:' + '|'.join(SOURCE_EXTENSIONS) + ')$'
pattern = r'^[A-Z]{2,5}-\d{3}(?:' + '|'.join(SOURCE_EXTENSIONS) + ')$'

# Test the regular expression
test_strings = ["ab-123.pdf", "abc-456.txt", "abcd-789.doc", "a-123.jpg", "abcde-12.png", "abc-1234.txt", "MIAD-283", "MIAD-283.mp4", "DOCP-093.txt", "DOCP093.mp4", "MIAD283.xxx", "FSDSS-017.mp4", "IPZZ-002.mp4", "MIFD-017.mp4"]

for test_string in test_strings:
    if re.match(pattern, test_string):
        print(f"'{test_string}' is a valid match.")
    else:
        print(f"'{test_string}' is not a valid match.")