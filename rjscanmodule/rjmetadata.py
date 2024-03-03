import javscraper
import rjscanmodule.rjlogging as rjlog

__all__ = ["download_metadata"]

def download_metadata(f_process_title, f_my_logger, f_attribute_override = None):
    ############## xxx
    ### need to check that, if f_attribute_override is set, try that first.
    p_my_javlibrary = javscraper.JAVLibrary()
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