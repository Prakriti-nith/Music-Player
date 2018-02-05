#import tkinter
from Tkinter import *
from tkFileDialog import *
import pyglet
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import urllib2
import googlesearch
import time  
from time import sleep  
#import pygame

fileName = []
songName = []
source = None
k = 0
i = 0
player = pyglet.media.Player()
FORWARD_REWIND_JUMP_TIME = 10

def playMusic():
	player.play()
	# while True:
	# 	if source: #lyrics
	# 		if player.time in range(source.duration - 2, source.duration):
	# 			showLyrics()

def pauseMusic():
	player.pause()

def nextMusic():
	player.next()
	if source: # if player.queue not empty
		showLyrics()
	
def add_to_queue(audio_file):
	global source
	source = pyglet.media.load(audio_file)
	player.queue(source)
	print(source)
	print type(source)

def reset_player():
	global player
	player.pause()
	player.delete()
	player = pyglet.media.Player()

def is_playing():
	try:
		elapsed_time = int(player.time)
		is_playing = elapsed_time < int(track_length)
	except:
		is_playing = False
	return is_playing

def seek(time):
	try:
		player.seek(time)
	except AttributeError:
		pass

@property
def track_length():
	try:
		return source.duration
	except AttributeError:
		return 0

@property
def volume():
	return player.volume

@property
def elapsed_play_duration():
	return player.time

def stop():
	reset_player()
	T.configure(state='normal')
	playlist.configure(state='normal')
	playlist.delete('1.0',END)
	T.delete('1.0',END)
	T.configure(state='disabled')
	playlist.configure(state='disabled')
	k = 0
	i = 0
	fileName.clear()
	songName.clear()

def mute():
	player.volume = 0.0

def unmute(newvolume_level):
	player.volume = newvolume_level

def fast_forward():
	time = player.time + FORWARD_REWIND_JUMP_TIME
	try:
		if source.duration > time:
			seek(time)
		else:
			seek(source.duration)
	except AttributeError:
		pass

def rewind():
	time = player.time - FORWARD_REWIND_JUMP_TIME
	try:
		seek(time)
	except:
		seek(0)

def lyricsScratch(songName):
	query = songName + ' az lyrics'
	for j in googlesearch.search(query, tld='com', lang='en', num=10, stop=1, pause=2.0):
		print(j)
		if 'https://www.azlyrics.com/lyrics/' in j:
				link = j
				print j+' hi'
				break
	
	#manager = urllib3.PoolManager()
	#page = manager.request('GET',link)
	# page = requests.get('https://www.azlyrics.com/lyrics/shayneward/nopromises.html')
	page=urllib2.urlopen(link)
	soup = BeautifulSoup(page, 'html.parser')

	parentDiv = soup.find('div',class_ = 'col-xs-12 col-lg-8 text-center')
	#print parentDiv
	lyrics = list(parentDiv.children)[12].get_text()
	indexLyricsNotReq = lyrics.find('if  (')
	if indexLyricsNotReq != -1:
		lyrics = lyrics[0:indexLyricsNotReq]
	return lyrics

def browsefunc():
	global fileName
	global player
	global songName,k,i
	filePath = askopenfilename(parent=window)
	fileName.append(filePath)
	add_to_queue(filePath)
	p = Path(fileName[i])
	i = i+1
	playlist.configure(state='normal')	
	playlist.insert(END, "\n" + p.name)
	playlist.configure(state='disabled')

	if k==0:
		showLyrics()
	# if source:
	# 	duration = (player.source).duration
	# else:
	# 	duration = 100
	# pygame.mixer.music.load(filename[k])

def showLyrics():
	global k
	p = Path(fileName[k])
	songName.append(p.name)
	lyrics = lyricsScratch(songName[k])
	#print type(lyrics)
	T.configure(state='normal')	
	T.delete('1.0',END)
	T.insert(END, lyrics)
	T.configure(state='disabled')
	k = k+1
	#print filename
	
if __name__ == '__main__':
	window = Tk()
	window.resizable(width=False, height=False)
	window.wm_title("Music War")
	#pyglet.options['audio'] = ('pulse','openal','silent')
	
	open_song = PhotoImage(file='open-folder.png')
	openSong = Button(window, image = open_song, command = browsefunc)
	play_button=PhotoImage(file='play-button.png')
	play = Button(window, image = play_button, command = playMusic)
	pause_button=PhotoImage(file='pause-button.png')
	pause = Button(window, image =pause_button, command = pauseMusic)
	next_button=PhotoImage(file='right-chevron.png')
	next = Button(window, image =next_button, command = nextMusic)
	fast_button = PhotoImage(file='fast-forward.png')
	fastButton = Button(window, image = fast_button, command = fast_forward)
	rewind_button = PhotoImage(file='rewind.png')
	rewindButton = Button(window, image = rewind_button, command = rewind)
	stop_button = PhotoImage(file='stop.png')
	stopButton = Button(window, image = stop_button, command = stop)
	# unmute_button = PhotoImage(file='unmute.png')
	# unmuteButton = Button(window, image = unmute_button, command = unmute(0.6))

	T = Text(window,state = 'disabled', height=30, width=60)
	T.pack(padx=2, pady=0,side=LEFT)

	playlist = Text(window,state = 'disabled', height=30, width=30)
	playlist.pack(padx=2,pady=0,side= LEFT)

	openSong.pack(padx=5,pady=10,side=TOP)
	play.pack(padx=5,pady=10,side=TOP)
	pause.pack(padx=5,pady=10,side=TOP)
	next.pack(padx=5,pady=10,side=TOP)
	fastButton.pack(padx=5,pady=10,side=TOP)
	rewindButton.pack(padx=5,pady=10,side=TOP)
	stopButton.pack(padx=5,pady=10,side=TOP)
	# muteButton.pack(padx=5,pady=10,side=TOP)
	# unmuteButton.pack(padx=5,pady=10,side=TOP)
	window.mainloop()

#pyglet.app.run()
