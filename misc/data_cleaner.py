import os, mysql.connector, fnmatch
from icecream import ic

def get_file_array(f_folder_path, f_source_extensions):
    file_list_1 = []
    file_list_2 = []
    for root, dirs, files in os.walk(f_folder_path):
        print(root + " " * 50, end="\r")
        for extension in f_source_extensions:
            for file in fnmatch.filter(files, f"*{extension}"):
                filename, file_extension = os.path.splitext(os.path.basename(file))
                file_list_1.append((filename.upper(), os.path.join(root, file)))
                if (not file.endswith(".xxx")):
                    file_list_2.append((filename.upper(), os.path.join(root, file)))

    print ("\n")
    return sorted(file_list_1, key = take_first), sorted(file_list_2, key = take_first)

def get_db_array(f_my_cursor):
    my_sql_query = "SELECT code, location FROM title WHERE location IS NOT NULL ORDER BY code"
    f_my_cursor.execute (my_sql_query)

    return f_my_cursor.fetchall()

def get_duplicates(f_file_array):
    compare_file = ""
    results = []

    for file in f_file_array:
        if file[0] == compare_file:
            results.append((compare_file, compare_line[1]))
            results.append((compare_file, file[1]))
        compare_file = file[0]
        compare_line = file

    return results

def take_first(elem):
    return elem[0]

if __name__ == "__main__":
    folder_path = "/mnt/multimedia/Other/RatedFinalJ/"
    SOURCE_EXTENSIONS = [".mkv", ".mp4", ".avi", ".xxx"]
    my_connection = mysql.connector.connect( 
        user="rjohnson", 
        password="5Nf%GB6r10bD", 
        host="mariadb.hachiko.int", 
        port=3306, 
        database="Multimedia" 
    )
    my_cursor = my_connection.cursor()

    file_array_1, file_array_2 = get_file_array(folder_path, SOURCE_EXTENSIONS)
    db_array = get_db_array(my_cursor)
    duplicates = get_duplicates(file_array_1)

    print (file_array_1)

    file_array_1_set = set(file_array_1)
    file_array_2_set = set(file_array_2)
    db_array_set = set (db_array)
    duplicates_set = set (duplicates)

    os.system('clear')

    print ("Duplicates")
    ic (duplicates)
    print ()

    print ("Missing from DB") # move to parent
    ic (file_array_2_set.difference(db_array_set.union(duplicates_set)))
    print ()

    print ("Missing from Filesystem")
    ic (db_array_set.difference(file_array_1_set))
    print ()

    my_cursor.close()
    my_connection.disconnect()