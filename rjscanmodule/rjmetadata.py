import javscraper, ast, time, re
import rjscanmodule.rjlogging as rjlog

__all__ = ["download_metadata", "new_search_title"]

def download_metadata(f_process_title, f_my_logger, f_short_results = False):
    with open("cookie.json", "r") as data:
        cookie = ast.literal_eval(data.read())
    p_my_javlibrary = javscraper.JAVLibrary()
    p_my_javlibrary.debug = False
    p_my_javlibrary._set_cookies(cookie)
    
    p_metadata_array = []

    #f_my_logger.info(rjlog.logt(f"MET - Searching web for '{f_process_title}'."))
    p_metadata_url = p_my_javlibrary.search(f_process_title)
    pass
    if p_metadata_url:
        if f_short_results == False:
            p_metadata = p_my_javlibrary.get_video(f_process_title)
            f_my_logger.info(rjlog.logt(f"MET - Metadata downloaded for '{f_process_title}'."))
            p_metadata_array = {
                "code": p_metadata.code,
                "name": p_metadata.name,
                "actor": p_metadata.actresses,
                "studio": p_metadata.studio,
                "image": p_metadata.image,
                "genre": p_metadata.genres,
                "url": p_metadata_url,
                "score": p_metadata.score,
                "release_date": (p_metadata.release_date).strftime("%Y-%m-%d"),
                "added_date": None,
                "file_date": None,
                "notes": None,
                "location": None,
                "subtitles": None,
                "prate": None,
                "status": None
                }
            
        if f_short_results == True:
            f_my_logger.info(rjlog.logt(f"MET - Metadata found for '{f_process_title}'."))
            p_metadata = True
            p_metadata_array = {
                "code": f_process_title,
                "name": None,
                "actor": None,
                "studio": None,
                "image": None,
                "genre": None,
                "url": p_metadata_url,
                "score": None,
                "release_date": None,
                "added_date": None,
                "file_date": None,
                "notes": None,
                "location": None,
                "subtitles": None,
                "prate": None,
                "status": None
                }
    else:
        f_my_logger.warning(rjlog.logt(f"MET - No metadata found for '{f_process_title}'."))
        p_metadata_array = {
            "code": f_process_title,
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
            "status": None
            }
        
    time.sleep(5)

    return p_metadata_array

# def search_for_title(f_input_string, f_javli_override = None):
#     print (f"fis: {f_input_string}")
#     with open("cookie.json", "r") as data:
#         cookie = ast.literal_eval(data.read())
#     p_my_javlibrary = javscraper.JAVLibrary()
#     p_my_javlibrary._set_cookies(cookie)

#     if f_javli_override:
#         if f_javli_override[:3] == 'jav':
#             p_get_video = p_my_javlibrary.get_video(f_javli_override)
#             time.sleep(5)
#             ### if a value result is returned, return f_input_string, 1
#             ### if not, just keep going.          
#             #print (f"crap: {p_get_video}")
#             if p_get_video:
#                 #print (f"Override: {f_input_string}")
#                 #print (p_get_video)
#                 return f_input_string, 1
    
#     p_valid = r'([A-Z]){3,}[0-9]{3,}([A-Z])'
#     p_strict_valid = r'^([A-Z]{3,5})(\d{3})Z$'
#     p_input_string = f_input_string.upper()
#     p_input_string = re.sub(r'[^A-Z0-9]', '', p_input_string)
#     print (f"pis: {p_input_string}")
#     p_input_string += "Z"

#     p_strict_match = (re.match(p_strict_valid, p_input_string))
#     p_strict_matched_value = None
#     if p_strict_match:
#         p_strict_matched_value = p_strict_match.group(1) + '-' + p_strict_match.group(2)

#     p_substrings = set()
#     for p_loop in range(len(p_input_string)):
#         p_substring = p_input_string[p_loop:]
#         if re.match(p_valid, p_substring):
#             p_matched_value = (re.match(p_valid, p_substring)).group()
#             p_matched_value = p_matched_value[:-1]
#             print (f"pmv: {p_matched_value}")
#             p_get_video = p_my_javlibrary.get_video(p_matched_value)
#             time.sleep(5)
#             if (p_get_video):
#                 p_substrings.add(p_get_video.code)
#                 #print (p_get_video.code)

#     #p_result = p_strict_matched_value
#     p_result_count = (len(p_substrings))

#     if p_result_count == 1:
#         p_result = list(p_substrings)[0]

#     if p_result_count > 1:
#         if f_input_string in p_substrings:
#             p_result = f_input_string
#             p_result_count = 1
#         else:
#             p_result = None
#             p_result_count = -p_result_count

#     if p_result_count == 0:
#         p_result = p_strict_matched_value
#         p_result_count = 0
#         if p_strict_matched_value is None:
#             p_result_count = -255

#     pass

#     return p_result, p_result_count

def new_search_title(f_input_string, f_my_logger, f_attribute_override = None):
    f_my_logger.info(rjlog.logt(f"MET - Processing '{f_input_string}'."))
    if f_attribute_override is None:
        p_input_string = f_input_string
        p_valid = r'[A-Z]{3,}[0-9]{3,}[^0-9]{1}'
        #p_input_string =  p_input_string.upper() + "Z"
        p_input_string = re.sub(r'[-]', '', p_input_string.upper()) + "Z"
        #print (p_input_string)
        #p_input_string = re.sub(r'[^A-Z0-9]', '', p_input_string.upper()) + "Z"
        # re.sub(r'[^A-Z0-9]', '',
        p_substrings = set()
        for p_loop in range(len(p_input_string)):
            p_substring = p_input_string[p_loop:]
            
            if re.match(p_valid, p_substring):
                #print (p_substring)
                p_matched_value = (re.match(p_valid, p_substring)).group()
                p_matched_value = p_matched_value[:-1]
                #print (p_matched_value)
                p_matched_value_split = (re.split('(\d+)', p_matched_value))
                p_matched_value_hyphen = (f"{p_matched_value_split[0]}-{p_matched_value_split[1]}")
                #print (p_matched_value_hyphen)
                p_substrings.add(p_matched_value_hyphen)
        p_substrings_dd = []
        for item in p_substrings:
            is_substring = False
            for other_item in p_substrings:
                if item != other_item:
                    if item in other_item:
                        is_substring = True
                        break
            if not is_substring:
                p_substrings_dd.append(item)
    else:
        p_substrings_dd = [f_attribute_override]

    #print (f"psdd: {p_substrings_dd}")
    p_substrings_count = len(p_substrings_dd)
    if p_substrings_count == 1:
        p_metadata_array = download_metadata(p_substrings_dd[0], f_my_logger)
        if p_metadata_array["name"]:
            p_substrings_dd = [p_metadata_array["code"]]
        else:
            p_substrings_count = 0
    
    if p_substrings_count > 1:
        f_my_logger.warning(rjlog.logt(f"MET - Multiple {p_substrings_dd} ({p_substrings_count})."))
        p_multi_count = 0
        p_multi_result = ""
        for p_multi_item in p_substrings_dd:
            pass
            if p_multi_count > 1:
                break
            p_multi_array = download_metadata(p_multi_item, f_my_logger, True)
            if p_multi_array["url"]:
                p_multi_result = p_multi_array["code"]
                p_multi_count += 1

        # print (p_multi_count)
        if p_multi_count == 1:
            p_metadata_array = download_metadata(p_multi_result, f_my_logger)
            p_substrings_dd = p_substrings_dd = [p_metadata_array["code"]]
            p_substrings_count = 1
        else:
            p_metadata_array = None
       
    return p_substrings_dd, p_substrings_count, p_metadata_array