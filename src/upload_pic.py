# Taken from https://stackoverflow.com/questions/52864531/posting-uploading-an-image-to-instagram-using-selenium-not-using-an-api

# import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import autoit
import time
from selenium.webdriver.common.keys import Keys
import keyring
from pathlib import Path
import insta_data_logger

is_connected = False
username = 'quedescentimetres' #your username
chromedriverpath = r"C:\Users\sub_s\Downloads\chromedriver_win32\chromedriver.exe"
driver = None

def remove_pop_up_windows():
    # Remove pop up windows if found
    list_parasitic_webelements = []
    current_elem = driver.find_elements_by_xpath("//button[contains(.,'Cancel')]")
    if(len(current_elem) > 0):
        list_parasitic_webelements.append(current_elem)
        
    current_elem = driver.find_elements_by_xpath("//button[contains(.,'Not Now')]")
    if(len(current_elem) > 0):
        list_parasitic_webelements.append(current_elem)
    
    for lis in list_parasitic_webelements:
        for elem in lis:
            elem.click()
    
def ig_connect():
    global is_connected
    global driver
    
    print("Connecting to Instragram...")
    
    password = keyring.get_password("instagram", username)
    
    mobile_emulation = {
        "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1" }
        # "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }
    chrome_options = Options()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    driver = webdriver.Chrome(chrome_options = chrome_options, 
                              executable_path = chromedriverpath)
    
    driver.get('https://www.instagram.com/')
    
    time.sleep(2)
    
    driver.find_element_by_xpath("//button[contains(.,'Accept All')]").click()
    
    time.sleep(2)
    
    driver.find_element_by_xpath("//button[contains(.,'Log In')]").click()
    
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password) 
    
    driver.find_element_by_xpath("//button[contains(.,'Log In')]").click()
    
    time.sleep(2)
    
    is_connected = True
    
    print("Done.")
    
def ig_post_picture(image_path, hashtags):
    
    global driver
    
    if(is_connected == False):
        ig_connect()
    else:
        remove_pop_up_windows()
    
    # Produce caption by listing all hashtags
    caption = ""
    for h in hashtags:
        caption += "#" + h + " "
    
    driver.get('https://www.instagram.com/' + username)
    
    ActionChains(driver).move_to_element( driver.find_element_by_xpath("""//*[@id="react-root"]/section/nav[2]/div/div/div[2]/div/div/div[3]""")).click().perform()
    handle = "[CLASS:#32770; TITLE:Open]"
    autoit.win_wait(handle, 3)
    autoit.control_set_text(handle, "Edit1", image_path)
    autoit.control_click(handle, "Button1")
    
    time.sleep(2)
    
    driver.find_element_by_xpath("""//*[@id="react-root"]/section/div[1]/header/div/div[2]/button""").click()
    
    time.sleep(2)
    
    txt = driver.find_element_by_class_name('_472V_')
    txt.send_keys('')
    txt = driver.find_element_by_class_name('_472V_')
    txt.send_keys(caption) # Caption to be sent with the picture
    
    # Click on the Share button to finalize post
    # driver.find_element_by_xpath("""//*[@id="react-root"]/section/div[1]/header/div/div[2]/button""").click()
    driver.find_element_by_xpath("//button[contains(.,'Share')]").click()
    
    # Just in case the buttons are open
    for s in range(1, 6):
        remove_pop_up_windows()
        time.sleep(2)
        
    print("Posted " + Path(image_path).stem)
    
    

if __name__ == "__main__":
    # testing upload
    image_path = r"C:\git-repos\text_to_insta\fig\black303.jpg"
    hashtags = ["truc", "noir"]
    
    ig_post_picture(image_path, hashtags)
    
    
