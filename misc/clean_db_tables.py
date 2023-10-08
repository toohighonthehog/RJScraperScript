import mysql.connector

if __name__ == "__main__":

    my_connection = mysql.connector.connect( 
        user="rjohnson", 
        password="5Nf%GB6r10bD", 
        host="diskstation.hachiko.int", 
        port=3306, 
        database="Multimedia_Dev"
    )
    
    my_cursor = my_connection.cursor()

    my_sql_delete = "DELETE FROM actor;"
    my_cursor.execute(my_sql_delete)
    my_sql_delete = "DELETE FROM actor_link;"
    my_cursor.execute(my_sql_delete)
    my_sql_delete = "DELETE FROM genre;"
    my_cursor.execute(my_sql_delete)
    my_sql_delete = "DELETE FROM title;"
    my_cursor.execute(my_sql_delete)
    my_sql_delete = "DELETE FROM url;"
    my_cursor.execute(my_sql_delete)

    my_connection.commit()
    my_cursor.close()
