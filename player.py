import tkinter as tk
import pygame
from tkinter.ttk import Progressbar
from tkinter import filedialog
import customtkinter as ctk
from mutagen.mp3 import MP3
import os
import threading
import time


#pygame mixer initialization
pygame.mixer.init()


#current position of song
current_position=0
paused= False
selected_folder_path="" # store selected folder path


def update_progress():
    global current_position
    while True:
        if pygame.mixer.music.get_busy() and not paused:
            current_position=pygame.mixer.music.get_pos()/1000
            pbar["value"]=current_position


            if current_position>=pbar["maximum"]:
                stop_music()
                pbar["value"]=0

            root.update
        time.sleep(0.1)

#Thread to update the progressbar
pt=threading.Thread(target=update_progress)
pt.daemon=True
pt.start()

def select_music_folder():
    global selected_folder_path
    selected_folder_path=filedialog.askdirectory()
    if selected_folder_path:
        lbox.delete(0, tk.END)
        for filename in os.listdir(selected_folder_path):
            if filename.endswith(".mp3"):
                lbox.insert(tk.END, filename)

def previous_song():
    if len(lbox.curselection())>0:
        current_index=lbox.curselection()[0]
        if current_index>0:
            lbox.select_clear(0, tk.END)
            lbox.selection_set(current_index-1)
            play_selected_song()


def next_song():
    if len(lbox.curselection())>0:
        current_index=lbox.curselection()[0]
        if current_index < lbox.size()-1:
            lbox.selection_clear(0, tk.END)
            lbox.selection_set(current_index + 1)
            play_selected_song()

def play_music():
    global paused
    if paused:
        pygame.mixer.music.unpause()
        paused=False

    else:
        play_selected_song()

def play_selected_song():
    global current_position, paused
    if len(lbox.curselection()) > 0:
        current_index=lbox.curselection()[0]
        selected_song=lbox.get(current_index)
        full_path=os.path.join(selected_folder_path, selected_song)
        pygame.mixer.music.load(full_path) #load selected song
        pygame.mixer.music.play(start=current_position)
        paused=False
        audio=MP3(full_path)
        song_duration=audio.info.length
        pbar["maximum"]=song_duration

def pause_music():
    global paused
    pygame.mixer.music.pause()
    paused=True

def stop_music():
    global paused
    pygame.mixer.music.stop()
    paused=False

root=tk.Tk()
root.title("Music Player")
root.geometry("500x600")
root.configure(background="#CCCCFF")
root.resizable(False,False)

image_icon= tk.PhotoImage(file="logo.png")
root.iconphoto(False,image_icon)

m_label=tk.Label(root,text="MUSIC PLAYER", font=("Times new roman",25, "bold"))
m_label.pack(pady=10)
m_label.config(bg="#CCCCFF")

#button for to select music folder
btn1=ctk.CTkButton(root, text="Select Music Folder",
                   command=select_music_folder,
                   font=("TkDefaultFont", 18))
btn1.pack(pady=20)

#list box for songs
lbox=tk.Listbox(root, width=50,bg="#5D6D7E", fg="black", selectbackground="#CCCCFF",font=("Times new roman", 16,))
lbox.pack(pady=10)

# progress  bar
pbar=Progressbar(root,length=300,mode="determinate")
pbar.pack(pady=10)

#frame for buttons
btn_frame=tk.Frame(root)
btn_frame.pack(pady=20)
btn_frame.config(bg="#CCCCFF")

#previous button
pre_btn=ctk.CTkButton(btn_frame, text="<", command=previous_song,
                     width=50, font=("TkDefaultFont", 18))
pre_btn.pack(side=tk.LEFT, padx=5)

#play button
play_btn=ctk.CTkButton(btn_frame, text="Play", command=play_music, 
                       width=50, font=("TkDefaultFont",18))
play_btn.pack(side=tk.LEFT, padx=5)

#pause button
pause_btn=ctk.CTkButton(btn_frame, text="Pause", command=pause_music,
                        width=50, font=("TkDefaultFont", 18))
pause_btn.pack(side=tk.LEFT, padx=5)

#button to play next song
next_btn=ctk.CTkButton(btn_frame, text=">", command=next_song, width=50,
                       font=("TkDefaultFont", 18))
next_btn.pack(side=tk.LEFT, padx=5)

root.mainloop()








