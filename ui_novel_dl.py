import os , signal , sys 
from multiprocessing import Process, Pipe, Semaphore, Queue
import requests
import pypandoc
# pypandoc.download_pandoc()
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from utility_functions import *
import custom_ui as ui

#todo get download functions working without global declarations
#todo separate main and download functions
#todo integrate manga-dl 

#? Global definitions
cover_save_path = 'cover-image.png'

#signal to close if ui window gets closed
signal.signal(signal.SIGTERM , sigterm_handler)

#create semaphore and pipe
proc_sem = Semaphore(0)
dl_pipe, ui_pipe = Pipe()

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
    debug_msg_q.put_nowait(f"Cover image downloaded and saved")
    
    file = open(f"{bookname}.txt" , "a+" )
    
    for chapterNumber in range(int(fc) , int(lc)+1): 
        url = f"{userURL}/{chapterNumber}"
        page = requests.get(url)
        print("DEBUG" , page)

        #handle case where website fails
        if page.status_code!= 200:
            print(f"Website failed to load, last chapter correctly downloadead is {chapterNumber-1}")
            break

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
        #!!! testing
        debug_msg_q.put_nowait(f"Chapter {chapterNumber} downloaded")
        sentID = 0
    print("\n--------------------------------\nDONE downloading, starting compression into epub...\n----------------------------\n")
    debug_msg_q.put_nowait(f"DONE downloading, starting compression into epub...")

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
    debug_msg_q.put_nowait(f"Cover image downloaded and saved")
    
    file = open(f"{bookname}.txt" , "a+" )
    
    for chapterNumber in range(int(fc) , int(lc)+1): 
        url = f"{userURL}/chapter-{chapterNumber}"
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        # Wait for some time to allow JavaScript to execute (adjust the time as needed)
        driver.implicitly_wait(10)
        page = driver.page_source
        
        #print("DEBUG" , page)

        # handle case where website fails
        # if page.status_code!= 200:
        #     print(f"Website failed to load, last chapter correctly downloadead is {chapterNumber-1}")
        #     break

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
        debug_msg_q.put_nowait(f"Chapter {chapterNumber} downloaded")
    print("\n--------------------------------\nDONE downloading, starting compression into epub...\n----------------------------\n")
    debug_msg_q.put_nowait(f"DONE downloading, starting compression into epub...")



#* main function
if __name__ == '__main__' :
    
    debug_msg_q = Queue()
    #define ui process and pass arguments
    ui_process = Process(target=ui.create_ui , args=(ui_pipe, proc_sem, debug_msg_q, ))
    ui_process.start()
    while(1):
        #wait for ui process to post sem
        proc_sem.acquire()


        # get variables
        userURL, first_chapter, last_chapter, removeTXT = dl_pipe.recv()
        print(f"Recieved user input: {userURL}, {first_chapter}, {last_chapter}, {removeTXT}")


        try:
            website = userURL.split('/')[2] #https: , "" , "website"
            match website:
                case "novelhi.com":
                    novel_hi_scraper(first_chapter, last_chapter)
                case "www.lightnovelhub.org":
                    lightnovelhub_scraper(first_chapter, last_chapter)

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
            debug_msg_q.put_nowait("Compression into epub done!")

            #remove .txt file if user wants to remove .txt
            if(removeTXT):
                try:
                    os.remove(f'{bookname}.txt')
                    print(f"File '{bookname}.txt' has been successfully removed.")
                    debug_msg_q.put_nowait(f"File '{bookname}.txt' has been successfully removed.")
                except FileNotFoundError:
                    print(f"File '{bookname}.txt' not found.")
                except Exception as e:
                    print(f"An error occurred: {e}")

            #remove coverImage file
            try:
                os.remove('cover-image.png')
                debug_msg_q.put_nowait("File 'cover-image' has been successfully removed.")
                print(f"File 'cover-image' has been successfully removed.")
            except Exception as e:
                debug_msg_q.put_nowait(f"Image not deleted: {e}")
                print(f"Image not deleted: {e}")

            debug_msg_q.put_nowait("Download Completed")
        except:
            debug_msg_q.put_nowait("Error: Data not correct or server Error. Try Again")

