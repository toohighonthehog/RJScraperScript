import mysql.connector

if __name__ == "__main__":

    my_connection = mysql.connector.connect( 
        user="rjohnson", 
        password="5Nf%GB6r10bD", 
        host="diskstation.hachiko.int", 
        port=3306, 
        database="Test" 
    )
    
    my_cursor = my_connection.cursor()

    my_sql_delete = "DELETE FROM actor;"
    my_cursor.execute(my_sql_delete)
    my_sql_delete = "DELETE FROM genre;"
    my_cursor.execute(my_sql_delete)
    my_sql_delete = "DELETE FROM titles;"
    my_cursor.execute(my_sql_delete)
 
    
    
    my_connection.commit()
    my_cursor.close()
    
    #my_sql_delete = "DELETE FROM genre;"
    #DELETE FROM titles;

