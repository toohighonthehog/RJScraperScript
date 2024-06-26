import javscraper, ast, time, re
import rjscanmodule.rjlogging as rjlog

__all__ = ["download_metadata", "search_for_title"]

def download_metadata(f_process_title, f_my_logger, f_attribute_override = None):
    ############## xxx
    ### need to check that, if f_attribute_override is set, try that first.
    with open("cookie.json", "r") as data:
        cookie = ast.literal_eval(data.read())
    p_my_javlibrary = javscraper.JAVLibrary()
    p_my_javlibrary._set_cookies(cookie)
    
    #p_process_title = f_process_title
    p_metadata_array = []

    if f_attribute_override:
        p_metadata = p_my_javlibrary.get_video(f_attribute_override)
        p_metadata_url = p_my_javlibrary.search(f_attribute_override)
        f_string_override = f" (xcode: {f_attribute_override})"
    else:
        p_metadata = p_my_javlibrary.get_video(f_process_title)
        p_metadata_url = p_my_javlibrary.search(f_process_title)
        f_string_override = ""
    time.sleep(5)

    f_my_logger.info(rjlog.logt(f"MET - Searching web for '{f_process_title}' metadata.{f_string_override}"))

    if p_metadata is not None:
        p_release_date = (p_metadata.release_date).strftime("%Y-%m-%d")

        f_my_logger.info(rjlog.logt(f"MET - Metadata downloaded for '{f_process_title}'."))

        p_metadata_array = {"code": p_metadata.code,
                            "name": p_metadata.name,
                            "actor": p_metadata.actresses,
                            "studio": p_metadata.studio,
                            "image": p_metadata.image,
                            "genre": p_metadata.genres,
                            "url": p_metadata_url,
                            "score": p_metadata.score,
                            "release_date": p_release_date,
                            "added_date": None,
                            "file_date": None,
                            "notes": None,
                            "location": None,
                            "subtitles": None,
                            "prate": None,
                            "status": None}
    else:
        # does this ever get called?
        f_my_logger.info(rjlog.logt(f"MET - No metadata found for '{f_process_title}'."))
        p_metadata_array = {"code": f_process_title,
                            "name": None,
                            "actor": None,
                            "studio": None,
                            "image": None,
                            "genre": None,
                            "url": None,
                            "score": None,
                            "release_date": None,
                            "added_date": None,
                            "file_date": None,
                            "notes": None,
                            "location": None,
                            "subtitles": None,
                            "prate": None,
                            "status": None}

    return p_metadata_array

def search_for_title(f_input_string, f_javli_override = None):
    with open("cookie.json", "r") as data:
        cookie = ast.literal_eval(data.read())
    p_my_javlibrary = javscraper.JAVLibrary()
    p_my_javlibrary._set_cookies(cookie)

    if f_javli_override:
        if f_javli_override[:3] == 'jav':
            p_get_video = p_my_javlibrary.get_video(f_javli_override)
            time.sleep(5)
            ### if a value result is returned, return f_input_string, 1
            ### if not, just keep going.          
            #print (f"crap: {p_get_video}")
            if p_get_video:
                #print (f"Override: {f_input_string}")
                #print (p_get_video)
                return f_input_string, 1
    
    p_valid = r'([A-Z]){3,}[0-9]{3,}([A-Z])'
    p_strict_valid = r'^([A-Z]{3,5})(\d{3})Z$'
    p_input_string = f_input_string.upper()
    p_input_string = re.sub(r'[^A-Z0-9]', '', p_input_string)
    p_input_string += "Z"

    p_strict_match = (re.match(p_strict_valid, p_input_string))
    p_strict_matched_value = None
    if p_strict_match:
        p_strict_matched_value = p_strict_match.group(1) + '-' + p_strict_match.group(2)

    p_substrings = set()
    for p_loop in range(len(p_input_string)):
        p_substring = p_input_string[p_loop:]
        if re.match(p_valid, p_substring):
            p_matched_value = (re.match(p_valid, p_substring)).group()
            p_matched_value = p_matched_value[:-1]
            p_get_video = p_my_javlibrary.get_video(p_matched_value)
            if (p_get_video):
                p_substrings.add(p_get_video.code)
                #print (p_get_video.code)

    #p_result = p_strict_matched_value
    p_result_count = (len(p_substrings))

    if p_result_count == 1:
        p_result = list(p_substrings)[0]

    if p_result_count > 1:
        if f_input_string in p_substrings:
            p_result = f_input_string
            p_result_count = 1
        else:
            p_result = None
            p_result_count = -p_result_count

    if p_result_count == 0:
        p_result = p_strict_matched_value
        p_result_count = 0
        if p_strict_matched_value is None:
            p_result_count = -255

    pass

    return p_result, p_result_count