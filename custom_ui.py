import tkinter as tk
from multiprocessing import Process, Pipe
import sys , signal, os 

import customtkinter as ctk

# from utility_functions import *

from PIL import Image , ImageTk

#todo  if text == "Cover image downloaded and saved" : add_cover_img() -> display downloaded cover-img.png file

bgc = "#1F2423"
textc = "#D8F3DC"
buttonc = "#2D6A4F"
highlightc = "#1B4332"

def create_ui(pipe, proc_sem, queue,):

  def reset():
    run_button.pack(pady=5)
    elink.delete(0, tk.END)
    s_chap_entry.delete(0, tk.END)
    e_chap_entry.delete(0, tk.END)


  def update_debug(label):
    if(not queue.empty()):
      text = queue.get_nowait()
      label.configure(text=text)
      # if label says the download is completed put download button back
      if text == "Download Completed" or "Error: Data not correct or server Error" : reset()
      #todo if text == "Cover image downloaded and saved" : add_cover_img()

  
  # closing window handler function
  def on_closing():
    app.quit()  # Quit the Tkinter event loop
    app.destroy()  # Destroy the window (optional)
    print("Window close, exiting program")
    pipe.close()
    os.kill(os.getppid() , signal.SIGTERM) # send sigterm to close parent process
    sys.exit()

  def start_download():
    print("download Button pressed")
    # run_button.destroy()
    run_button.pack_forget()
    userURL = elink.get()
    first_chapter = s_chap_entry.get()
    last_chapter = e_chap_entry.get()
    if download_all_var.get() :
        first_chapter = 1
        last_chapter = "getLastChapter"
    removetxt = txt_var.get()
    print(f"Sent user input: {userURL}, {first_chapter}, {last_chapter}, {removetxt}")
    pipe.send((userURL, first_chapter, last_chapter, removetxt))
    proc_sem.release()

  ctk.set_appearance_mode("Dark")  # Modes: system (default), light, dark
  ctk.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

  # create CTk window
  app = ctk.CTk(fg_color=bgc)  
  app.geometry("700x420")
  app.title("novel-dl by normalset")
  app.protocol("WM_DELETE_WINDOW", on_closing)

  main_frame = ctk.CTkFrame(app , fg_color=bgc,)
  main_frame.pack(pady=10)

  link_frame = ctk.CTkFrame(main_frame, fg_color=bgc,)
  link_frame.pack(pady=10)

  link_text = ctk.CTkLabel(link_frame, text="Novel Link", font=("Helvetica", 16))
  link_text.pack()
  link_text2 = ctk.CTkLabel(link_frame, text="Enter the URL of the novel (without a chapter open) \nFormat of the link should be:\n https://novelhi.com/s/NovelName or https://www.lightnovelhub.org/novel/novelName ", font=("Helvetica", 12))
  link_text2.pack()

  elink = ctk.CTkEntry(link_frame, justify=ctk.CENTER)
  elink.pack(pady=5, fill=ctk.X, padx=15)

  # Chapter section
  chapter_frame =  ctk.CTkFrame(main_frame,  fg_color=bgc,)
  chapter_frame.pack(pady=10)


  s_chap_text =  ctk.CTkLabel(chapter_frame, text="From Chapter", font=("Helvetica", 16), )
  s_chap_text.grid(row= 0, column=0)

  s_chap_entry =  ctk.CTkEntry(chapter_frame, justify=ctk.CENTER)
  s_chap_entry.grid(row=1 , column=0, pady=5, padx=5)

  e_chap_text =  ctk.CTkLabel(chapter_frame, text="To Chapter", font=("Helvetica", 16), )
  e_chap_text.grid(row=0 , column=1)

  e_chap_entry =  ctk.CTkEntry(chapter_frame, justify=ctk.CENTER)
  e_chap_entry.grid(row=1 , column=1, pady=5, padx=5)


  # Checkbox section
  download_all_var = ctk.BooleanVar()
  txt_var = ctk.BooleanVar()

  download_all_check = ctk.CTkCheckBox(
      main_frame,
      text="Download All Chapters",
      command=lambda: print("download_all set to ",download_all_var.get()),
      variable=download_all_var,
      onvalue=True,
      offvalue=False,
      fg_color=bgc,
      checkmark_color=textc, 
      checkbox_height=20 ,
      checkbox_width=20 ,
      corner_radius=5 ,
      hover_color=highlightc
  )
  download_all_check.pack(pady=10)

  txt_check = ctk.CTkCheckBox(
      main_frame,
      text="Remove .txt file created while scanning, keep to add more chapters later",
      command=lambda: print("removetxt set to ",txt_var.get()),
      variable=txt_var,
      onvalue=True,
      offvalue=False,
      fg_color=bgc,
      checkmark_color=textc , 
      checkbox_height=20 ,
      checkbox_width=20 ,
      corner_radius=5 ,
      hover_color=highlightc
  )
  txt_check.pack(pady=5)

  debug_text = ctk.CTkLabel(main_frame, text="made with <3 by normalset" ,font=("Helvetica", 11), fg_color=highlightc, corner_radius=10)
  debug_text.pack(pady = 15)

  run_button = ctk.CTkButton(main_frame, text="Download", font=("Helvetica", 14), command=start_download , fg_color="transparent" , border_color=buttonc , border_width=2 , hover_color="#1B4332",)
  run_button.pack(pady=5)


  # Start a loop within the main event loop for updates
  def loop():
    update_debug(debug_text)
    app.after(200, loop)  # Schedule next update

  loop()  # Call loop to start periodic updates

  app.mainloop()
