import tkinter as tk
from multiprocessing import Process, Pipe


from utility_functions import *

    

def create_ui(pipe, proc_sem, queue,):

    def update_debug(label):
        if(not queue.empty()):
            label.configure(text=queue.get_nowait())

    # closing window handler function
    def on_closing():
        f.quit()  # Quit the Tkinter event loop
        f.destroy()  # Destroy the window (optional)
        print("Window close, exiting program")
        pipe.close()
        exit()

    def start_download():
        print("download Button pressed")
        run_button.destroy()
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

    # Define black and white colors
    background_color = "#c5bcd6"  # White background
    text_color = "#000000"  # Black text
    entry_background_color = "#e0e0e0"  # Light gray entry background

    f = tk.Tk()

    f.title("novel-dl by normalset")
    f.geometry("700x400")
    f.configure(background=background_color)
    f.protocol("WM_DELETE_WINDOW", on_closing)

    # Custom icon (if applicable)
    # icon = tk.PhotoImage(file="icon.png")
    # f.iconphoto(True, icon)

    # Improved layout with frames for grouping
    main_frame = tk.Frame(f, bg=background_color)
    main_frame.pack(padx=20, pady=20)

    # Link section
    link_frame = tk.Frame(main_frame, bg=background_color)
    link_frame.pack(pady=10)

    link_text = tk.Label(link_frame, text="Novel Link", font=("Helvetica", 14), fg=text_color, bg=background_color)
    link_text.pack()
    link_text2 = tk.Label(link_frame, text="Enter the URL of the novel (without a chapter open) \nFormat of the link should be:\n https://novelhi.com/s/NovelName or https://www.lightnovelhub.org/novel/novelName ", font=("Helvetica", 9), fg=text_color, bg=background_color)
    link_text2.pack()

    elink = tk.Entry(link_frame, justify=tk.CENTER, bg=entry_background_color, fg=text_color)
    elink.pack(pady=5, fill=tk.X, padx=15)



    # Chapter section
    chapter_frame = tk.Frame(main_frame, bg=background_color)
    chapter_frame.pack(pady=10)


    s_chap_text = tk.Label(chapter_frame, text="From Chapter", font=("Helvetica", 12), fg=text_color, bg=background_color)
    s_chap_text.grid(row= 0, column=0)

    s_chap_entry = tk.Entry(chapter_frame, bg=entry_background_color, fg=text_color)
    s_chap_entry.grid(row=1 , column=0, pady=5, padx=5)

    e_chap_text = tk.Label(chapter_frame, text="To Chapter", font=("Helvetica", 12), fg=text_color, bg=background_color)
    e_chap_text.grid(row=0 , column=1)

    e_chap_entry = tk.Entry(chapter_frame, bg=entry_background_color, fg=text_color)
    e_chap_entry.grid(row=1 , column=1, pady=5, padx=5)

    # Checkbox section
    download_all_var = tk.BooleanVar()
    txt_var = tk.BooleanVar()

    download_all_check = tk.Checkbutton(
        main_frame,
        text="Download All Chapters",
        command=lambda: print("download_all set to ",download_all_var.get()),
        variable=download_all_var,
        onvalue=True,
        offvalue=False,
        fg=text_color,
        bg=background_color,
    )
    download_all_check.pack(pady=10)

    txt_check = tk.Checkbutton(
        main_frame,
        text="Remove .txt file created while scanning, keep to add more chapters later",
        command=lambda: print("removetxt set to ",txt_var.get()),
        variable=txt_var,
        onvalue=True,
        offvalue=False,
        fg=text_color,
        bg=background_color,
    )
    txt_check.pack(pady=5)


    run_button = tk.Button(main_frame, text="Download", font=("Helvetica", 14), fg=text_color, bg=background_color, command=start_download)
    run_button.pack(pady=5)

    debug_text = tk.Label(main_frame, text="", font=("Helvetica", 12), fg=text_color, bg=background_color)
    debug_text.pack(pady = 10)

     # Start a loop within the main event loop for updates
    def loop():
        update_debug(debug_text)
        f.after(500, loop)  # Schedule next update

    loop()  # Call loop to start periodic updates

    f.mainloop()
    return debug_text

