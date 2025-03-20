# Novel Downloader (novel-dl)

A Python-based application to scrape, download, and compact web novels into EPUB files for eReaders. This tool supports multiple websites and provides both a graphical user interface (GUI) and a terminal-based interface for ease of use.

---

## Features

- **Scrape Web Novels**: Automatically fetch chapters from supported websites.
- **Download Chapters**: Save chapters in a structured format.
- **Compact into EPUB**: Convert downloaded chapters into an EPUB file for eReaders.
- **Supported Websites**:
  - [NovelHi](https://novelhi.com)
  - [LightNovelHub](https://www.lightnovelhub.org/home)
- **Graphical User Interface**: Built with `customtkinter` for a modern and user-friendly experience.
- **Terminal Interface**: For users who prefer command-line operations.

---

## Installation

### Prerequisites

- **Python Version**: Python 3.11.6 (or higher is recommended).
- **Required Libraries**: Install the dependencies listed in `requirements.txt`.

### Steps to Install

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/novel-dl.git
   cd novel-dl
   ```

2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Running the Application

#### Option 1: Using the Graphical User Interface (Recommended)
Run the following command to launch the GUI:
```bash
python3 ui_novel_dl.py
```

#### Option 2: Using the Terminal Interface
Run the following command to use the terminal-based interface:
```bash
python3 novel_dl.py
```

### How It Works

1. **Input the Novel URL**: Provide the URL of the novel's main page (not a specific chapter).
   - Example formats:
     - `https://novelhi.com/s/NovelName`
     - `https://www.lightnovelhub.org/novel/NovelName`
2. **Select Chapters**:
   - Specify the starting and ending chapter numbers.
   - Alternatively, choose to download all chapters.
3. **Download and Convert**:
   - The application will scrape the chapters, download them, and convert them into an EPUB file.
4. **Output**:
   - The EPUB file will be saved in the same directory as the script.

---

## Example Run

### Graphical User Interface
![Example using tkinter](./screenshots/ui.png)

### Terminal Interface
1. **Initial Prompt**: Insert the novel link and chapter range.
   ![Initial prompt](https://imgur.com/yH8c4cH.png)

2. **Download Progress**: View the progress of chapter downloads.
   ![Download progress](https://imgur.com/r3x0tpm.png)

3. **EPUB Compression**: See the final steps of EPUB creation.
   ![EPUB compression](https://imgur.com/MySZ15s.png)

---

## Libraries Used

The following Python libraries are required for this project:

- `fake_useragent`: For generating random user agents.
- `beautifulsoup4`: For parsing HTML content.
- `requests`: For making HTTP requests.
- `pypandoc`: For converting text files into EPUB format.
- `selenium`: For handling dynamic web pages.
- `Pillow`: For image processing.
- `customtkinter`: For creating the GUI.

Install them using:
```bash
pip install -r requirements.txt
```

---

## Notes

- Ensure you have the latest version of Chrome and the corresponding ChromeDriver installed for Selenium to work.
- The application has been tested on Python 3.11.6. Compatibility with older versions is not guaranteed.

---

## Contributing

Feel free to fork the repository and submit pull requests for improvements or new features.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
