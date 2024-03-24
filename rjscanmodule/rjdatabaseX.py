import hashlib, json
import rjscanmodule.rjlogging as rjlog
#from rjlogging import *

__all__ = ["send_to_database", "send_to_json", "get_db_array", "get_db_title_record", "update_db_title_record"]

def send_to_database(f_metadata_array, f_my_logger, f_my_cursor):
    # if net new 'INSERT', if not, 'UPDATE' - if update, leave prate as is.
    p_my_insert_sql_title = "\
        INSERT INTO title (\
            name, \
            studio, \
            image, \
            score, \
            release_date, \
            added_date, \
            file_date, \
            location, \
            subtitles, \
            prate, \
            notes, \
            status, \
            code) \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

    p_my_insert_sql_title_u = "\
        UPDATE title SET \
            name = %s, \
            studio = %s, \
            image = %s, \
            score = %s, \
            release_date = %s, \
            added_date = %s, \
            file_date = %s, \
            location = %s, \
            subtitles = %s, \
            prate = %s, \
            notes = %s, \
            status = %s \
            WHERE code = %s;"

    p_my_insert_sql_genre = "\
        INSERT IGNORE INTO genre \
            (description) VALUES (%s);"

    # should we be using IGNORE so much here?
    p_my_insert_sql_genre_title_link = "\
        INSERT INTO genre_title_link \
            (genre_g_id, \
            title_code, \
            guid ) VALUES (%s, %s, %s) \
        ON DUPLICATE KEY UPDATE \
            genre_g_id = values(genre_g_id), \
            title_code = values(title_code), \
            guid = values(guid);"

    p_my_insert_sql_url = "\
        INSERT INTO url \
            (title_code, \
            url, \
            guid) VALUES (%s, %s, %s) \
        ON DUPLICATE KEY UPDATE \
            url = values(url), \
            guid = values(guid);"

    p_my_insert_sql_actor = "\
        INSERT IGNORE INTO actor \
            (name) VALUES (%s);"

    p_my_insert_sql_actor_title_link = "\
        INSERT INTO actor_title_link \
            (actor_a_id, \
            title_code, \
            guid ) VALUES (%s, %s, %s) \
        ON DUPLICATE KEY UPDATE \
            actor_a_id = values(actor_a_id), \
            title_code = values(title_code), \
            guid = values(guid);"

    f_my_cursor.execute(f"SELECT * FROM title WHERE code = '{f_metadata_array['code']}';")
    p_my_results = f_my_cursor.fetchone()

    if (p_my_results):
        f_my_logger.info(rjlog.logt(f"MET - Write updated metadata for '{f_metadata_array['code']}' to database."))
        p_my_insert_sql_title = p_my_insert_sql_title_u
        # the columns we retain when updating a title.
        f_prate = p_my_results['prate']
        f_added_date = p_my_results['added_date']
        f_notes = p_my_results['notes']
        f_location = f_metadata_array['location']

    else:
        f_my_logger.info(rjlog.logt(f"MET - Write new metadata for '{f_metadata_array['code']}' to database."))
        f_prate = f_metadata_array['prate']
        f_added_date = f_metadata_array['added_date']
        f_notes = f_metadata_array['notes']
        f_location = f_metadata_array['location']

    try:
        f_location = f_location.replace("/mnt", "file://diskstation")
    except:
        f_location = ''

    f_my_cursor.execute(p_my_insert_sql_title,
                        (f_metadata_array['name'],
                         f_metadata_array['studio'],
                         f_metadata_array['image'],
                         f_metadata_array['score'],
                         f_metadata_array['release_date'],
                         f_added_date,
                         f_metadata_array['file_date'],
                         f_location,
                         f_metadata_array['subtitles'],
                         f_prate,
                         f_notes,
                         f_metadata_array['status'],
                         f_metadata_array['code']))

    if f_metadata_array['actor']:
        for a in f_metadata_array['actor']:
            p_my_query_sql_actor = f"SELECT a_id FROM actor WHERE name = '{a}';"
            f_my_cursor.execute(p_my_query_sql_actor)
            p_my_results = f_my_cursor.fetchone()

            if p_my_results is None:
                f_my_cursor.execute(p_my_insert_sql_actor, (a,))
                p_a_id = f_my_cursor.lastrowid
            else:
                p_a_id = p_my_results['a_id']

            p_hash_input = (
                f_metadata_array['code'] + str(p_a_id) + "actor_title_link").encode()
            p_hash_output = hashlib.sha1(p_hash_input).hexdigest()
            f_my_cursor.execute(p_my_insert_sql_actor_title_link,
                                (p_a_id,
                                f_metadata_array['code'],
                                p_hash_output))

    if f_metadata_array['genre']:
        for g in f_metadata_array['genre']:
            p_my_query_sql_genre = "SELECT g_id FROM genre WHERE description = '" + g + "';"
            f_my_cursor.execute(p_my_query_sql_genre)
            p_my_results = f_my_cursor.fetchone()

            if p_my_results is None:
                f_my_cursor.execute(p_my_insert_sql_genre, (g,))
                p_g_id = f_my_cursor.lastrowid
            else:
                p_g_id = p_my_results['g_id']

            p_hash_input = (
                f_metadata_array['code'] + str(p_g_id) + "genre_title_link").encode()
            p_hash_output = hashlib.sha1(p_hash_input).hexdigest()
            f_my_cursor.execute(p_my_insert_sql_genre_title_link,
                                (p_g_id, f_metadata_array['code'], p_hash_output))

    if f_metadata_array['url']:
        for u in f_metadata_array['url']:
            p_hash_input = (f_metadata_array['code'] + u).encode()
            p_hash_output = hashlib.md5(p_hash_input).hexdigest()
            f_my_cursor.execute(p_my_insert_sql_url, (f_metadata_array['code'], u, p_hash_output))

    return True

def send_to_json(f_metadata_array, f_my_logger, f_json_filename):
    f_my_logger.info(rjlog.logt(f"MET - Write metadata for '{f_metadata_array['code']}' to json."))

    try:
        p_location = f_metadata_array['location'].replace("/mnt", "file://diskstation")
    except:
        p_location = ''

    p_metadata_json_array = {"code": f_metadata_array['code'],
                             "name": f_metadata_array['name'],
                             "actor": f_metadata_array['actor'],
                             "studio": f_metadata_array['studio'],
                             "image": f_metadata_array['image'],
                             "genre": f_metadata_array['genre'],
                             "url": f_metadata_array['url'],
                             "score": f_metadata_array['score'],
                             "release_date": f_metadata_array['release_date'],
                             "location": p_location}

    p_metadata_json = json.dumps(p_metadata_json_array, indent=4)
    with open(f_json_filename, "w") as outfile:
        outfile.write(p_metadata_json)

def get_db_array(f_my_cursor, f_db_query):
    p_my_sql_query = f"SELECT \
        code, \
        ifnull(name,'') as name, \
        ifnull(studio,'') as studio, \
        ifnull(image,'') as image, \
        ifnull(score,'') as score, \
        ifnull(release_date,'') as release_date, \
        ifnull(added_date,'') as added_date, \
        ifnull(file_date,'') as file_date, \
        ifnull(location,'') as location, \
        ifnull(subtitles,'') as subtitles, \
        ifnull(prate,'') as prate, \
        ifnull(notes,'') as notes, \
        ifnull(status,'') as status \
        FROM title {f_db_query} ORDER BY code"
    #p_my_sql_query = f"SELECT * FROM title {f_db_query} ORDER BY code"

    f_my_cursor.execute(p_my_sql_query)
    p_results = f_my_cursor.fetchall()
    return p_results

def get_db_title_record(f_my_cursor, f_process_filename):
    p_my_sql_query = "SELECT * FROM title WHERE code='" + f_process_filename + "'"
    f_my_cursor.execute(p_my_sql_query)

    p_result = f_my_cursor.fetchone()
    return p_result

def update_db_title_record(f_my_cursor, f_db_record):
    p_my_insert_sql_title = "\
        UPDATE title SET \
            name = %s, \
            studio = %s, \
            image = %s, \
            score = %s, \
            release_date = %s, \
            added_date = %s, \
            file_date = %s, \
            location = %s, \
            subtitles = %s, \
            prate = %s, \
            notes = %s, \
            status = %s \
            WHERE code = %s;"

    f_my_cursor.execute(p_my_insert_sql_title,
                        (f_db_record['name'],
                         f_db_record['studio'],
                         f_db_record['image'],
                         f_db_record['score'],
                         f_db_record['release_date'],
                         f_db_record['added_date'],
                         f_db_record['file_date'],
                         f_db_record['location'],
                         f_db_record['subtitles'],
                         f_db_record['prate'],
                         f_db_record['notes'],
                         f_db_record['status'],
                         f_db_record['code']))