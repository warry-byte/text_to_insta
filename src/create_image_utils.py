from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import textwrap
import numpy as np


def create_image_from_txt(text, 
                 image_height = 1080, 
                 image_width = 1080, 
                 background_color = "black", 
                 text_color = "white",
                 text_font_path = Path.cwd().parent / "fonts" / "sylfaen.ttf",
                 text_font_size = 75,
                 path = Path.cwd().parent / "fig", 
                 filename = "test_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png", 
                 save_to_file = True, 
                 split_text_on_dash = True):
    
    # image = Image.new("L", (image_width, image_height), background_color) # "L": (8-bit pixels, black and white)
    image = Image.new(mode = "RGB", 
                      size = (image_width, image_height), 
                      color = background_color) # "L": (8-bit pixels, black and white)
    draw = ImageDraw.Draw(image) # get drawing context
    image_font = ImageFont.truetype(str(text_font_path), text_font_size)
    
    # Calculate initial size of text
    text_w, text_h = draw.textsize(text, font = image_font)
    
    # Lines separators not provided by the user - calculate default and wrap text in multiple lines
    if(not ("*" in text)): 
        ref_letter_width = draw.textsize("h", font = image_font)[0] # taking letter H as reference
        max_charact_per_line = np.round(image_width / ref_letter_width) # heuristic: calculate max number of char on the basis of the width of the H
        number_of_lines = int(np.ceil(len(text) / max_charact_per_line))
        
        if(number_of_lines > 2): # test if we can make it in two lines
            # reduce font size by 5%
            text_font_size = int(text_font_size * 0.95)
            image_font = ImageFont.truetype(str(text_font_path), text_font_size) # Necessary - cannot change the size of a font object after its creation
            # take a less restrictive reference letter width
            ref_letter_width = draw.textsize("h", font = image_font)[0]
            max_charact_per_line = np.round(image_width / ref_letter_width) # heuristic: calculate max number of char on the basis of the width of the H
            number_of_lines = int(np.ceil(len(text) / max_charact_per_line)) # this will be the final number of lines
        
        # wrap text 
        # wrapped_text = textwrap.wrap(text, 
                                     # width=max_charact_per_line)
        if(("-" in text) and (split_text_on_dash == True)):
            wrapped_text = text.split("-")
            # Add back hyphen to subsequent strings
            for t in range(1, len(wrapped_text)):
                wrapped_text[t] = "-" + str(wrapped_text[t])
                
        else: # normal wrapping 
            wrapped_text = textwrap.wrap(text,
                                         width=max_charact_per_line)
        
    else: 
        if("*" in text): # using the character as a line separator
            wrapped_text = text.split("*")
            number_of_lines = len(wrapped_text) # recalculate the number of lines

    # Initialize text coordinates
    h_center = image_height / 2
    total_text_height = number_of_lines * text_h
    h_start = h_center - total_text_height/2 # offset the whole text in height to have it centered
    current_h = h_start # initialize
    
    # Drawing each lines successively, and move the height cursor by one step equal to the height of a line of text in current font
    for line in range(0, number_of_lines):
        (current_line_width, dummy) = draw.textsize(wrapped_text[line], font = image_font)
        current_w = int((image_width-current_line_width)/2)
        draw.text((current_w, current_h), 
                  wrapped_text[line], 
                  fill = text_color, 
                  font = image_font)
        current_h += text_h # move top left corner y coordinate to the next line
        
    if(save_to_file):
        image.save((path / filename).with_suffix(".png"))
    else:
        image.show()
        
    print("Created file: " + str(path / filename))
    
    return (path / filename)
    
if __name__ == "__main__":
    
    # size = create_image("Plus je la rote, plus je l'aime!", save_to_file=False)
    create_image_from_txt("Plus je la rote, plus je l'aime!", 
                        text_font_size = 75, 
                        save_to_file = False)
    # create_image_from_txt("Et alors Hélène, on a encore fini en collimaçon?", 
    #                     text_font_size = 75, 
    #                     save_to_file = False)
    # print(size)