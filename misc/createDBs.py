import mysql.connector

if __name__ == "__main__":

    db_name="MultimediaShare"

    my_connection = mysql.connector.connect(
        user="rjohnson",
        password="5Nf%GB6r10bD",
        host="diskstation.hachiko.int",
        port=3306,
    )

    my_cursor = my_connection.cursor()

    my_sql_create = f"DROP DATABASE IF EXISTS {db_name};"
    my_cursor.execute(my_sql_create)

    my_sql_create = f"CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;"
    my_cursor.execute(my_sql_create)

    my_sql_create = f"USE {db_name};"
    my_cursor.execute(my_sql_create)

    my_sql_create = (f"CREATE TABLE title (" \
    	f"code varchar(20), " \
    	f"name varchar(500), " \
    	f"studio varchar(100), " \
    	f"image varchar(100), " \
    	f"score decimal(3,1), " \
    	f"release_date datetime, " \
        f"added_date datetime, " \
	    f"file_date datetime, " \
	    f"location varchar(100), " \
	    f"subtitles integer UNSIGNED, " \
	    f"prate integer, " \
	    f"notes varchar(1000), " \
	    f"status integer UNSIGNED, " \
	    f"t_id integer NOT NULL AUTO_INCREMENT, " \
	    f"PRIMARY KEY (code), " \
	    f"UNIQUE (t_id));")
    my_cursor.execute(my_sql_create)

    my_sql_create = (f"CREATE TABLE actor (" \
        f"name varchar(100)," \
        f"notes varchar(1000)," \
        f"prate int," \
        f"a_id int NOT NULL AUTO_INCREMENT," \
        f"PRIMARY KEY (a_id));")
    my_cursor.execute(my_sql_create)

    my_sql_create = (f"CREATE TABLE genre (" \
        f"description varchar(100)," \
        f"notes varchar(1000)," \
        f"prate int," \
        f"g_id int NOT NULL AUTO_INCREMENT," \
        f"PRIMARY KEY (g_id));")
    my_cursor.execute(my_sql_create)

    my_sql_create = (f"CREATE TABLE actor_title_link (" \
        f"actor_a_id int," \
        f"title_code varchar(20)," \
        f"guid varchar(40)," \
        f"PRIMARY KEY (guid)," \
        f"FOREIGN KEY (actor_a_id) REFERENCES actor(a_id) ON DELETE NO ACTION ON UPDATE NO ACTION," \
        f"FOREIGN KEY (title_code) REFERENCES title(code) ON DELETE NO ACTION ON UPDATE NO ACTION);")
    my_cursor.execute(my_sql_create)

    my_sql_create = (f"CREATE TABLE genre_title_link (" \
        f"genre_g_id int," \
        f"title_code varchar(20)," \
        f"guid varchar(40)," \
        f"PRIMARY KEY (guid)," \
        f"FOREIGN KEY (genre_g_id) REFERENCES genre(g_id) ON DELETE NO ACTION ON UPDATE NO ACTION," \
        f"FOREIGN KEY (title_code) REFERENCES title(code) ON DELETE NO ACTION ON UPDATE NO ACTION);")
    my_cursor.execute(my_sql_create)

    my_sql_create = (f"CREATE TABLE url (" \
        f"title_code varchar(20)," \
        f"url varchar(100)," \
        f"guid varchar(40)," \
        f"PRIMARY KEY (guid)," \
        f"FOREIGN KEY (title_code) REFERENCES title(code) ON DELETE NO ACTION ON UPDATE NO ACTION);")
    my_cursor.execute(my_sql_create)

    my_sql_create = f"ALTER TABLE actor AUTO_INCREMENT = 1296"
    my_cursor.execute(my_sql_create)
    my_sql_create = f"ALTER TABLE genre AUTO_INCREMENT = 1296"
    my_cursor.execute(my_sql_create)
    my_sql_create = f"ALTER TABLE title AUTO_INCREMENT = 1296"
    my_cursor.execute(my_sql_create)




    my_cursor.close()