#!/python311/python

#     change font for messages

from tkinter import *
from tkinter.scrolledtext import ScrolledText
import fnmatch
import os
import re
import sqlite3
import sys
import tkinter as tk
import winsound

print('\n\n\nPackage basename:    ', os.path.basename(__file__))
print('Package dirname:     ', os.path.dirname(__file__))

class Certification_Question_Insert():

	def __init__(self, db_name):
		super().__init__()
		self.debug=False
		self.test_form = ["""Who prevail in 2024?""","""Greg\nBiden\nConvicted Felon Orange\nSara\nNone of the above\n""","I can't envision any result except for Biden.", "c:\Greg\Scripts\sunburst.png", "c:\Greg\Scripts\tabbed.csv"]    #'
		self.mygrid = {
			"Clear Form":[2,5,1,10],
			"Exit":[3,5,1,10],
			"Insert Record":[1,5,1,10],
			"Question:":[1,0,1,20],
			"Answers:":[3,0,1,20],
			"Explanation:":[7,0,1,20],
			"Image File:":[11,0,1,20],
			"Data File:":[12,0,1,20],
			"Certification Family:":[0,0,1,20],
			}

		self.mainwin = Tk(screenName="Greg", baseName="Roeper", className='Tk', useTk=True, sync=False, use=None)
		#help (self.mainwin)
		self.mainwin.title("Certification Question Entry")
		self.conn = sqlite3.connect(db_name)
		self.cursor = self.conn.cursor()
		self.menubar = Menu(self.mainwin)
		self.mainwin.config(menu=self.menubar)

		self.fileMenu = Menu(self.menubar, tearoff=False)
		self.submenu = Menu(self.fileMenu)
		self.submenu.add_command(label="New feed")
		self.submenu.add_command(label="Bookmarks")
		self.submenu.add_command(label="Mail", command=self.onExit)
		self.submenu2 = Menu(self.fileMenu)
		self.submenu2.add_command(label="New feed")
		self.submenu2.add_command(label="Bookmarks")
		self.submenu2.add_command(label="Mail", command=self.onExit)
		self.fileMenu.add_cascade(label='Import', menu=self.submenu, underline=0)
		self.fileMenu.add_separator()
		self.fileMenu.add_cascade(label='Export', menu=self.submenu2, underline=0)
		self.fileMenu.add_separator()
		self.fileMenu.add_command(label="Exit", underline=0, command=self.onExit)
		self.menubar.add_cascade(label="Options", underline=0, menu=self.fileMenu)
		self.menubar.add_cascade(label="Jobs", underline=0, menu=self.fileMenu)
		self.menubar.add_cascade(label="Help", underline=0, menu=self.fileMenu)
		self.menubar.add_cascade(label="Select Family", underline=0, menu=self.fileMenu)

		self.addLabel("Certification Family:")
		#Label(self.mainwin, text="Certification Family", anchor="e", width=20).grid(row=0, column=0)
		self.certification_family = Text(self.mainwin, height=1, width=20);
		self.certification_family.grid(row=0, column=1, padx=10, pady=2,columnspan=3, sticky="W")

		self.addLabel("Question:")
		#Label(self.mainwin, text="Question:", anchor="e", width=20).grid(row=1, column=0)
		self.question_text = ScrolledText(self.mainwin, height=5, width=60);
		self.question_text.grid(row=1, column=1, padx=10, pady=10, rowspan=2, columnspan=2, sticky="N")
	  #DD
		self.addLabel("Answers:")
		#DDLabel(self.mainwin, text="Answers:", anchor="e", width=20).grid(row=2, column=0)
		self.answer_text = ScrolledText(self.mainwin, height=10, width=60);
		self.answer_text.grid(row=3, column=1, padx=10, pady=10, rowspan=4, columnspan=2, sticky="N")

		self.addLabel("Explanation:")
		self.explanation_text = ScrolledText(self.mainwin, height=8, width=60);
		self.explanation_text.grid(row=7, column=1, padx=10, pady=10, rowspan=4, columnspan=2, sticky="N")

		self.addLabel("Image File:")
		#Label(self.mainwin, text="Image File 11:", anchor="e", width=20).grid(row=11, column=0)
		self.image_file = Text(self.mainwin, height=1, width=40);
		self.image_file.grid(row=11, column=1, padx=10, pady=10, sticky="W")

		self.addLabel("Data File:")
		#Label(self.mainwin, text="Data File  12:", anchor="e", width=20).grid(row=12, column=0)
		self.data_file = Text(self.mainwin, height=1, width=40);
		self.data_file.grid(row=12, column=1, padx=10, pady=10, sticky="W")

	  # Do no use addLabel because we need to update the label during processing
		self.lbl_messages = Label(self.mainwin, text='Messages will appear here', anchor="center", height=10, width=60)
		self.lbl_messages.grid(row=13, column=0, padx=30, pady=10, columnspan=2)

		if True:
			self.question_text.insert(END, self.test_form[0])
			self.answer_text.insert(END, self.test_form[1])
			self.explanation_text.insert(END, self.test_form[2])
			self.image_file.insert(END, self.test_form[3])
			self.data_file.insert(END, self.test_form[4])

		self.addButton("Clear Form", self.clearform)
		self.addButton("Exit",self.onExit)
		self.addButton("Insert Record", self.insert_records)

		flist = self.get_families()
		self.optVariable = StringVar(self.mainwin)
		self.optVariable.set("Available Families") # default value
		optFiles = OptionMenu(self.mainwin, self.optVariable,*flist).grid(row=0, column=2, sticky="W", padx=10, pady=10)
		self.optVariable.trace('w', self.change_family)

		self.mainwin.mainloop()


	def onExit(self):

		quit(self)

	def addButton(self, intxt, incmd):
	    Button(self.mainwin, text=intxt
	    		, command=incmd).grid(row=self.mygrid[intxt][0]
						, column=self.mygrid[intxt][1]
						, sticky="EW", padx=10, pady=10)

	def addLabel(self, intxt):
			Label(self.mainwin, text=intxt, anchor="e"
				, width=self.mygrid[intxt][3]).grid(row=self.mygrid[intxt][0], column=self.mygrid[intxt][1])

	def message(self,inval):
			#print(inval)
			self.lbl_messages['text']  = inval

	def clearform(self):
			self.question_text.delete(1.0, END)
			self.answer_text.delete(1.0, END)
			self.explanation_text.delete(1.0, END)
			self.image_file.delete(1.0, END)
			self.data_file.delete(1.0, END)

	def get_families(self):
		outlist = []
		rows = self.cursor.execute("Select distinct(FAMILY) from questions;")
		for foo in rows:
			outlist.append(foo[0])
		return outlist

	def change_family(self,*args):
		#print(args)
		self.certification_family.delete(1.0, END)
		self.certification_family.insert(1.0, self.optVariable.get())

	def insert_records(self):
		question = self.question_text.get(1.0, END).strip().replace("'","''")
		explanation = self.explanation_text.get(1.0, END).strip().replace("'","''")
		family = self.certification_family.get(1.0, END).strip().replace("'","''")
		image = self.image_file.get(1.0, END).strip().replace("'","''")
		data = self.data_file.get(1.0, END).strip().replace("'","''")
		answers = self.answer_text.get(1.0, END).strip()

		if len(family) == 0 or len(question) == 0 or len(answers) == 0:
			self.message(f"Family, Question, and Answers must be provided")
			winsound.Beep(1500, 700)
			return

		cmd = f"""insert into questions
		(QID,FAMILY,TEXT,EXPLANATION,IMAGE_FILE,DATA_FILE,CREATED_TS,LAST_ASKED_TS,LAST_ANSWER,ANSWERED_CORRECTLY)
		values (NULL
		, '{family}'
		, '{question}'
		, '{explanation}'
		, '{image}'
		, '{data}'
		, current_timestamp
		, current_timestamp
		, ''
		, False
		);"""
		print(cmd)
		if not self.debug:
				self.cursor.execute(cmd)
				self.conn.commit()
		cmd = f"Select max(QID) from questions where FAMILY = '{family}';"
		rows = self.cursor.execute(cmd)
		for foo in rows:
			current_id = foo[0]
		if current_id is None:
			self.message(f"ERROR retrieving QID")
			return
		print("Current ID = ", current_id)
		
		for foo in answers.split("\n"):
			answer = foo.replace("'","''")
			bullets = re.findall('^[A-H]\.',answer)
			if len(bullets) > 0:
				answer = answer[2:].strip()
			if answer.lower().find("~correct") > -1:
				answer = answer.replace("~correct","")
				TF="True"
			else:
				TF="False"

			cmd = f"""insert into answers

		(QID,TEXT,CORRECT,CREATED_TS)
		values ({current_id}
		, '{answer}'
		, {TF}
		, current_timestamp
		);"""

			print(cmd)
			if not self.debug:
				self.cursor.execute(cmd)
		self.conn.commit()
		self.clearform()
		self.message(f"Question # {current_id} has been inserted")
	

if __name__ == '__main__':
	frame = Certification_Question_Insert(r'c:\Greg\DEV\dev_certification_practice.db')
	exit()

