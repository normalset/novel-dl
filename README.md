# novel-dl
A simple python script to automatically scrape web novels from [novelhi](https://novelhi.com), [lightnovelhub](https://www.lightnovelhub.org/home) (and more to come soon) to compress it into an epub file for eReaders.

—

## Installation
Run this command in a terminal to install the required libraries (`pypandoc` , `requests` , `beautifulsoup4`, `selenium`):
```
pip3 install -r requirements.txt
```
(Tested on python 3.11.6)

## Usage
Run and follow the requests on the terminal 
```
python3 novelhi-dl.py
```
## Currently supported websites
- [lightnovelhub](https://www.lightnovelhub.org/home)
- [novelhi](https://novelhi.com)
- 
## Example run 

- Initial prompt to insert the novel link and the first and last chapter to include in the final epub file
![Initial prompt to insert the novel link and the first and last chapter to include in the final epub file](https://media.discordapp.net/attachments/1040311436083212309/1189926483200839773/Screenshot_2023-12-28_at_14.39.05.png?ex=659ff065&is=658d7b65&hm=8cc3ef5ff6894e73112b077aa8273d457801766c2b32811daaef16d8396fdeb6&=&format=webp&quality=lossless&width=454&height=246)

- Example of how the beginning of the download looks like
![Example of how the beginning of the download looks like](https://media.discordapp.net/attachments/1040311436083212309/1189926507234197504/Screenshot_2023-12-28_at_14.39.15.png?ex=659ff06b&is=658d7b6b&hm=4dc30ca4bd8740410fcb7bb04eee8e17ecad5aa277f405153ad3fde67ea5b7a3&=&format=webp&quality=lossless&width=624&height=117)

- Example of how the end of the download of a chapter looks like
![Example of how the end of the download of a chapter looks like](https://media.discordapp.net/attachments/1040311436083212309/1189926537802297384/Screenshot_2023-12-28_at_14.39.30.png?ex=659ff072&is=658d7b72&hm=307805f13b79954aac3d92605d7a5bffcc4cd290018f9d397f8b5449f8285bff&=&format=webp&quality=lossless&width=458&height=165)

- Example of how the compression into the final epub looks like
![Example of how the compression into the final epub looks like](https://media.discordapp.net/attachments/1040311436083212309/1189926551370870794/Screenshot_2023-12-28_at_14.39.46.png?ex=659ff075&is=658d7b75&hm=8b41f2846db709d3b1e09e1bce6c358d756677cc22dec14a4deafad8fddc6d50&=&format=webp&quality=lossless&width=539&height=218)
