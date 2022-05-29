import os
import threading
from time import sleep
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from mutagen.mp3 import MP3
from pygame import mixer
from ttkthemes import themed_tk as tk

root = tk.ThemedTk()
root.get_themes()
root.set_theme("plastik")
root.title('Musico')
root.geometry('+300+150')
root.resizable(False, False)
root.iconbitmap(r'musico.ico')  # app logo

# some required variables
mixer.init()  # initializing the mixer
index = 0
paused = False
muted = False
volume = IntVar()
playlist_path = []


# all_comments
# playlist : contains file names only
# playlist_path : contains full file paths (mixer needs file path to play music)

def show_details(song_path):
    namelabel.config(text=os.path.basename(song_path))
    filestring = os.path.splitext(song_path)

    if filestring[1] == '.mp3':
        audio = MP3(song_path)
        total_length = audio.info.length
    else:
        song = mixer.Sound(song_path)
        total_length = song.get_length()

    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel.config(text=timeformat)

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global paused
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            countdownlabel.config(text=timeformat)
            sleep(1)
            current_time += 1


def play():
    global paused
    global playlist_path
    if paused:
        mixer.music.unpause()
        statusbar.config(text='Playing - ' + os.path.basename(filepath))
        paused = False
    else:
        try:
            mixer.music.stop()
            sleep(1)
            if playlist.curselection() != ():  # if there's a selection
                selected_song = playlist.curselection()
                selected_song = int(selected_song[0])
                song = str(playlist_path[selected_song])
                mixer.music.load(song)
                mixer.music.play()
                mixer.music.set_volume(scale.get() / 100)
                statusbar.config(text='Playing - ' + os.path.basename(song))
                show_details(song)
            else:
                song = str(playlist_path[0])
                mixer.music.load(song)
                mixer.music.play()
                mixer.music.set_volume(scale.get() / 100)
                statusbar.config(text='Playing - ' + os.path.basename(song))
                show_details(song)
        except:
            browse_file()
            play()


def pause():
    global paused
    paused = True
    mixer.music.pause()
    statusbar.config(text='Music Paused..')


def stop():
    global paused
    mixer.music.stop()
    statusbar.config(text='Music stopped')
    paused = False
    countdownlabel.config(text='00:00')


def rewind():
    try:
        stop()
        play()
    except:
        browse_file()
        play()


def mute():
    global muted
    if muted:
        mixer.music.set_volume(int(volume.get()) / 100)
        scale.set(volume.get())
        b_volume.config(image=imgvolume)
        muted = False
    else:
        volume.set(scale.get())
        mixer.music.set_volume(0)
        scale.set(0)
        b_volume.config(image=imgmute)
        muted = True


def set_vol(var):
    global muted
    b_volume.config(image=imgvolume)
    muted = False
    volume = scale.get() / 100
    mixer.music.set_volume(volume)


def hot_keys():
    messagebox.showinfo(title=root.title(), message='''Tap 'Enter' to Pause/Play music
Tap 'm' to mute/unmute volume
Tap 'Esc' to Stop music
That's all :P''')


def about_us():
    messagebox.showinfo(title="About " + root.title(), message='''This App was writen by Isaac Omodia,
during the #100DaysOfCode challenge.
Contact the developer at : isaacomodia@gmail.com''')


def browse_file():
    global filepath
    filepath = filedialog.askopenfilename()
    add_to_playlist(filepath)


def add_to_playlist(path):
    global index
    global playlist_path
    name = os.path.basename(path)
    if name in playlist.get(0, END):
        pass
    else:
        playlist.insert(index, name)
        playlist_path.insert(index, path)
    index += 1


def del_song():
    try:
        selected_song = playlist.curselection()
        selected_song = int(selected_song[0])
        playlist.delete(selected_song)
        playlist_path.pop(selected_song)
    except:
        pass


def pause_play():
    global paused
    if not playlist_path:
        play()
    else:
        if not paused and mixer.music.get_busy():
            pause()
        else:
            play()


def on_closing():
    mixer.music.stop()
    root.destroy()


menubar = Menu(root)
file = Menu(menubar, tearoff=0)
help_ = Menu(menubar, tearoff=0)
root.config(menu=menubar)
menubar.add_cascade(menu=file, label='File')
menubar.add_cascade(menu=help_, label='Help')
file.add_command(label='Open', command=browse_file)
file.add_separator()
file.add_command(label='Exit', command=root.destroy)
help_.add_command(label='Hot keys', command=hot_keys)
help_.add_command(label='About Us', command=about_us)

statusbar = ttk.Label(root, text='Welcome to ' + root.title(), relief=SOLID, font='Times 12 italic')
statusbar.pack(side=BOTTOM, fill=X)

leftframe = Frame(root, padx=30, pady=0)
leftframe.pack(side=LEFT)

playlist = Listbox(leftframe, width=22)
playlist.pack()

b_add = ttk.Button(leftframe, text='Add', command=browse_file)
b_add.pack(side=LEFT)

b_remove = ttk.Button(leftframe, text='Remove', command=del_song)
b_remove.pack(side=LEFT)

rightframe = Frame(root)
rightframe.pack()

topframe = Frame(rightframe)
topframe.pack()

namelabel = ttk.Label(topframe, text='Welcome to ' + root.title())
namelabel.pack(pady=10)

lengthlabel = ttk.Label(topframe, text='--:--')
lengthlabel.pack()

countdownlabel = ttk.Label(topframe, text='--:--')
countdownlabel.pack()

middleframe = Frame(rightframe)
middleframe.pack(pady=10)

imgplay = PhotoImage(file=r'play.png')
b_play = ttk.Button(middleframe, image=imgplay, command=play)  # , relief=FLAT)
b_play.grid(row=0, column=0, padx=10)

imgpause = PhotoImage(file=r'pause.png')
b_pause = ttk.Button(middleframe, image=imgpause, command=pause)  # , relief=FLAT)
b_pause.grid(row=0, column=1, padx=10)

imgstop = PhotoImage(file=r'stop.png')
b_stop = ttk.Button(middleframe, image=imgstop, command=stop)  # , relief=FLAT)
b_stop.grid(row=0, column=2, padx=10)

bottomframe = Frame(rightframe)
bottomframe.pack(padx=30, pady=10)

imgrewind = PhotoImage(file=r'rewind.png')
b_rewind = ttk.Button(bottomframe, image=imgrewind, command=rewind)  # , relief=FLAT)
b_rewind.grid(row=0, column=0, padx=30, pady=35)

imgmute = PhotoImage(file=r'mute.png')
imgvolume = PhotoImage(file=r'volume.png')
b_volume = ttk.Button(bottomframe, image=imgvolume, command=mute)  # , relief=FLAT)
b_volume.grid(row=0, column=1)

scale = ttk.Scale(bottomframe, from_=0, to=99, value=60, orient=HORIZONTAL, command=set_vol)
scale.grid(row=0, column=2, padx=10)

root.bind_all('<Return>', lambda e: pause_play())
root.bind_all('<Escape>', lambda e: stop())
root.bind_all('<m>', lambda e: mute())
# root.bind_all('<space>', lambda e: pause_play())
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
