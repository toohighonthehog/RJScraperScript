import os
#SOURCE_DIRECTORY = "/mnt/multimedia/Other/RatedFinalJ/Censored/General/"
SOURCE_DIRECTORY = "/home/rjohnson/vscode/git/RJScraperScript/misc/General/"
prate = "General"

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

print (prate_directory(SOURCE_DIRECTORY, prate))