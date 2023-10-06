import os, mysql.connector, fnmatch
from collections import defaultdict

os.system('clear')

def find_duplicate_files(folder_path, min_file_size):
    # Create a dictionary to store files with the same base name
    file_dict = defaultdict(list)

    # Walk through the folder structure
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            # Get the base file name without the extension
            base_name = os.path.splitext(file_name)[0]
            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size >= min_file_size:
                # Add the file to the dictionary using the base name (ignoring extension)
                file_dict[base_name.lower()].append(file_path)

    # Filter out files with only one occurrence (no duplicates)
    duplicate_files = {base_name: paths for base_name, paths in file_dict.items() if len(paths) > 1}

    return duplicate_files

def find_orphaned_files(f_folder_path, f_source_extension):
    # go through each line of the database and make sure the file exists.
    pass

def find_orphaned_records(f_folder_path, f_source_extension, f_my_cursor):
    file_list = []
    
    
    for root, dirs, files in os.walk(f_folder_path):
        print(root + " " * 50, end="\r")
        for extension in f_source_extension:
            for file in fnmatch.filter(files, f"*{extension}"):
                my_sql_query = "SELECT * from title WHERE location = '" + file + "'"
                f_my_cursor.execute (my_sql_query)
                try:
                    row = my_cursor.fetchone()
                except:
                    file_list.append(os.path.join(root, file))
                    row = None

                if row == None:
                    file_list.append(os.path.join(root, file))
                    #print(file)

    return file_list
    # go through the folder path, look for files with the extension, check if that file exists in the DB.
    pass

if __name__ == "__main__":
    folder_path = "/mnt/multimedia/Other/RatedFinalJ/"
    SOURCE_EXTENSIONS = [".mkv", ".mp4", ".avi", ".xxx"]
    my_connection = mysql.connector.connect( 
        user="rjohnson", 
        password="5Nf%GB6r10bD", 
        host="diskstation.hachiko.int", 
        port=3306, 
        database="Multimedia" 
    )

    my_cursor = my_connection.cursor()

    min_file_size = 10485760 # 10MB
    #duplicate_files = find_duplicate_files(folder_path, min_file_size)
    #orphaned_files = find_orphaned_records(folder_path, SOURCE_EXTENSIONS, my_cursor)
    orphaned_records = find_orphaned_records(folder_path, SOURCE_EXTENSIONS, my_cursor)
    print (orphaned_records)
    my_connection.commit()

    exit()

    if duplicate_files:
        print("Duplicate files found:")
        for base_name, paths in duplicate_files.items():
            print(f"File Name (ignoring extension): {base_name}")
            for path in paths:
                print(f"  - {path}")
    else:
        print("No duplicate files found.")
