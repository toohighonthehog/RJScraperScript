VALID_TASKS = (1, 2, 3, 4, 32, 36)


query = "javliiatr4"
print (query[:5])

task = 31
if task in VALID_TASKS:
    print ("valid")
else:
    print ("not valid")