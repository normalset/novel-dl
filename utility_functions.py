import requests

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from multiprocessing import Queue

def create_selenium_driver():
  chrome_options = webdriver.ChromeOptions() # Set up the headless browser for webdriver
  chrome_options.add_argument('--headless')  # Run Chrome in headless mode
  chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration (needed in headless mode)
  chrome_options.add_argument('--no-sandbox')
  driver = webdriver.Chrome(options=chrome_options) # Create a WebDriver instance with the specified options
  driver.minimize_window()
  return driver

# function to get bookname from passed url
def get_bookname_from_url(url): #? works form novelhi/lightnovelhub tbd for other websites
    #handle case where website fails or userURL is not correct
    try:
        bookname = url.split('/')[4].replace('-',' ')
        print(f"\n\nBookname : {bookname}")
        return bookname
    except Exception as e:
            print(f"Error: {e}")
            print("Novel URL is not in correct format. Please try again.")
            exit()

# image download functions
def download_image_novelhi(url, save_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        print(f"\n\nImage downloaded and saved at: {save_path}")
    else:
        print(f"\n\nFailed to download image. Status code: {response.status_code}")

def download_image_lightnovelhub(url, save_path):
    driver = create_selenium_driver()
    driver.get(url)
    driver.implicitly_wait(10)
    # Find the image element using the By.TAG_NAME method, get 3rd item and save it
    image = driver.find_elements(By.TAG_NAME, 'img')[2]
    image.screenshot(save_path)
    
    print(f"\n\nImage downloaded and saved at: {save_path}")
    # Close the browser
    driver.quit()


##* Get last chapter from website
#novelhi
def get_nh_lastchapter(url):
    driver = create_selenium_driver()
    driver.get(url)
    driver.implicitly_wait(10)
    c = driver.find_element(By.CSS_SELECTOR, "#indexList > li:nth-child(1) > span:nth-child(1) > a:nth-child(1)").text
    return c.split("Chapter ")[1]


#lightnovelhub
def get_lnh_lastchapter(url):
    driver = create_selenium_driver()
    driver.get(url)
    driver.implicitly_wait(10)
    return driver.find_element(By.CSS_SELECTOR, ".header-stats > span:nth-child(1) > strong:nth-child(1)").text
