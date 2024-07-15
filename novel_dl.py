import requests
import pypandoc
# pypandoc.download_pandoc()
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from utility_functions import *

#? Global definitions
cover_save_path = 'cover-image.png'


#? functions for different websites
#todo save functions in a separate file
def novel_hi_scraper(fc, lc):  
    #get bookname and open file
    global bookname 
    bookname = get_bookname_from_url(userURL)

    #get last chapter
    if lc and lc == "getLastChapter":
        lc = get_nh_lastchapter(userURL)

    #handle cover download
    coverRequest = requests.get(userURL)
    coverParser = BeautifulSoup(coverRequest.content, "html.parser")
    image_url = coverParser.find('img', class_='cover')['src']
    download_image_novelhi(image_url, cover_save_path)
    coverRequest.close()
    
    file = open(f"{bookname}.txt" , "a+" )
    
    chapterNumber = int(fc)
    while chapterNumber <= int(lc): 
        url = f"{userURL}/{chapterNumber}"
        page = requests.get(url)
        print("DEBUG" , page)

        #handle case where website fails
        if page.status_code!= 200:
            print(f"Website failed to load, last chapter correctly downloadead is {chapterNumber-1}")
            chapterNumber -= 1 
            time.sleep(1)
            continue

        parser = BeautifulSoup(page.content, "html.parser")

        sentID = 0
        chapterText = "" 

        chapterName = parser.find("h1").text
        chapterText += "\n# " + chapterName + "\n"


        while(parser.find(id=f"{sentID}")):
            chapterText += "\n" + f'{parser.find(id=f"{sentID}").text}' + "\n"
            sentID += 1

        page.close()
        file.write(chapterText)
        print(f"CHAPTER {chapterNumber} DONE\n")
        sentID = 0
        chapterNumber += 1

    print("\n--------------------------------\nDONE downloading, starting compression into epub...\n----------------------------\n")

def lightnovelhub_scraper(fc, lc): 

    chrome_options = webdriver.ChromeOptions() # Set up the headless browser for webdriver
    chrome_options.add_argument('--headless')  # Run Chrome in headless mode
    chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration (needed in headless mode)
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=chrome_options) # Create a WebDriver instance with the specified options
    driver.minimize_window()

    #get bookname and open file
    global bookname 
    bookname = get_bookname_from_url(userURL)

    #get last chapter
    if lc and lc == "getLastChapter":
        lc = get_lnh_lastchapter(userURL)

    #download cover image for epub file
    download_image_lightnovelhub(userURL, cover_save_path)
    
    file = open(f"{bookname}.txt" , "a+" )
    
    chapterNumber = int(fc)
    while chapterNumber <= int(lc): 
        try: 
            url = f"{userURL}/chapter-{chapterNumber}"
            
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)

            # Wait for some time to allow JavaScript to execute  fix by using webdriverWait(driver , n).until( condition )
            driver.implicitly_wait(10)
            page = driver.page_source
            
            #print("DEBUG" , page)

            parser = BeautifulSoup(page, "html.parser")

            chapterText = "" 
            chapterName = parser.find("span", {"class": "chapter-title"}).text
            chapterText += "\n# " + chapterName + "\n"

            container = parser.find("div", {"id": "chapter-container"})
            chapterTextArray = container.find_all("p")
            for line in chapterTextArray:
                chapterText += "\n" + line.text + "\n"

            driver.quit()

            file.write(chapterText)
            print(f"CHAPTER {chapterNumber} DONE\n")
            chapterNumber += 1
        except Exception as error:
            print("[ERR] got an error, redownloading chapter n: ",chapterNumber , error)
            chapterNumber -= 1 
            time.sleep(1)
            continue

    print("\n--------------------------------\nDONE downloading, starting compression into epub...\n----------------------------\n")



#* main function
#Get url from user
userURL = input("Enter the URL of the novel (without a chapter open) \nFormat of the link should be https://novelhi.com/s/NovelName or https://www.lightnovelhub.org/novel/novelName\n: ")


FIRSTCHAPTER = input("\n\nInsert first chapter number to be downloaded (leave empty to download from the first chapter): ")
if FIRSTCHAPTER == "" : FIRSTCHAPTER = 1
LASTCHAPTER = input("\n\nInsert last chapter number to be downloaded (leave empty to download to the last ): ")
if LASTCHAPTER == "" : LASTCHAPTER = "getLastChapter"
#* Tokenize link to use correct website scraper
website = userURL.split('/')[2] #https: , "" , "website"

match website:
    case "novelhi.com":
        novel_hi_scraper(FIRSTCHAPTER, LASTCHAPTER)
    case "www.lightnovelhub.org":
        lightnovelhub_scraper(FIRSTCHAPTER, LASTCHAPTER)

# Specify the input and output formats
input_format = 'markdown'
output_format = 'epub'

# Read the content of the input file
with open(f'{bookname}.txt', 'r', encoding='utf-8') as f:
    content = f.read()


# Convert the content using pypandoc and save it directly to the output file
pypandoc.convert_file(f'{bookname}.txt', output_format, format=input_format, outputfile=f'{bookname}.epub', extra_args=[
        '--metadata', f'cover-image={cover_save_path}',
        '--metadata', f'language=en',
        '--metadata', f'title={bookname}',
    ])

print("Compression into epub done!\n")  

#remove .txt file if user wants to remove .txt
removeTXT = input("\n\nDo you want to remove the.txt file? Keep to update with newer chapters later\n(y/n): ") #todo avoid doing this by reconverting epub into .txt
if(removeTXT == 'y'):
    try:
        os.remove(f'{bookname}.txt')
        print(f"File '{bookname}.txt' has been successfully removed.")
    except FileNotFoundError:
        print(f"File '{bookname}.txt' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

#remove coverImage file
try:
    os.remove('cover-image.png')
    print(f"File 'cover-image' has been successfully removed.")
except Exception as e:
    print(f"Image not deleted: {e}")
