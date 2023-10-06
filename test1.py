from module_rjscanfix import *
from icecream import ic
import os

my_connection = mysql.connector.connect( 
    user="rjohnson", 
    password="5Nf%GB6r10bD", 
    host="diskstation.hachiko.int", 
    port=3306, 
    database="Multimedia" 
)

def in_list(f_list, f_value):
    p_result = False
    for i in f_list:
        if f_value in i[0]:
            p_result = True

    return p_result

my_cursor = my_connection.cursor()

update_status = get_db_array(my_cursor)
ic (update_status)

ic (type(update_status))
ic (type(update_status[0]))

if (in_list(update_status, "BBAN-442")):
    print ("True")
else:
    print ("False")