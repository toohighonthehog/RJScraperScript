import re, shutil, os, ast, time
import javscraper
import rjscanmodule.rjlogging as rjlog

__all__ = ["search_for_title", "get_list_of_files", "move_up_level"]

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

def get_list_of_files(f_source_directory, f_source_extensions):
    p_folder_list_1 = os.listdir(f_source_directory)
    p_folder_list_2 = [f_source_directory + filename for filename in p_folder_list_1 if any(filename.endswith(extension) for extension in f_source_extensions)]
    p_folder_list_2.sort()

    return p_folder_list_2

def move_up_level(f_source_directory, f_target_directory, f_process_filename, f_source_extensions, f_my_logger):
    p_folder_list_1 = os.listdir(f_source_directory + f_process_filename)
    p_folder_list_2 = [filename for filename in p_folder_list_1 if any(filename.endswith(ext) for ext in f_source_extensions)]

    for p_filename in p_folder_list_2:
        p_source_filename = f_source_directory + f_process_filename + "/" + p_filename
        p_target_directory = f_source_directory + f_process_filename + "/"
        p_target_filename = f_target_directory + p_filename
        
        f_my_logger.info(rjlog.logt(f"MOV - Moving {p_filename} back a level."))
        os.makedirs(p_target_directory, exist_ok=True)
        shutil.move(p_source_filename, p_target_filename)

        return True
    
def transfer_files_by_extension(f_source_directory, f_target_directory, f_extensions, f_my_logger, f_processmode='MOVE'):
    for root, _, files in os.walk(f_source_directory):
        for filename in files:
            if any(filename.endswith(ext) for ext in f_extensions):
                p_source_filename = os.path.join(root, filename)
                f_my_logger.info(rjlog.logt(f"{f_processmode[:3]} - {filename} to {f_target_directory}."))
                if (f_processmode == "MOVE"):
                    shutil.move(p_source_filename, f_target_directory)

                if (f_processmode == "COPY"):
                    shutil.copy(p_source_filename, f_target_directory)

    return True

def prate_directory(f_source = "", f_prate = ""):
    pos_end = f_source.rfind('/')
    pos_start = f_source.rfind('/', 0, pos_end)
    p_source_folder = f_source[pos_start: pos_end + 1]
    try:
        p_prate_float = float(f_prate)
        p_prate_int = int(p_prate_float)
    except:
        p_prate_int = 0

    p_prate_str = "{0:0=2d}".format(p_prate_int)
    p_dest_folder = f"/{p_prate_str}/"
    p_target_path = f_source.replace(p_source_folder, p_dest_folder)
    if not os.path.exists(p_target_path):
        p_target_path = None

    return p_target_path