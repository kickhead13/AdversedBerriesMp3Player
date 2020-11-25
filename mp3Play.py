from tkinter import *
import pygame
from tkinter import filedialog
from tkinter import ttk
from tkinter.font import Font
from mutagen.mp3 import MP3
import os

color = "white"
last = 0
playing=0
toprint= """                                                                  
   (     (                          (      (                          
   )\    )\ )  )     (  (        (  )\ ) ( )\    (  (   (  (    (     
((((_)( (()/( /((   ))\ )(  (   ))\(()/( )((_)  ))\ )(  )( )\  ))\(   
 )\ _ )\ ((_)|_))\ /((_|()\ )\ /((_)((_)|(_)_  /((_|()\(()((_)/((_)\  
 (_)_\(_)_| |_)((_|_))  ((_|(_|_))  _| | | _ )(_))  ((_)((_|_|_))((_) 
  / _ \/ _` |\ V // -_)| '_(_-< -_) _` | | _ \/ -_)| '_| '_| / -_|_-< 
 /_/ \_\__,_| \_/ \___||_| /__|___\__,_| |___/\___||_| |_| |_\___/__/ 
 """
print(toprint)

root = Tk()
root.title('Adveresed Berries v0.2')
root.geometry("900x750")
root["bg"] = color

#Initializeaza pygame
pygame.mixer.init()

#Creare master frame
master_frame=Frame(root)
master_frame["bg"] = color
master_frame.pack()


#creare volume frame
volume_frame=LabelFrame(master_frame, bg=color)
volume_frame.grid(row=2, column=0)

#Creare lista de melodii
song_box= Listbox(master_frame, bg="black", fg="white", font=Font(size=14), width=80, height=25, selectbackground="white", selectforeground="black")
song_box.grid(row=0, column=0)


#INITIALIZARE FILE
with open('InfoSong.txt', 'r') as f:
    data = f.readlines()
    data[1] = '1\n'
with open('InfoSong.txt', 'w') as f:
    f.writelines(data)

with open('InfoVolume.txt', 'r') as f:
    cont1=f.readline()
    c=float(cont1)
    pygame.mixer.music.set_volume(c)

#MODULE
def add_to_playlist(file, song):
    with open(f'{file}', 'a') as fd:
        fd.write(f'{song}\n')

def find_set_playlist():
    with open('InfoSong.txt', 'r') as fd:
        data=fd.readlines()
    if data[3] == 1:
        return data[2]
    else:
        return 1



def add_song():
    song=filedialog.askopenfilename(initialdir=r'Aaudio', title="Choose song", filetypes=(("mp3 files", "*.mp3"),))
    song=song.replace("Aaudio", "")
    song = song.replace(".mp3", "")
    song_box.insert(END, song)

def existingSong(str):
    global last
    for i in range(last+1):
        if song_box.get(i)==str:
            return 1

    return 0

def add_songs():
    global last
    songs = filedialog.askopenfilenames(initialdir=r'Aaudio', title="Choose song", filetypes=(("mp3 files", "*.mp3"), ("mp4 files", "*.mp4"), ))
    for song in songs:
        sav = os.getcwd()
        sav = f'{sav}\Aaudio'
        sav = sav.replace(chr(92), "/")
        song = song.replace(f'{sav}/', "")
        song = song.replace(".mp3", "")
        if not existingSong(song):
            song_box.insert(END, song)
            last += 1

def Play():
    try:
        song = song_box.get(ACTIVE)
        song_sav=song
        song = f'Aaudio/{song}.mp3'
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=1)
        for i in range(20):
            if song_box.get(i) == song_sav:
                l=i
        global playing
        playing = l

    except:
        print("error 001: Audio file is not properly enconded")

def Last_Song():
    try:
        global playing
        cont = playing
        song = song_box.get(cont - 1)
        song = f'Aaudio/{song}.mp3'
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=1)
        song_box.selection_clear(0, END)
        song_box.activate(cont - 1)
        song_box.selection_set(cont - 1, last=None)
        cont = cont - 1
        playing-=1
    except:
        print("error 003: Next song is non-existent")

def Next_Song():
    try:
        global playing
        cont = playing
        song = song_box.get(cont + 1)
        song = f'Aaudio/{song}.mp3'
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=1)
        song_box.selection_clear(0, END)
        song_box.activate(cont + 1)
        song_box.selection_set(cont + 1, last=None)
        cont = cont + 1
        playing+=1
    except:
        print("error 003: Next song is non-existent")

def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())
    with open('InfoVolume.txt', 'w') as f:
        cont = f.write(f'{volume_slider.get()}')

def commandBlock(x):

    #Comanda .create
    if (x.find(".create ") != -1):
        x = x.replace(".create ", "")
        x= x + ".txt"
        print(x)
        with open(f'{x}', 'w') as fd:
            pass


    #Comanda .set (seteaza playlistul curent ca playlist principal)
    elif (x.find(".set ") != -1):
        x = x.replace(".set ", "")
        with open('InfoSong.txt', 'r') as fd:
            data = fd.readlines()
            data[2] = f'{x}\n'
            data[3] = '1\n'
        with open('InfoSong.txt', 'w') as f:
            f.writelines(data)
            print(data)

    #comanda .delete (sterge ori ultima melodie ori tot playlistul in functie de parametru dat)
    elif (x.find(".delete ") != -1):
        x = x.replace(".delete ", "")
        x = int(x)
        try:
            song_box.delete(x-1)
        except:
            print("Deleting error")

    #comanda .deletef (Sterge fila unde se afla lista cu PATH urile)
    elif(x.find(".deletef ") != -1):
        x=x.replace(".deletef ", "")
        os.remove(x)

    else:
        print("Unkown command")



def addtoplaylist():
    with open('InfoSong.txt', 'r') as f:
        data=f.readlines()
    if int(data[1]) >= 1:
        if int(data[1]) == 1:
            print('\nPlease use the ".help" command in case you don\'t know the commands. Some commands can delete important files if not used properly.')
        str=input("_>")
        commandBlock(str)

    data[1]=f'{int(data[1])+1}\n'
    with open('InfoSong.txt', 'w') as f:
        f.writelines(data)

def search_song():
    root2 = Tk()
    root2.title('Download a song from youtube')
    root2.geometry("400x100")

    controls_frame2 = Frame(root2)
    controls_frame2.grid(row=1, column=0, pady=5, padx=15)

    def Take_input():
        pass


    l = Label(root2, text="Download a MP3 File using an Youtube Link")
    inputtxt = Text(controls_frame2, height=1, width=25, font=Font(size=8),bg="light yellow")
    Display = Button(controls_frame2, height=1, width=5, text="Search", command=lambda: Take_input())

    l.grid(row=0, column =0)
    inputtxt.grid(row =1, column =1)
    Display.grid(row =1, column = 2)

    root2.mainloop()

def Stop():
    pygame.mixer.music.stop()



#imagini butoane de control
Last_Song_img=PhotoImage(file=r'Imagini\Last_Song.png')
Play_img=PhotoImage(file=r'Imagini\Play.png')
Skip_Song_img=PhotoImage(file=r'Imagini\Skip_Song.png')
Pause_img=PhotoImage(file=r'Imagini\Pause.png')
Add_song_img=PhotoImage(file=r'Imagini\Add_song.png')
Add_To_Playlist_img=PhotoImage(file=r'Imagini\AddToPlaylist.png')

#Frame pt butoane de control
controls_frame=Frame(master_frame)
controls_frame["bg"] =color
controls_frame.grid(row=1, column=0, pady=20)

#creare butoane de control
Last_Song_btn = Button(controls_frame, bg=color, image=Last_Song_img, borderwidth=0, command=Last_Song)
Last_Song_btn.grid(row=0, column =1, padx=10)

Play_btn = Button(controls_frame, bg=color,image=Play_img, borderwidth=0, command=Play)
Play_btn.grid(row=0, column =2, padx=10)

Skip_Song_btn = Button(controls_frame,bg=color, image=Skip_Song_img, borderwidth=0, command=Next_Song)
Skip_Song_btn.grid(row=0, column =3, padx=10)

Pause_btn = Button(controls_frame,bg=color, image=Pause_img, borderwidth=0, command=Stop)
Pause_btn.grid(row=0, column=4, padx=10)

Add_song_btn = Button(controls_frame, bg=color, image=Add_song_img, borderwidth=0, command=add_songs)
Add_song_btn.grid(row=0, column=5, padx=10)

Add_To_Playlist_btn= Button(controls_frame, bg=color, image=Add_To_Playlist_img, borderwidth=0, command=addtoplaylist)
Add_To_Playlist_btn.grid(row=0, column=6, padx=10)

#meniu
meniu=Menu(root, bg=color)
root.config(menu=meniu)

#Add song menu
add_song_menu=Menu(meniu)
meniu.add_cascade(label="Add Song", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song", command = add_song)
add_song_menu.add_command(label="Terminal", command=addtoplaylist)

#Add search menu
Search_song = Menu(meniu)
meniu.add_cascade(label="Seach song", menu=Search_song)
Search_song.add_command(label="Search Song", command =search_song)

#Volume slider
volume_slider=ttk.Scale(volume_frame, from_=0, to=1, orient=HORIZONTAL, value=c, command=volume, length=250)
volume_slider.pack()

with open('InfoCheck.txt', 'r') as f:
    l=f.readline()

root.mainloop()