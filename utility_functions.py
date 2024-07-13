import requests

from bs4 import BeautifulSoup as bs

#per proxies
from fake_useragent import UserAgent
from urllib.request import Request, urlopen

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from multiprocessing import Queue

import os , signal , sys , time, random

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

#closing parent process if window gets closed
def sigterm_handler(si, frame):
    print("UI process ended, terminating parent process")
    sys.exit()

### Proxy functions


# Function to extract proxies from https://www.sslproxies.org/ to be used when getting a website request
def generate_proxies(proxy_list):
    ua = UserAgent() 
    proxy_list.clear() # Svuoto la lista dei proxy (nel caso la funzione venga chiamata più volte non si vogliono avere duplicati)
    proxies_req = Request('https://www.sslproxies.org/')
    proxies_req.add_header('User-Agent', ua.random)
    proxies_doc = urlopen(proxies_req).read().decode('utf8')
    soup = bs(proxies_doc, 'html.parser')
    proxies_table = soup.find('table', class_='table table-striped table-bordered')
    # Salvo i proxy nella lista proxies
    for row in proxies_table.tbody.find_all('tr'):
        td = row.find_all('td')
        proxy_list.append({
        'ip':   td[0].string,
        'port': td[1].string})

# function to request a page using proxies
def get_request_page(url, proxies):
    ua = UserAgent() 
    original_proxy_count = len(proxies)
    while True:
        if len(proxies) == 0:
            print(f"Max blocked proxies reached, getting new ones ({original_proxy_count})")
            raise StopIteration
        proxy = random.choice(proxies)
        # print("uso il proxy : ",proxy)
        user_agent = ua.random
        try:
            headers = {'User-Agent': user_agent}
            response = requests.get(url, headers=headers, proxies=proxy)
            # print(response)
            soup = bs(response.text, 'html.parser')
            if response.text.startswith("Too"):
                 proxies.remove(proxy)
                 print(f"Website blocked the request, changing proxy... (numero di proxy rimanenti: {len(proxies)})")
                 time.sleep(5)  # Attendi 5 secondi prima di provare un nuovo proxy
                 continue
            
            #se ho una risposta OK, restituisco la risposta e l'oggetto response
            return response        
        except:
            proxies.remove(proxy)
            print(f"Errore durante la richiesta. Cambio proxy... (numero di proxy rimanenti alla sospensione dell'esecuzione: {len(proxies)})")
            time.sleep(5)  # Attendi 5 secondi prima di provare un nuovo proxy
            continue