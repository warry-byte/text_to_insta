# Handling meta data of insta account such as list of posts, etc
# We differentiate between logbook (i.e. file physically present on the disk) and log entries (RAM)

# To limit file accesses, the log book file is only accessed when an entry has been added

# TODO class style accessing

from pathlib import Path
import datetime
import errno
import os

log_book = Path.cwd().parent / "data" / "logbook.txt"
log_entries = None # image of the log_book file

def log_post(path_to_json):
    # Throws an error if the post is not in the list of posts
    # Returns False if the post (= JSON file name) is in the logbook
    
    global log_entries
    
    success = False
    
    # ensure that the variable is an instance of Path
    path_to_json = Path(path_to_json) 
    
    if(path_to_json.is_file() == False):
        print("Data error: JSON File not present.")
        raise FileNotFoundError(errno.ENOENT, 
                                os.strerror(errno.ENOENT), 
                                path_to_json)
    
    # update log entries if not done already - TODO move to constructor
    if(log_entries == None):
        log_entries = reset_log_entries_read_logbook()
        
        
    if(is_log_entry(path_to_json) == False): # update log book
        # Create log entry
        log_entry = str(path_to_json.stem + "    " + str(datetime.datetime.now())) 
        
        # Log picture in list of posts
        with open(str(log_book), "a") as f:
            f.write(log_entry + "\n") # Create a new line: write at the end of the file
                        
        log_entries.append(log_entry)
        
        success = True
    else:
        success = False
        
    return success
        
def reset_log_entries_read_logbook():
    # Read logbook and populate log entries list
    global log_entries
    
    with open(str(log_book), "r") as f:
        log_entries = f.readlines()
        
    return log_entries

        
def is_log_entry(path_to_json):
    # Ensure that we read the logbook file once
    global log_entries
    
    entry_found = False
    
    # ensure that variable is an instance of Path
    path_to_json = Path(path_to_json) 
    
    if(log_entries == None):
        reset_log_entries_read_logbook() # populate log_entries list
    
    # Check if filename is in the log_entries list
    if(string_is_in_list(str(path_to_json.stem), log_entries)):
        entry_found = True
        
    return entry_found

def string_is_in_list(_string, log_entries):
    # Lower-level function: check if a string is contained somewhere in a list of strings
    # Reference: https://stackoverflow.com/questions/4843158/check-if-a-python-list-item-contains-a-string-inside-another-string
    entry_found = False
    
    if any(_string in s for s in log_entries):
            entry_found = True
            
    return entry_found
        
if __name__ == "__main__":
    
    def test_file_logging(post):
        s = log_post(post)
        if(s):
            print("File logged succesfully")
        else:
            print("Nique ta mère")
            
    current_path = Path.cwd()
    path_to_tumblr_posts = current_path.parent / "data" / "tumblr_all" / "html"
    test_files = [path_to_tumblr_posts / "110348424618.html", 
                  path_to_tumblr_posts / "72327713057.html",
                  path_to_tumblr_posts / "CUL.html"]
    
    for t in test_files:
        test_file_logging(t)
    