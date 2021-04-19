from instabot import Bot
from pathlib import Path
from PIL import Image
import argparse

#%% Connection data (to be modified)
username = 'quedescentimetres' #your username
password = 'Mb(I)p7C2MdP!TdQm!' #your password 


#%% Define paths and filenames
current_path = Path.cwd()
fig_path = current_path.parent / 'fig'
test_fig = "black303.jpg"

#%% Create image
img = Image.new('RGB', (1080, 1080), color = 'black')
img.save(fig_path / test_fig)

#%% Connect to instagram and upload picture
bot = Bot()
bot.login(username = username, 
          password = password, 
          use_cookie=False,
          use_uuid = False)
bot.upload_photo(fig_path / test_fig, "testamere")


