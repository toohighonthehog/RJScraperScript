import re

def insert_hyphens(input_string):
    # Use regular expressions to separate letters and numbers
    match = re.match(r'([A-Za-z]{5})(\d{3})', input_string)
    
    if match:
        letters = match.group(1)
        numbers = match.group(2)
        
        # Insert hyphen between letters and numbers
        result_string = f'{letters}-{numbers}'
        return result_string
    else:
        return "Invalid input format. Please provide 5 letters followed by 3 numbers."

# Input string containing 5 letters and 3 numbers
input_string = input("Enter a string of 5 letters followed by 3 numbers: ")

# Call the function to insert hyphens
result = insert_hyphens(input_string)

# Print the result
print("Result:", result)