#!/python311/python


#abadae
#c2f1f5
#e4e6e7

import argparse
import cv2
import os
import pathlib
import random
import re
import sqlite3
import sys
import textwrap
import time
import wx
from subprocess import Popen


import configparser
import os
import tkinter as tk
from tkinter import scrolledtext, ttk




class Main_Window(wx.Frame):
	def __init__(self, parent, title, arguments):
		self.background_color = "#f0f0f0"
		wx.Frame.__init__(self, parent, title = title, size = (1200,850), pos=(300,100))
		self.start_time = time.time()
		self.conn = sqlite3.connect(r'C:\Greg\dev\dev_certification_practice.db')
		self.cursor = self.conn.cursor()
		print(arguments.question_count)
		print(arguments.review_missed_questions)
		print(arguments.family)
		print(arguments.review_missed_questions)

		
		self.imagepath = r"c:\Greg\Alteryx\QuizImages"
		self.datapath = r"c:\Greg\Alteryx\QuizData"
		self.SetBackgroundColour(self.background_color)
		self.bullets = "ABCDEFGH"
		self.crlf = chr(10)+chr(13)
		self.randomize = True
		self.button_size = (200,20)

		font1 = wx.Font(10, family = wx.DECORATIVE, style = 0, weight = 90,underline = False, faceName ="", encoding = wx.FONTENCODING_DEFAULT)
		font2 = wx.Font(12, family = wx.DECORATIVE, style = 1, weight = 90,underline = False, faceName ="", encoding = wx.FONTENCODING_DEFAULT)
		font3 = wx.Font(14, 72, 0, 90, underline = False,faceName ="")

		row_offset = 300
		if False:
			count = 50
			while count < 1100:
				tic = wx.StaticText(self, pos=(10,count))
				tic.SetLabel(f"{count}")
				tic.SetFont(font1)
				tic.SetBackgroundColour(self.background_color)
				tic2 = wx.StaticText(self, pos=(count,10))
				tic2.SetLabel(f"{count}")
				tic2.SetFont(font1)
				tic2.SetBackgroundColour(self.background_color)

				count += 50
		self.answered_questions = 0
		self.question_number = 0
		self.question_header = wx.StaticText(self, name='question_header', style = wx.BORDER_DOUBLE | wx.ALIGN_CENTER| wx.ST_NO_AUTORESIZE, size=(650,30), pos=(40,20))
		self.question_header.SetLabel("Question")
		self.question_header.SetFont(font3)
		self.question_header.SetBackgroundColour(self.background_color)

		self.answer_header = wx.StaticText(self, name='answer_header', style = wx.BORDER_DOUBLE | wx.ALIGN_CENTER| wx.ST_NO_AUTORESIZE, size=(450,30), pos=(700,20))
		self.answer_header.SetLabel("Possible Answers")
		self.answer_header.SetFont(font3)
		self.answer_header.SetBackgroundColour(self.background_color)

		self.question_text = wx.StaticText(self, name='question_field'
			, style = wx.BORDER_DOUBLE | wx.TE_MULTILINE
			, size=(650,250), pos=(40,80)) #Text area with multiline
		self.question_text.SetFont(font1)
		self.question_text.SetBackgroundColour(self.background_color)
		self.question_text.SetLabel("\nGreg\n\t\tRoeper\n\t\t\trocks")

		self.user_message = wx.TextCtrl(self, name='message_field'
				, style = wx.TE_MULTILINE | wx.BORDER_DOUBLE | wx.TE_READONLY
				, size=(650,250), pos=(40,350)) #Text area with multiline
		self.user_message.SetBackgroundColour(self.background_color)

		self.checkboxes = {}

		checkboxy = 100
		for foo in self.bullets:
			self.checkboxes[foo] = wx.CheckBox(self, -1, label= " "*120, size=(175,25), pos=(900,checkboxy))
			checkboxy += 25

		##  Buttons
		self.submit_btn = wx.Button(self, label="Submit Answer", name="quit", size=(self.button_size), pos=(800,100))
		self.submit_btn.Bind(wx.EVT_BUTTON, self.CheckAnswers)

		self.NextQuestion_btn = wx.Button(self, label="Next Question", name="next",  size=(self.button_size), pos=(800,100))
		self.NextQuestion_btn.Bind(wx.EVT_BUTTON, self.NextQuestion)

		self.exit_btn = wx.Button(self, label="Exit", name="quit", size=(self.button_size), pos=(800,650))
		self.exit_btn.Bind(wx.EVT_BUTTON, self.OnExit)

		self.end_test_btn = wx.Button(self, label="End Test", name="quit", size=(self.button_size), pos=(800,675))
		self.end_test_btn.Bind(wx.EVT_BUTTON, self.ShowResults)

		self.reset_exam_btn = wx.Button(self, label=" Restart Exam", name="quit", size=(self.button_size), pos=(800,700))
		self.reset_exam_btn.Bind(wx.EVT_BUTTON, self.ResetBoard)

		#self.show_notes = wx.CheckBox(self, -1, label= "Show Explanation if Available", pos=(100,880))
		self.show_mistakes = wx.CheckBox(self, -1, label= "Show Wrong Answers During Test", pos=(100,700))
		self.number_of_questions = wx.TextCtrl(self, name='message_field'
				, style = wx.BORDER_DOUBLE
				, size=(40,25), pos=(100,750))

		self.lbl1 = wx.StaticText(self, name='lbl1'
			, style = wx.BORDER_DOUBLE | wx.ALIGN_CENTER| wx.ST_NO_AUTORESIZE
			, size=(150,25), pos=(140,750))
		self.lbl1.SetLabel("# of questions")


		self.correct_answers = self.correct_count = self.question_number = 0

		self.questions = []

		self.max_questions = 10
		self.debug_level = 0
		self.review = False
		self.family = arguments.family
		
		if arguments.question_count:
			self.max_questions = arguments.question_count
		self.number_of_questions.ChangeValue(str(self.max_questions))

		if arguments.debug_level:
			self.debug_level = arguments.debug_level

		if arguments.review_missed_questions:
			self.review = True


		self.ResetBoard(None)

	##########################################################################################
	def ResetBoard(self,event):

		self.ShowResults(event)
		self.start_time = time.time()
		self.missed_questions = ""
		self.question = {}
		self.answer_key = []
		self.explanation = []
		self.correct_count = 0
		#self.exit_btn.Hide()
		self.end_test_btn.Show()
		self.question_number = 0
		self.correct_answers = 0
		self.answer_dict = {}
		self.explanation_dict = {}
		self.question_number_list = []
		self.question_dict = {}
		self.answer_dict[0] = []
		self.explanation_dict[0] = []
		self.question_dict[0] = []

		self.question_id_array = []
		self.max_questions = 10

		inq = f"select qid from QUESTIONS where family = '{self.family}' order by RANDOM() limit {self.max_questions};"
		if self.review:
			inq = f"select qid from QUESTIONS where family = '{self.family}' and answered_correctly = False order by RANDOM();"
		rows = self.cursor.execute(inq).fetchall()
		for foo in rows:
			self.question_id_array.append(foo[0])
		if self.review:
			self.max_questions = len(rows)
			self.number_of_questions.ChangeValue(str(self.max_questions))


		#print (self.question_id_array)

		self.answered_questions = 0

		self.NextQuestion(None)

	##########################################################################################
	def ShowImage(self, photo):
		print(f"Displaying image {photo}")
		img = cv2.imread(photo, cv2.IMREAD_ANYCOLOR)
		cv2.imshow("Image", img)

	##########################################################################################
	def ShowWorkflow(self, workflow):
		print(f"opening {workflow}")
		cmd = [r"c:\Program Files\Alteryx\bin\AlteryxGui.exe", f"{self.datapath}\{workflow}"]
		print(cmd)
		print(cmd[0])
		print(cmd[1])
		try:
			Popen(cmd, shell=False, stdin=None,stdout=None, stderr=None, close_fds=True)
		except:
			pass
# FUNCTIONS
# ------------------------------------------------------------------------------

	##########################################################################################
	def SplitLongLine(self, intext, WRAP=82, INDENT="    "):

		if intext is None:
			return ""
		print("\n\n", intext) # DELETE ME
		#intext = f"{intext}{self.crlf}{self.crlf}{self.crlf}{intext}"     # DELETE ME
		lines = intext.split("\n")
		print(f"Length of split array = {len(lines)}")  # DELETE ME
		for foo in lines:
			print(">>>", foo)  # DELETE ME
		for foo in lines:
			self.LogMessage(f"New Line 1", 3)
			arrayed = intext.split(" ")
			outarray = []
			temptext = ""

			for bar in arrayed:
				if len(temptext) + len(bar) > WRAP:
					self.LogMessage(temptext, 3)
					self.LogMessage(f"   The length of the current question line is {len(temptext)}", 3)
					print("Adding outarray - length of temptext is", len(temptext))   # DELETE ME
					outarray.append(temptext)
					temptext = ""
					self.LogMessage("Temp Text is reset", 3)
					self.LogMessage(f"New Line 2", 3)
				temptext += bar + " "
			outarray.append(temptext)
			print("\n\n", outarray) # DELETE ME
			
		join_string = "\n" 
		return join_string.join(s for s in outarray)

	##########################################################################################
	def NextQuestion(self,event):
		if len(self.question_id_array) == 0:
			self.ShowResults(None)
			return
		self.answer_key = []
		self.explanation = []
		self.ResetAnswerKey()
		self.ResetCheckboxes()

		self.question = {"Question":"nah", "Explanation":"None", "Answers":[]}
		self.question_id = self.question_id_array.pop(0)

		## Query for next question
		rows = self.cursor.execute(f"select text, explanation, image_file, data_file from QUESTIONS where family = '{self.family}' and qid = {self.question_id};")
		for foo in rows:
			self.question["Question"] = foo[0]
			self.question["Explanation"] = foo[1]
			self.question["Image"] = foo[2]
			self.question["Data"] = foo[3]
		print("Question ID = ", self.question_id)

		## Query for answers
		aqry = f"select text, correct from ANSWERS where qid = {self.question_id} limit 8;"
		rows = self.cursor.execute(aqry)
		for foo in rows:
			self.question["Answers"].append({"Answer":foo[0], "Correct":foo[1]})

		self.question_header.SetLabel("Question %d out of %d" %(self.question_number+1,self.max_questions))

		temptext = (self.SplitLongLine(self.question['Question'],WRAP=120))
		self.question_text.SetLabel("\n" + 	temptext)

		temp_answers = []
		for bar in self.question['Answers']:
			temp_answers.append(bar)
		if self.randomize:
			random.shuffle(temp_answers)

		for foo in self.bullets:
			self.HideCheckbox(foo)

		positiony = 140
		for bar in range(len(self.question['Answers'])):
			#temptext = ("  %s.  %s" %(self.bullets[bar], self.SplitLongLine(temp_answers[bar]["Answer"],WRAP=62)))
			temptext = ("  %s. %s" %(self.bullets[bar], temp_answers[bar]["Answer"]))
			lines = int(len(temptext) / 60)
			newheight = 20 + lines * 17

			self.SetCheckLabel(self.bullets[bar], temptext)
			self.MoveCheckBox(self.bullets[bar], 750, positiony)
			self.SizeCheckBox(self.bullets[bar], newheight)
			positiony += newheight
			self.ShowCheckbox(self.bullets[bar])

			if temp_answers[bar]['Correct'] == "True" or temp_answers[bar]['Correct'] == 1:
				self.answer_key.append(self.bullets[bar])

		#self.submit_btn.Move(800, 340)
		#self.NextQuestion_btn.Move(800, 145)

		#self.HideExplanation()
		self.ShowSubmitBtn()
		self.HideNextQuestionBtn()

		if 'Image' in self.question.keys():
			if self.question['Image'] != "":
				fullpath = os.path.join(self.imagepath, self.question['Image'])
				self.ShowImage(fullpath)

		self.question_number += 1

		#self.ShowWorkflow("greggo.yxmd")
		self.Layout()
		self.Update()

	##########################################################################################
	def MoveCheckBox(self,keyvalue, x, y):
		self.checkboxes[keyvalue].Move((x,y))

	##########################################################################################
	def SizeCheckBox(self,keyvalue, height):
		self.checkboxes[keyvalue].SetSize(400,height)

	##########################################################################################
	def ShowResults(self,event):
		temptext = "\n\n\nShowing Results"

		for foo in self.bullets:
			self.HideCheckbox(foo)
		self.HideSubmitBtn()
		#self.question_header.SetLabel("Question %d out of %d" %(self.question_number+1,self.max_questions))
		self.correct_answers = self.correct_count
		elapsed = time.strftime("%H:%M:%S", time.gmtime(time.time() - self.start_time))
		temptxt = ""
		if self.answered_questions > 0:
			temptext += ("\n\n%d correct answer(s) out of %d	\n\n\t%.0f %%\n\n" %(self.correct_answers, self.answered_questions, 100*self.correct_answers/self.answered_questions))

		print(f"	Time: {elapsed}")

		self.question_text.SetLabel("\n" + 	temptext)
		self.Update()
		self.exit_btn.Show()
		self.NextQuestion_btn.Hide()
		print("Hiding end test button")
		self.end_test_btn.Hide()
		#self.HideExplanation()
		#self.Hide()
		self.Layout()
		self.Update()

	# ------------------------------------------------------------------------------
	def OnExit(self, event):
		self.Close(True) #Close the frame

	#----------------------------------------------------------------------
	def LogMessage(self, value, debug_level):
		if debug_level <= self.debug_level:
			print(value)

	#----------------------------------------------------------------------
	def SetCheckLabel(self, keyvalue, value):
		self.checkboxes[keyvalue].SetLabel(value.replace("(Correct)",""))

	#----------------------------------------------------------------------
	def HideNextQuestionBtn(self):
		self.NextQuestion_btn.Hide()

	#----------------------------------------------------------------------
	def ShowNextQuestionBtn(self):
		self.NextQuestion_btn.Show()

	#----------------------------------------------------------------------
	def HideSubmitBtn(self):
		self.submit_btn.Hide()

	#----------------------------------------------------------------------
	def ShowSubmitBtn(self):
		self.submit_btn.Show()

	#----------------------------------------------------------------------
	def HideCheckbox(self, keyvalue):
		self.checkboxes[keyvalue].Hide()

	#----------------------------------------------------------------------
	def ResetCheckboxes(self):
		for foo in self.checkboxes.keys():
			self.checkboxes[foo].SetValue(False)

	#----------------------------------------------------------------------
	def ShowCheckbox(self, keyvalue):
		self.checkboxes[keyvalue].Show()

	#----------------------------------------------------------------------
	def SetMessage(self, value):
		self.user_message.ChangeValue(value)

	#----------------------------------------------------------------------
	def AppendMessage(self, value):
		self.user_message.ChangeValue(f"{self.user_message.Value}\n\n{value}")

	#----------------------------------------------------------------------
	def HideExplanation(self):
		""""""
		#self.SetMessage("")

		self.Layout()
		self.Update()

	#----------------------------------------------------------------------
	def ResetAnswerKey(self):
		self.answer_key = []

	#----------------------------------------------------------------------
	def GetValue(self, inbox):
		return inbox.GetValue()

	#----------------------------------------------------------------------
	def CheckAnswers(self, event):

		self.SetMessage("")

		my_answer = ""
		self.answered_questions += 1
		for foo in self.checkboxes.keys():
			if self.GetValue(self.checkboxes[foo]):
				my_answer += foo

		output = "\n\n"
		explained = ""
		correct_answer = "".join(s for s in self.answer_key)
		#("*%s* ??? *%s*" %(correct_answer, my_answer))

		if correct_answer == my_answer:
			output += ("\nYou are correct!  The answer(s) are	 %s\n\n"  %",".join(s for s in self.answer_key))
			rows = self.cursor.execute(f"update QUESTIONS set LAST_ASKED_TS = current_timestamp, LAST_ANSWER = '{my_answer}',ANSWERED_CORRECTLY = True where family = '{self.family}' and qid = {self.question_id};")
			self.correct_count += 1
		else:
			output += ("\n\nSorry, that is incorrect")
			output += ("\n\nThe correct answer(s) are:  %s\n\n"  %",".join(s for s in self.answer_key))
			#self.StoreMissedQuestion()
			output += "\n"
			rows = self.cursor.execute(f"update QUESTIONS set LAST_ASKED_TS = current_timestamp, LAST_ANSWER = '{my_answer}',ANSWERED_CORRECTLY = False where family = '{self.family}' and qid = {self.question_id};")
			explained = (self.SplitLongLine(self.question["Explanation"],WRAP=75) + "\n")
		output += "\n"
		if self.GetValue(self.show_mistakes):
			output += explained
			self.SetMessage(output)
			self.HideSubmitBtn()
			self.ShowNextQuestionBtn()
			self.Layout()
			self.Update()
		else:
			self.NextQuestion(None)
			if len(explained) > 0:
				explained = "\n\nNotes on previous question:\n" + explained
				self.SetMessage(explained)
				self.Layout()
				self.Update()
		self.conn.commit()

	# ------------------------------------------------------------------------------
	def StoreMissedQuestion(self):
		self.missed_questions += str(self.question) + ",\n"

def main(args):

	app = wx.App(False)
	frame = Main_Window(None, "Greg Roeper", args)
	#frame.Centre(direction = wx.BOTH)
	frame.Show()
	app.MainLoop()

if __name__ == "__main__" :
	parser = argparse.ArgumentParser()

	parser =  argparse.ArgumentParser(description = 'Optional app description')
	parser.add_argument('-review_missed_questions', action='store_true', help = 'Review questions previously missed')
	parser.add_argument('-family', type = str, required=True, help = 'Certification family, i.e. "SnowPro Core"')
	parser.add_argument('-question_count', type = int, help = '# of questions to ask')
	parser.add_argument('-debug_level', type = int, help = 'Degug Level')

	args =  parser.parse_args()

	main(args)