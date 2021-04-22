# Parse all HTML files and save them in the data\tumblr_all\txt folder

import html_parser as hp
from bs4 import BeautifulSoup
from pathlib import Path

def convert_tumblr_quote_write_to_json(quote_file_path):
    with open(quote_file_path, 'r', encoding='utf16') as html_file:
        html_content = html_file.read()
    
    soup = BeautifulSoup(html_content, features="lxml")
    soup_txt = soup.get_text()
    soup_txt = hp.remove_text_start(soup_txt)
    soup_txt = hp.str_to_list(soup_txt)
    quote_dict = hp.cleanup_str_list(soup_txt)
    
    new_file_name = Path(quote_file_path).stem
    new_file_path = (current_path.parent / "data" / "tumblr_all" / "txt" / new_file_name).with_suffix(".json")
    hp.write_dict_to_file(quote_dict, new_file_path)


# test file
current_path = Path.cwd()
path_to_tumblr_posts = current_path.parent / "data" / "tumblr_all" / "html"
# test_file = path_to_tumblr_posts / "110348424618.html"
# test_file = path_to_tumblr_posts / "72327713057.html"
test_file = path_to_tumblr_posts / "127886382393.html"

p = Path(path_to_tumblr_posts).glob('*.html')
# files = [x for x in p if x.is_file()]
files = [test_file]

for f in files:
    print('Converting file: ' + str(f))
    convert_tumblr_quote_write_to_json(f)

# test read from file
testdict = hp.read_list_from_file(test_file)
print(testdict)