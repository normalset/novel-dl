import requests
import re
import pypandoc
import os
from bs4 import BeautifulSoup

def extract_series_name(url):
    # Define a regular expression pattern to match the series name in the URL
    pattern = re.compile(r'https://novelhi.com/s/(.*)')

    # Use the pattern to search for a match in the URL
    match = pattern.search(url)

    # If a match is found, extract and return the series name
    if match:
        series_name = match.group(1)
        # Replace '-' with ' ' in the series name
        series_name = series_name.replace('-', ' ')
        return series_name
    else:
        return None

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
BOOKNAME = extract_series_name(userURL)
print(f"\n\nBOOKNAME : {BOOKNAME}")

coverRequest = requests.get(userURL)
coverParser = BeautifulSoup(coverRequest.content, "html.parser")
image_url = coverParser.find('img', class_='cover')['src']

download_image(image_url, cover_save_path)

coverRequest.close()


#!reset file and open in append mode
    # file = open(f"{BOOKNAME}.txt" , "w" )
    # file.close()


file = open(f"{BOOKNAME}.txt" , "a+" )
#Insert Book Name
file.write(f'%{BOOKNAME}\n')


FIRSTCHAPTER = input("\n\nInsert first chapter number to be downloaded: ")
LASTCHAPTER = input("\n\nInsert last chapter number to be downloaded: ")

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
  print(f'{chapterText}')
  print(f"CHAPTER {chapterNumber} DONE\n------------------------------")
  sentID = 0

print("\n------------------------------\nDONE downloading, starting compression into epub...\n----------------------------\n")

#download cover art



# Specify the input and output formats
input_format = 'markdown'
output_format = 'epub'

# Read the content of the input file
with open(f'{BOOKNAME}.txt', 'r', encoding='utf-8') as f:
    content = f.read()


# Convert the content using pypandoc and save it directly to the output file
pypandoc.convert_file(f'{BOOKNAME}.txt', output_format, format=input_format, outputfile=f'{BOOKNAME}.epub', extra_args=[
        '--metadata', f'cover-image={cover_save_path}',
    ])

print("Compression into epub done!\n")  

#remove .txt file
try:
    os.remove(f'{BOOKNAME}.txt')
    print(f"File '{BOOKNAME}.txt' has been successfully removed.")
except FileNotFoundError:
    print(f"File '{BOOKNAME}.txt' not found.")
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




