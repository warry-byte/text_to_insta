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
import insta_data_logger as ig_log

is_connected = False
username = 'quedescentimetres' #your username
driver = None
is_ready = False # will be set to true when the page is ready to accept clicks from us (new post)

def remove_pop_up_windows():
    # Remove pop up windows if found
    list_parasitic_webelements = []
    try:
        current_elem = driver.find_elements_by_xpath("//button[contains(.,'Cancel')]")
        if(len(current_elem) > 0):
            list_parasitic_webelements.append(current_elem)
    except:
        pass
        
    try:
        current_elem = driver.find_elements_by_xpath("//button[contains(.,'Not Now')]")
        if(len(current_elem) > 0):
            list_parasitic_webelements.append(current_elem)
    except:
        pass
    
    for lis in list_parasitic_webelements:
        for elem in lis:
            elem.click()
    
def ig_connect():
    global is_connected
    global driver
    
    print("Connecting to Instagram...")
    
    password = keyring.get_password("instagram", username)
    
    mobile_emulation = {
        "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1" }
        # "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }
    chrome_options = Options()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    #chrome_options.add_argument("--headless")
    #chrome_options.add_argument("--remote-debugging-port=9515")
    #chrome_options.binary_location = r"C:\Users\sub_s\Downloads\chromedriver_win32_v106\chromedriver.exe"
    #driver = webdriver.Chrome(options = chrome_options, 
    #                          executable_path = chrome_options.binary_location)
    
    # IF NOT WORKING AZNYMORE, FOLLOW THESE STEPS:
    # - Download the chromedriver that corresponds to your version of Chrome: https://sites.google.com/chromium.org/driver/
    # - Unzip 
    # - Include the unzipped folder in your path
    driver = webdriver.Chrome(options = chrome_options)
    driver.get('https://www.instagram.com/')
    
    time.sleep(2)
    
    driver.find_element_by_xpath("//button[contains(.,'Only allow essential cookies')]").click()
    
    time.sleep(2)
    
    driver.find_element_by_xpath("//button[contains(.,'Log In')]").click()
    
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password) 
    
    driver.find_element_by_xpath("//button[contains(.,'Log In')]").click()
    
    time.sleep(4)
    
    # Remove pop up windows    
    button_label = "Cancel"
    
    wait_for_element_and_click(button_label)
    
    button_label = "Not Now"
    
    wait_for_element_and_click(button_label)
    
    is_connected = True
    
    print("Done.")

def ig_create_caption(quote):
    # Produce caption by listing all hashtags
    caption = ""
    for h in quote["hashtags"]:
        caption += "#" + h + " "
        
    # Append date for captions
    caption += "\n." * 8 # Why 8? Because.
    
    caption += "\n" + "Anonyme, " + quote["date"]
    
    return caption
    
def ig_post_picture(image_path, quote):
    
    global driver
    global is_connected
    global is_ready
    
    if(is_connected == False):
        ig_connect()
    else:
        remove_pop_up_windows()
    
    is_ready = False # will allow to wait for the appropriate buttons inside the Wait function (is_ready is a marker that we do not wait for any button to be clicked)
    
    caption = ig_create_caption(quote)
    
    driver.get('https://www.instagram.com/' + username + "/#")
    
    #ActionChains(driver).move_to_element( driver.find_element_by_xpath("""//*[@id="react-root"]/section/nav[2]/div/div/div[2]/div/div/div[3]""")).click().perform()
    #ActionChains(driver).move_to_element( driver.find_element_by_xpath("""//*[@id="react-root"]/section/nav[2]/div/div/div[2]/div/div/div[3]""")).click().perform()
    
    #button_label = "Post"
    #wait_for_element_and_click(button_label)
   
    time.sleep(3)
    
    driver.find_element_by_xpath("""/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/nav[2]/div/div/div/div/div/div[3]""").click()
    driver.find_element_by_xpath("""/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/nav[2]/div/div/div/div/div/div[3]/div/div[1]/div[1]/div/div/div[1]/div[1]""").click() # find element by div class on HTML page
    
    handle = "[CLASS:#32770; TITLE:Open]"
    autoit.win_wait(handle, 3)
    time.sleep(2) # test
    autoit.control_set_text(handle, "Edit1", str(image_path))
    autoit.control_click(handle, "Button1")
    
    time.sleep(2)
    
    # "Next" button
    #driver.find_element_by_xpath("""//*[@id="react-root"]/section/div[1]/header/div/div[2]/button""").click()
    wait_for_element_and_click("Next")
    
    time.sleep(2)
    
    # Find text area "Write a caption..." (seen in HTML, 2022-10-02)    
    txt = driver.find_element_by_xpath("//textarea[@aria-label='Write a caption...']")
    txt.send_keys(caption)
    
    # Click on the Share button to finalize post
    wait_for_element_and_click("Share")
    
    # Just in case the buttons are open
    for s in range(1, 6):
        remove_pop_up_windows()
        time.sleep(2)
        
    print("Posted " + Path(image_path).stem + ".json")
    
    is_ready = True # at the end of a post, the page is considered as ready (2022-10-02)
    

def wait_for_element_and_click(button_label):
    global driver
    global is_ready
    
    if(is_ready == True): # disable check if the page is considered as ready (e.g. end of a post)
        return
    
    element_found = False
    xpath = f"//button[contains(.,'{button_label}')]"
    
    while(not element_found):
        try:
            driver.find_element_by_xpath(xpath).click()
            element_found = True
        except:
            pass


if __name__ == "__main__":
    # testing upload
    image_path = r"C:\git-repos\text_to_insta\fig\black303.jpg"
    hashtags = ["marty", "mcfly"]
    quote = {
        'quote' : "C'est pas le pied!", 
        'hashtags' : hashtags, 
        'date' : "21 Octobre 2015"
        }
    
    ig_post_picture(image_path, quote)
    
    
