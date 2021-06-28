# Main module

import html_parser as hp
import create_image_utils as iu
import upload_pic as up
from pathlib import Path
import insta_data_logger as ig_log
import errno
import os
import timeit
from datetime import datetime
import dateutil.parser
import locale
        
from kivy.app import App
from kivy.uix.button import Button

batch_log_book = Path.cwd().parent / "data" / "last_batch.txt"
path_to_json_folder = (Path.cwd().parent / "data" / "tumblr_all" / "txt")
path_to_figs = (Path.cwd().parent / "fig")

def batch_prepare_posts(num_posts = 100):
    # Choose posts randomly from the list of json files present on the disk and log them into the batch_log_book
    # and create all pictures related to this batch post, to allow the user to check all the pics manually before posting them in batch
    # If a picture is not good, its entry will be removed manually from the batch_log_book
    batch_flush()
    json_files = batch_get_new_file_list(num_posts)
    
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

def batch_get_new_file_list(num_files):
    import random 
    
    global path_to_json_folder
    
    # Generate a list of JSON files to pickup from
    # The method outputs a list of files available for posting, i.e. files not contained in the log_book.txt file
    p = path_to_json_folder.glob("*.json")
    all_files = [x for x in p if x.is_file()]
    past_entries = ig_log.reset_log_entries_read_logbook()
    
    available_files = [f for f in all_files if not ig_log.string_is_in_list(f.stem, past_entries)]
    available_files_index_list = random.sample(range(0, len(available_files)), num_files)
    
    output_file_list = [available_files[a] for a in available_files_index_list]
    
    return output_file_list

def batch_upload(upload_files = True):
    # Upload all posts indicated in the batch_log_book file
    # The upload_files flag allows to log only (debugging)
    
    with open(str(batch_log_book), "r") as f:
        selected_posts_id = f.read().splitlines()
        
    for s in selected_posts_id:
        path_to_fig = (path_to_figs / s).with_suffix(".png")
        path_to_json = (path_to_json_folder / s).with_suffix(".json")
        
        if(not path_to_fig.is_file()):
            raise FileNotFoundError(errno.ENOENT, 
                                os.strerror(errno.ENOENT), 
                                path_to_fig)
            
        if(ig_log.is_log_entry(path_to_json)):
            raise Exception("Files already uploaded. Please prepare new files.")
            
        # Get current quote's hashtags in corresponding json
        current_quote = hp.read_dict_from_file(path_to_json)
        
        # Post picture and log
        if(upload_files):
            up.ig_post_picture(path_to_fig, current_quote)
        ig_log.log_post(path_to_json)
        
def batch_regenerate_figs():
    # Take the post IDs contained in the batch log book last entries, 
    # and regenerate pics (e.g. in case of text corrections)
    with open(str(batch_log_book), "r") as f:
        selected_posts_id = f.read().splitlines()
        
    for s in selected_posts_id:
        path_to_json = (path_to_json_folder / s).with_suffix(".json")
        
        current_quote = hp.read_dict_from_file(path_to_json)
        iu.create_image_from_txt(current_quote["quote"], 
                              text_font_size = 75, 
                              save_to_file = True, 
                              filename = path_to_json.stem)
        
def post_quote(quote, hashtags, upload_file = True):
    filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png"
    date = datetime.now().strftime("%Y-%m-%d")
    
    iu.create_image_from_txt(quote, 
                            text_font_size = 75, 
                            save_to_file = True, 
                            filename = filename)
    locales = ['fr']
    loc = locales[0]
    locale.setlocale(locale.LC_ALL, loc) # change to French
    date_obj = dateutil.parser.parse(date) 
    
    output_date = date_obj.strftime("%A %d %B %Y").capitalize()

    if(upload_file):
        path = Path.cwd().parent / "fig"
        current_quote = {
        'quote' : quote, 
        'hashtags' : hashtags, 
        'date' : output_date
        }
        up.ig_post_picture(path / filename, current_quote)

class TextToInstaApp(App):
    def build(self):
        return Button()

    def on_press_button(self):
        print('You pressed the button!')

if __name__ == '__main__':
    # app = TextToInstaApp()
    # app.run()

# if __name__ == "__main__":
    # num_posts = 3
#     # print(batch_get_new_file_list(10))
    # batch_flush()
    
#     #%% Step 1: Prepare posts
    # batch_prepare_posts(num_posts)
    
#     #%% Optional - to do if there are adjustments to pics to be made
    # batch_regenerate_figs()
    
#     #%% Step 2: Upload all pics
#     start_time = timeit.default_timer()
    # batch_upload(upload_files = True)
#     print("Elapsed time: " + str(timeit.default_timer() - start_time) + " seconds")

#%% Direct post text
    quote = "Mbappé sait lacer ses chaussures et compter deux par deux."
    hashtags = ["apprenti", "joueur"]
    post_quote(quote, hashtags, upload_file = True)