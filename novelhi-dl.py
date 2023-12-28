import requests
import re
import pypandoc
import os
from bs4 import BeautifulSoup

#todo modify how the title is extracted from the URL for multiple websites

def download_image(url, save_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        print(f"\n\nImage downloaded and saved at: {save_path}")
    else:
        print(f"\n\nFailed to download image. Status code: {response.status_code}")

cover_save_path = 'cover-image.jpg'


#Get url from user
userURL = input("Enter the URL of the novel (without a chapter open) \nFormat of the link should be https://novelhi.com/s/NovelName\n: ")


FIRSTCHAPTER = input("\n\nInsert first chapter number to be downloaded: ")
LASTCHAPTER = input("\n\nInsert last chapter number to be downloaded: ")


#* Tokenize link to use correct website scraper
website = userURL.split('/')[2] #https: , "" , "website"

#? functions for different websites
#todo save functions in a separate file
def novel_hi_scraper():  
    #get bookname and open file
    global bookname 
    bookname = userURL.split('/')[4].replace('-',' ')
    print(f"\n\nbookname : {bookname}")

    #handle cover download
    coverRequest = requests.get(userURL)
    coverParser = BeautifulSoup(coverRequest.content, "html.parser")
    image_url = coverParser.find('img', class_='cover')['src']
    download_image(image_url, cover_save_path)
    coverRequest.close()
    
    file = open(f"{bookname}.txt" , "a+" )
    
    for chapterNumber in range(int(FIRSTCHAPTER) , int(LASTCHAPTER)+1): 
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
        print(f"PRINTING CHAPTER {chapterNumber}")
        #print(f'{chapterText}')
        print(f"CHAPTER {chapterNumber} DONE\n------------------------------")
        sentID = 0
    print("\n--------------------------------\nDONE downloading, starting compression into epub...\n----------------------------\n")

def lightnovelhub_scraper():
    print("debug: todo")



match website:
        case "novelhi.com":
            novel_hi_scraper()
        case "www.lightnovelhub.org":
            lightnovelhub_scraper()


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
    os.remove('cover-image.jpg')
    print(f"File 'cover-image.jpg' has been successfully removed.")
except FileNotFoundError:
    print(f"File 'cover-image.jpg' not found.")
except Exception as e:
    print(f"An error occurred: {e}")




