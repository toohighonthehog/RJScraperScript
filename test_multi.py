PROCESS_LIST = [{'base': "/mnt/multimedia/Other/RatedFinalJ/Censored/General/", 'prate': 0, 'target': None}, \
                    {'base': "/mnt/multimedia/Other/RatedFinalJ/Censored/07/", 'prate': 7, 'target': None}, \
                    {'base': "/mnt/multimedia/Other/RatedFinalJ/Censored/08/", 'prate': 8, 'target': None}, \
                    {'base': "/mnt/multimedia/Other/RatedFinalJ/Censored/09/", 'prate': 9, 'target': None}, \
                    {'base': "/mnt/multimedia/Other/RatedFinalJ/Censored/10/", 'prate': 10, 'target': None}, \
                    {'base': "/mnt/multimedia/Other/RatedFinalJ/Names/", 'prate': 0, 'target': None}, \
                    {'base': "/mnt/multimedia/Other/RatedFinalJ/Series/", 'prate': 0, 'target': None}]

for PROCESS_ITEM in PROCESS_LIST:
    BASE_DIRECTORY = PROCESS_ITEM['base']

    ARBITRARY_PRATE = PROCESS_ITEM['prate']
    if PROCESS_ITEM['target'] is None:
        TARGET_DIRECTORY = PROCESS_ITEM['base']
    else:
        TARGET_DIRECTORY = PROCESS_ITEM['target']

    print(f"{BASE_DIRECTORY} # {TARGET_DIRECTORY} # {ARBITRARY_PRATE}")
