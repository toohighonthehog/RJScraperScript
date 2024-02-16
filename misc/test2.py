metadata_array = {
    "code": "abc",
    "name": None,
    "actor": [],
    "studio": None,
    "image": None,
    "genre": [],
    "url": [],
    "score": None,
    "release_date": None,
    "added_date": None,
    "file_date": None,
    "location": None,
    "subtitles": None,
    "prate": None,
    "notes": None,
    "status": 7
}

def logger_text(f_left = "", f_right = "", f_middle = " ", f_width = 120):
    if len(f_left) == 1:
        return (f_left * f_width)
    
    p_middle_length = f_width - (len(f_left) + len(f_right))

    return (f_left + (p_middle_length * f_middle) + f_right)

print (logger_text("-"))
print (logger_text("abcd"))
print (logger_text(f_right = "xyz"))
print (logger_text(f_left = "abc", f_right = "xyz"))
print (logger_text("+"))

# metadata_array["studio"] = "xyz"
# metadata_array["studio"] = "sdd"

# print (metadata_array["code"])
# print (metadata_array["studio"])