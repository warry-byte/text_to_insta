from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import textwrap
import numpy as np

width = 1080
height = 1080
font_size = 75

# text = "H" * 20
text = "on a encore fini en collimaçon?"

img = Image.new("L", (width, height), color=0)   # "L": (8-bit pixels, black and white)
font = ImageFont.truetype("arial.ttf", font_size)
draw = ImageDraw.Draw(img)
w, h = draw.textsize(text, font=font)
h += int(h*0.21)
draw.text(((width-w)/2, (height-h)/2), text=text, fill='white', font=font)
# img.save('H.png')
img.show()