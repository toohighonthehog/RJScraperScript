from module_rjscanfix import *
from javscraper import *
import os
import mysql.connector

my_connection = mysql.connector.connect(
    user="rjohnson",
    password="5Nf%GB6r10bD",
    host="diskstation.hachiko.int",
    port=3306,
    database="Multimedia"
)

my_cursor = my_connection.cursor()
output = ""

os.system('clear')

columns = (os.get_terminal_size().columns - 20)
count = 50
prefix = "DOCP"
skip_got = False
p_my_javlibrary = JAVLibrary()
substrings = [""]

while count < 100:
    count = count + 1
    title = prefix + "{0:0=3d}".format(count)
    try:
        object_result = p_my_javlibrary.get_video(title)
    except:
        object_result = False
        pass
    print(title, end="\r")

    if object_result:
        if all(sub in object_result.name.lower() for sub in substrings):
            if (fix_file_code(object_result.code, '')) == title:
                my_sql_query = "SELECT * from title WHERE code = '" + \
                    fix_file_code(title) + "'"
                my_cursor.execute(my_sql_query)
                try:
                    rows = my_cursor.fetchone()
                except:
                    rows = None

                if rows == None or (skip_got == False):
                    if len(object_result.name) > columns:
                        print(f"{title}     : {object_result.name[:columns]}")
                        print(
                            f"{(len(title) + 5 ) * ' '}  {object_result.name[columns:]}")
                    else:
                        print(f"{title}     : {object_result.name}")

                    object_url = p_my_javlibrary.search(title)
                    print(f"{title.lower()}.xxx > {object_url}")
                    output = output + "touch " + title.lower() + ".xxx\n"
                    print("-" * (columns + 13))
                else:
                    print("\r")

print(output)

my_cursor.close()
my_connection.disconnect()
