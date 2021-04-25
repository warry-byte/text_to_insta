# Main module

import html_parser as hp
import create_image_utils as iu
import upload_pic as up
from pathlib import Path
import insta_data_logger as ig_log

batch_log_book = Path.cwd().parent / "data" / "last_batch.txt"
path_to_json = (Path.cwd().parent / "data" / "tumblr_all" / "txt")
path_to_figs = (Path.cwd().parent / "fig")

def batch_prepare_posts(num_posts = 100):
    # Choose posts randomly from the list of json files present on the disk and log them into the batch_log_book
    # and create all pictures related to this batch post, to allow the user to check all the pics manually before posting them in batch
    # If a picture is not good, its entry will be removed manually from the batch_log_book
    batch_flush()
    json_files = batch_get_file_list(num_posts)
    
    # Log pictures in list of posts
    with open(str(batch_log_book), "a") as f:
    
        for j in json_files:
            current_quote = hp.read_dict_from_file(j)
            iu.create_image_from_txt(current_quote["quote"], 
                                  text_font_size = 75, 
                                  save_to_file = True, 
                                  filename = j.stem)
            f.write(str(j.stem) + "\n") # Write quote file name in log book
            
def batch_flush(delete_figs = True):
    # Empty batch log file
    with open(str(batch_log_book), "w") as f:
        f.write("")
        
    if(delete_figs):
        all_figs = path_to_figs.glob("*.png")
        for a in all_figs:
            a.unlink()

def batch_get_file_list(num_files):
    import random 
    
    global path_to_json
    
    # Generate a list of JSON files to pickup from
    # The method outputs a list of files available for posting, i.e. files not contained in the log_book.txt file
    p = path_to_json.glob("*.json")
    all_files = [x for x in p if x.is_file()]
    past_entries = ig_log.reset_log_entries_read_logbook()
    
    available_files = [f for f in all_files if not ig_log.string_is_in_list(f.stem, past_entries)]
    available_files_index_list = random.sample(range(0, len(available_files)), num_files)
    
    output_file_list = [available_files[a] for a in available_files_index_list]
    
    return output_file_list
    
    
if __name__ == "__main__":
    # print(batch_get_file_list(10))
    # batch_prepare_posts(10)
    # batch_flush()