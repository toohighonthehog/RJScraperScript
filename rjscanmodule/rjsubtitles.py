import os, shutil, time, re, requests
from requests_html import HTMLSession
import rjscanmodule.rjgeneral as rjgen
import rjscanmodule.rjlogging as rjlog

__all__ = ["get_localsubtitles", "get_subtitlecat", "get_best_subtitle"]

def get_localsubtitles(f_subtitle_general, f_subtitle_whisper, f_target_directory, f_target_language, f_process_title, f_my_logger):
    #p_process_title = f_process_title

    pass
    # fix raw whisper filename
    p_whisper_raw = f_subtitle_whisper + f_process_title + "-en Whisper-cleaned.srt"
    p_whisper_raw_fixed = p_whisper_raw.replace("-en Whisper-cleaned", "-(WH)-en")

    try:
        os.rename(p_whisper_raw, p_whisper_raw_fixed)
    except:
        pass

    if (os.path.isfile(f_subtitle_general + f_process_title + ".srt")):
        f_my_logger.info(rjlog.logt(f"SUB - Found {f_process_title}.srt in 'General'."))
        os.makedirs(f_target_directory + f_process_title, exist_ok=True)
        shutil.copy(f_subtitle_general + f_process_title + ".srt", f_target_directory + f_process_title + "/" + f_process_title + "-(LR).srt")

    if (os.path.isfile(f_subtitle_whisper + f_process_title + ".srt")):
        f_my_logger.info(rjlog.logt(f"SUB - Found {f_process_title}.srt in 'Whisper'."))
        os.makedirs(f_target_directory + f_process_title, exist_ok=True)
        shutil.copy(f_subtitle_whisper + f_process_title + ".srt", f_target_directory + f_process_title + "/" + f_process_title + "-(WH).srt")

    if (os.path.isfile(f_subtitle_whisper + f_process_title + "." + f_target_language)):
        f_my_logger.info(rjlog.logt(f"SUB - Found {f_process_title}{f_target_language} in 'Whisper'."))
        os.makedirs(f_target_directory + f_process_title, exist_ok=True)
        shutil.copy(f_subtitle_whisper + f_process_title + "." + f_target_language, f_target_directory + "/" + f_process_title + "/" + f_process_title + "-" + f_target_language)

    if (os.path.isfile(f_subtitle_whisper + f_process_title + "-(WH)-" + f_target_language)):
        f_my_logger.info(rjlog.logt(f"SUB - Found {f_process_title}-(WH)-{f_target_language} in 'Whisper'."))
        os.makedirs(f_target_directory + f_process_title, exist_ok=True)
        shutil.copy(f_subtitle_whisper + f_process_title + "-(WH)-" + f_target_language, f_target_directory + "/" + f_process_title + "/" + f_process_title + "-(WH)-" + f_target_language)

    return True

def get_subtitlecat(f_target_directory, f_target_language, f_process_title, f_my_logger):
    p_session = HTMLSession()
    p_target_directory = f_target_directory + f_process_title + "/"

    if any(filename.endswith(f_target_language) for filename in os.listdir(p_target_directory)):
        f_my_logger.debug(rjlog.logt(f_left = "SUB - Existing subtitles found."))

    f_my_logger.info(rjlog.logt(f"SUB - Searching SubtitleCat for '{f_process_title}'."))

    p_url_level1 = 'https://www.subtitlecat.com/index.php?search=' + f_process_title

    p_counter = 0
    while p_counter < 5:
        try:
            p_response_level1 = p_session.get(p_url_level1, timeout=60, allow_redirects=True)
            break
        except:
            p_counter += 1
            f_my_logger.warning(rjlog.logt(f_left = f"URL - SubtitleCat (L0) not responding.", f_right = f"{str(p_counter)}/5"))
            time.sleep(30)

    if p_counter >= 5:
        f_my_logger.critical(rjlog.logt(f_left = "URL - SubtitleCat (L0) connection failed.  Terminating."))
        exit()

    p_counter = 0
    while p_counter < 5:
        try:
            p_table_level1 = p_response_level1.html.find('table')[0]
            break
        except:
            p_counter += 1
            f_my_logger.warning(rjlog.logt(f_left = f"URL - SubtitleCat (L1) not responding.", f_right = f"{str(p_counter)}/5"))
            time.sleep(30)

    if p_counter >= 5:
        f_my_logger.critical(rjlog.logt(f_left = "URL - SubtitleCat (L1) connection failed.  Terminating."))
        exit()

    p_table_level1_entries = [[c.absolute_links for c in row.find('td')][:1] for row in p_table_level1.find('tr')][1:]

    for p_table_level1_entry in p_table_level1_entries:
        p_table_level1_entry_url = (list(p_table_level1_entry[0])[0])

        if re.search(f_process_title, p_table_level1_entry_url, re.IGNORECASE):
            p_response_level2 = p_session.get(p_table_level1_entry_url, timeout=60, allow_redirects=True)
            pass

            p_counter = 0
            while p_counter < 3:
                try:
                    p_table_level2 = p_response_level2.html.xpath('/html/body/div[4]/div/div[2]', timeout=30, first=True)
                except:
                    p_counter += 1
                    f_my_logger.warning(rjlog.logt(f_left = f"URL - SubtitleCat (L2) not responding.", f_right = f"{str(p_counter)}/3"))
                    time.sleep(5)

            if p_counter >= 3:
                f_my_logger.warning(rjlog.logt(f_left = "URL - SubtitleCat (L2) connection failed.  Skipping."))
                break

            p_table_level2 = p_response_level2.html.xpath('/html/body/div[4]/div/div[2]', first=True)
            if p_table_level2 is not None:
                for p_table_level2_entry in p_table_level2.absolute_links:
                    if re.search(f_target_language, p_table_level2_entry, re.IGNORECASE):
                        p_subtitle_url = p_table_level2_entry
                try:
                    if re.search(f_target_language, p_subtitle_url, re.IGNORECASE):
                        p_count = 0
                        while p_count < 5:
                            p_subtitle_url_check = (requests.head(p_subtitle_url).status_code)
                            p_count += 1
                            if p_subtitle_url_check == 200:
                                f_my_logger.debug(rjlog.logt(f_left = f"SUB - Subtitle_URL " + p_subtitle_url + "."))
                                if p_subtitle_url.find('/'):
                                    p_subtitle_filename = ((p_subtitle_url.rsplit('/', 1)[1]).lower())
                                f_my_logger.info(rjlog.logt(f"SUB - Downloading {p_subtitle_filename}."))
                                p_subtitle_download = requests.get(p_subtitle_url, timeout=60, allow_redirects=True)
                                p_new_subtitle_filename = re.sub(f_process_title, f_process_title.upper() + "-(SC)", p_subtitle_filename, flags=re.IGNORECASE)
                                
                                open(p_target_directory + p_new_subtitle_filename, 'wb').write(p_subtitle_download.content)
                                time.sleep(p_count)
                                break
                except:
                    pass

    return True

def get_best_subtitle(f_target_directory, f_target_language, f_process_title, f_my_logger):
    p_target_directory = f_target_directory + f_process_title + "/"
    p_filelist = rjgen.get_list_of_files(p_target_directory, ['.srt'])
    p_biggest_filesize = 0
    p_biggest_filename = ""
    p_subtitle_available = 0

    for p_filename in p_filelist:
        if os.path.getsize(p_filename) > p_biggest_filesize and p_filename.endswith(f_target_language):
            p_biggest_filename = p_filename
            p_biggest_filesize = os.path.getsize(p_filename)

        if p_filename.endswith('.srt') and p_subtitle_available < 7:
            p_subtitle_available = 7

        if p_filename.endswith('-(WH).srt') and p_subtitle_available < 8:
            p_subtitle_available = 8

        if p_filename.endswith(f_target_language):
            p_subtitle_available = 9

    if (p_biggest_filesize > 0) and not (os.path.isfile(p_target_directory + f_process_title + "-" + f_target_language)):
        f_my_logger.info(rjlog.logt(f"SUB - Creating {f_process_title}-{f_target_language} as default subtitle file."))
        shutil.copy(p_biggest_filename, (p_target_directory + f_process_title + "-" + f_target_language))

    return p_subtitle_available