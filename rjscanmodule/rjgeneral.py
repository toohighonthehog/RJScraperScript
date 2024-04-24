import shutil, os, ast, time
import rjscanmodule.rjlogging as rjlog

__all__ = ["search_for_title", "get_list_of_files", "move_up_level"]

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