# This is an adaptation of: https://www.geeksforgeeks.org/python-make-a-simple-window-using-kivy/

# base Class of your App inherits from the App class.
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image

from pathlib import Path

import create_image_utils as iu
  
class LoginScreen(GridLayout):
    def __init__(self, **var_args):
          
        super(LoginScreen, self).__init__(**var_args)
        # super function can be used to gain access
        # to inherited methods from a parent or sibling class
        # that has been overwritten in a class object.
        self.cols = 1     # You can change it accordingly 
        self.add_widget(Label(text ='Citation')) 
        self.citation = TextInput(multiline = True)
        self.add_widget(self.citation)
        self.add_widget(Label(text ='hashtags'))
        self.hashtags = TextInput(multiline = False)
        self.add_widget(self.hashtags)
        
        self.generate_pic_btn = Button(text = "Générer image")
        self.generate_pic_btn.bind(on_press = self.on_generate_pic_press_callback)
        self.add_widget(self.generate_pic_btn)
        
        # Add picture vizualization - requires test.png to be present
        self.img = Image(source="test.png") # test: pic must be in the same folder
        self.add_widget(self.img)
  
    def on_generate_pic_press_callback(self, event):
        if(self.citation.text != ""):
            p = iu.create_image_from_txt(self.citation.text, 
                                      text_font_size = 75, 
                                      save_to_file=True, 
                                      path = Path.cwd(),
                                      filename='test.png')
            
            self.img.reload()

  
# the Base Class of our Kivy App
class MyApp(App): 
    def build(self):
        # return a LoginScreen() as a root widget
        return LoginScreen()
  
  
if __name__ == '__main__':
    MyApp().run()