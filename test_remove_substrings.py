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

# Example usage:
input_strings = ["apple", "IAD093", "banana", "app", "ana", "cherry","CAWD064", "AWD064","MIAD093"]
filtered_strings = remove_substrings(input_strings)
print(filtered_strings)
