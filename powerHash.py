#!/usr/bin/env python

from Tkinter import *
from ttk import *
from Tkinter import Frame
import tkFileDialog
import os

from os.path import isfile, join
import hashlib
import csv
import random


BUF_SIZE = 65536
#creates the 15^10 hash and randomises the characters
def gen_salt(length):
	pool = "1234567890abcde"
	return ''.join(random.choice(pool) for i in range(length))

def read_hash(file_list):
	salt_list = []
	
	for file in file_list:
		with open(file, 'rb') as fh:
			fh.seek(-1024, 2)
			last = fh.readlines()[-1][-10:]
			salt_list.append(last)
	hashes =  '\n'.join(salt_list)
	return hashes


def hash(file_list):
	salt_list = []
	for file in file_list:
		salt = gen_salt(10)
		with open(file, 'ab') as f:
			f.write(salt)
		salt_list.append(salt)
	hashes =  '\n'.join(salt_list)
	basenames = [os.path.basename(file) for file in file_list]
	hash_list = hashes.replace("\n", ",").split(',')
	
	package = zip(file_list, basenames,salt_list)	

	return hashes, package


#sets the base of the GUI
class FirstPanel(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent, background='white')
		
		file_label = Label(self, text="Select file", background="#d3d3d3")
		file_label.place(x=25,y=40)
		self.file_select_button = Button(self, text="Select file", command=self.openfile)
		self.file_select_button.place(x=120, y=30)
		
		self.file_location = Entry(self, background="#d3d3d3", width=50)
		self.file_location.place(x=25, y=70)
		
		
		self.hash_result = Text(self, background="#d3d3d3", width=40, height=4)
		self.hash_result.place(x=25, y=100)
		

		
		self.hash_status = Label(self)
		self.hash_status.place(x=25, y=170)
		
		self.pack(fill=BOTH, expand=1)
		
		self.file_opt = options = {}
		options['filetypes'] = [('all files', '.*')]
		options['initialdir'] = os.getcwd()
		options['parent'] = self
		options['title'] = 'Select File'
		
		
	def openfile(self):
		
		self.hash_status['text'] = ""
		filename = tkFileDialog.askopenfilename(**self.file_opt)
		path =os.path.abspath(filename)
		files_list = []
		files_list.append(path)
		
		self.hash = hash(files_list)
		self.file_location.delete(0,END)
		self.file_location.insert(0,path)
		self.hash_result.delete(1.0, END)
		self.hash_result.insert(1.0, self.hash[0])
		self.hash_status['text'] = "Hashing complete!"
		
#builds on top of the first layer of the GUI
class SecondPanel(Frame):
	
	def __init__(self, parent):
		Frame.__init__(self, parent, background='white')
		
		file_label = Label(self, text="Select folder", background="#d3d3d3")
		file_label.place(x=25,y=40)
		self.file_select_button = Button(self, text="Select folder", command=self.opendir)
		self.file_select_button.place(x=120, y=30)
		
		self.file_location = Entry(self, background="#d3d3d3", width=50)
		self.file_location.place(x=25, y=70)
		
		self.hash_result = Text(self, background="#d3d3d3", width=40, height=4)
		self.hash_result.place(x=25, y=90)
		
		self.hash_status = Label(self)
		self.hash_status.place(x=25, y=170)
		
		self.pack(fill=BOTH, expand=1)
		
		self.dir_opt = options = {}
		options['initialdir'] = os.getcwd()
		options['mustexist'] = False
		options['parent'] = self
		options['title'] = 'Select Folder'
		
		self.file_opt = options = {}
		options['initialdir'] = os.getcwd()
		options['filetypes'] = [('csv files', '.csv')]
		options['parent'] = self
		options['title'] = 'Select Folder'
		
		self.pack(fill=BOTH, expand=1)
		

		
		
        #open directory button
	def opendir(self):
		path =  tkFileDialog.askdirectory(**self.dir_opt)
		
		self.files_list = [(join(path,f)) for f in os.listdir(path) if isfile(join(path, f))]
		
		self.hash = hash(self.files_list)
		self.file_location.delete(0,END)
		self.file_location.insert(0,path)
		self.hash_result.delete(1.0, END)
		self.hash_result.insert(1.0, self.hash[0])
		self.hash_status['text'] = "Hashing complete! " + str(len(self.files_list)) + " files"
		
		self.export_button = Button(self, text="Export to CSV", command=self.csv)
		self.export_button.place(x=25, y=200)
		
        #csv generation
	def csv(self):
		filename = tkFileDialog.asksaveasfile(**self.file_opt)
		writer = csv.writer(filename, delimiter = ',')
		writer.writerow( ('File path', 'File name', 'PowerHash'))
		for i in range(len(self.hash[1])):
			writer.writerow((self.hash[1][i][0], self.hash[1][i][1], self.hash[1][i][2]))
		filename.close()
#builds on top of first and second layers of GUI
class ThirdPanel(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent, background='white')
		
		file_label = Label(self, text="Select file", background="#d3d3d3")
		file_label.place(x=25,y=40)
		self.file_select_button = Button(self, text="Select file1", command=self.openfile1)
		self.file_select_button.place(x=120, y=30)
		
		
		file_label2 = Label(self, text="Select file", background="#d3d3d3")
		file_label2.place(x=25,y=70)
		self.file_select_button2 = Button(self, text="Select file2", command=self.openfile2)
		self.file_select_button2.place(x=120, y=60)
		
		
		self.file_location = Text(self, background="#d3d3d3", width=40, height=4)
		self.file_location.place(x=25, y=90)
		
		self.hash_result = Text(self, background="#d3d3d3", width=40, height=4)
		self.hash_result.place(x=25, y=170)
		
		
		self.hash_status = Label(self, text="", background="#d3d3d3")
		self.hash_status.place(x=25,y=250)
		
		self.file1 = ""
		self.file2 = ""
		
		
		self.compare_button = Button(self, text="Compare", command=self.compare)
		self.compare_button.place(x=25,y=280)
		
		self.compare_status = Label(self, text="", background="#d3d3d3")
		self.compare_status.place(x=25,y=320)
		
		self.pack(fill=BOTH, expand=1)
		
		self.file_opt = options = {}
		options['filetypes'] = [('all files', '.*')]
		options['initialdir'] = os.getcwd()
		options['parent'] = self
		options['title'] = 'Select File'
		
		self.pack(fill=BOTH, expand=1)
		
	
		
	def openfile1(self):
		filename = tkFileDialog.askopenfilename(**self.file_opt)
		self.file_location.delete(1.0,END)
		self.file1 = os.path.abspath(filename)
		self.file_location.insert(1.0, self.file1 + '\n' + self.file2)
	
	def openfile2(self):
		filename = tkFileDialog.askopenfilename(**self.file_opt)
		self.file2 = os.path.abspath(filename)
		self.file_location.delete(1.0,END)
		self.file_location.insert(1.0, self.file1 + '\n' + self.file2)
		
	def compare(self):
		self.hash_result.delete(1.0,END)
		files_list = [self.file1, self.file2]
		hashes = read_hash(files_list)
		self.hash_result.insert(1.0,hashes)
		hash_list = hashes.replace("\n", ",").split(",")
		if hash_list[0] == hash_list[1]:
			self.compare_status['text']  = "Collision detected!"
		else:
			self.compare_status['text'] = "No collision detected"
		self.hash_status['text'] = "Hashing complete!"
			
		
	
		
#GUI dialogue box
class NotebookDemo(Frame):
	
	def __init__(self, isapp=True, name='powerhash'):
		Frame.__init__(self, name=name)
		self.pack(expand=Y, fill=BOTH)
		self.master.title('PowerHash')
		self.isapp = isapp
		self._create_widgets()
		
		
	def _create_widgets(self):
		self._create_demo_panel()
	
	def _create_demo_panel(self):
		demoPanel = Frame(self, name='demo',width=400, height=600)
		demoPanel.pack(side=TOP, fill=BOTH, expand=Y)
		nb = Notebook(demoPanel, name='notebook')
		nb.enable_traversal()
		nb.pack(fill=BOTH, expand=Y, padx=2, pady=3)
		self.create_first_tab(nb)
		self.create_second_tab(nb)
		self.create_third_tab(nb)
		
	def create_first_tab(self, nb):
		frame = FirstPanel(nb)
		nb.add(frame, text='Single File', underline=0, padding=2)
		
	def create_second_tab(self, nb):
		
		frame = SecondPanel(nb)
		nb.add(frame, text='Multiple Files', underline=0, padding=2)
		
	def create_third_tab(self, nb):
		frame = ThirdPanel(nb)
		nb.add(frame, text='Compare Two Files', underline=0)


if __name__ == '__main__':
	root = Tk()
	root.geometry("500x400")
	app = NotebookDemo(root)
	root.resizable(width=TRUE, height=TRUE)
	root.mainloop()
