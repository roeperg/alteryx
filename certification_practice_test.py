#!/python311/python


#abadae
#c2f1f5
#e4e6e7


#import tkinter as tk
from PIL import Image
from subprocess import Popen
from tkinter import scrolledtext, ttk
import argparse
import configparser
import cv2
import os
import pathlib
import random
import re
import signal
import sqlite3
import sys
import textwrap
import time
import win32clipboard
import wx


class Main_Window(wx.Frame):
	def __init__(self, parent, title, arguments):
		self.background_color = "#f0f0f0"
		wx.Frame.__init__(self, parent, title = title, size = (1200,850), pos=(300,100))
		self.start_time = time.time()
		self.conn = sqlite3.connect(r'C:\Greg\dev\dev_certification_practice.db')
		self.cursor = self.conn.cursor()

		self.pythonexecutable = sys.executable
		self.image_display_path = os.path.join(os.path.dirname(__file__), "trash.py")

		self.imagepath = r"c:\Greg\Alteryx\QuizImages"
		self.datapath = r"c:\Greg\Alteryx\QuizData"
		self.SetBackgroundColour(self.background_color)
		self.bullets = "ABCDEFGH"
		self.crlf = chr(10)+chr(13)
		self.randomize = True
		self.button_size = (200,20)

		self.open_window = 0
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
		self.last_row_count = 0
		self.log_level = 0
		self.answered_questions = 0
		self.question_number = 0
		self.question_header = wx.StaticText(self, name='question_header', style = wx.BORDER_DOUBLE | wx.ALIGN_CENTER| wx.ST_NO_AUTORESIZE, size=(350,30), pos=(40,20))
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
			self.checkboxes[foo] = wx.CheckBox(self, -1, label= " "*120, size=(175,75), pos=(900,checkboxy))
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

		self.clipboard_search_btn = wx.Button(self, label="Clipboard Search", name="quit", size=(self.button_size), pos=(800,725))
		self.clipboard_search_btn.Bind(wx.EVT_BUTTON, self.ClipboardSearch)


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

		self.max_questions = 100
		self.debug_level = 0
		self.review = False
		if arguments.family:
			self.family = arguments.family
		else:
			self.family = 'Alteryx Advanced Desktop'

		if arguments.question_count:
			self.max_questions = arguments.question_count
		self.number_of_questions.ChangeValue(str(self.max_questions))

		if arguments.debug_level:
			self.debug_level = arguments.debug_level

		if arguments.qid:
			self.target_qid = arguments.qid
		else:
			self.target_qid = 0

		if arguments.review_missed_questions:
			self.review = True

		self.update_user("Initialized", LOGLEVEL=1)
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
		self.max_questions = 100

		if self.randomize:
			inq = f"select qid from QUESTIONS where family = '{self.family}' order by RANDOM() limit {self.max_questions}"
			if self.review:
				inq = f"select qid from QUESTIONS where family = '{self.family}' and answered_correctly = False order by RANDOM()"
		else:
			inq = f"select qid from QUESTIONS where family = '{self.family}' limit {self.max_questions}"
			if self.review:
				inq = f"select qid from QUESTIONS where family = '{self.family}' and answered_correctly = False"

		if self.target_qid > 0:
			inq = inq.replace(" where ", f" where qid = {self.target_qid} and ")
			self.HideSubmitBtn()
			print(f"select * from questions where qid  = {self.target_qid};")
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
	def update_user(self, textStr, LOGLEVEL=1, TIMES=True, SUPPRESS_TIME=False):
			if self.log_level >= LOGLEVEL:
					currtime = time.time()
					elapsed_time = currtime - self.last_message_time
					if not SUPPRESS_TIME:
						self.last_message_time = currtime
					Msg = str(time.strftime("%d-%b-%Y %H:%M:%S", time.localtime())) + "  %-50s" % str(textStr)
					if TIMES:
						Msg += self.secondsToStr(elapsed_time) + " elapsed"
					self.user_log_text += Msg + "\n"
					print(Msg)

	##########################################################################################
	def ShowImage(self, photo):
		print(f"Displaying image {photo}")

		cmd = [self.pythonexecutable, self.image_display_path ,os.path.join(self.imagepath, photo)]
		print(cmd)
		print(cmd[0])
		print(cmd[1])
		if True:#try:
			self.open_window = Popen(cmd, shell=False, stdin=None,stdout=None, stderr=None, close_fds=True).pid
		if False:#except:
			pass
		print(self.open_window)

	##########################################################################################
	def ShowExcel(self, workflow):
		print(f"opening {workflow}")
		cmd = [r"c:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE", f"{self.datapath}\{workflow}"]
		print(cmd)
		print(cmd[0])
		print(cmd[1])
		try:
			Popen(cmd, shell=False, stdin=None,stdout=None, stderr=None, close_fds=True)
		except:
			pass


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

	##########################################################################################
	def SplitLongLine(self, intext, WRAP=82, INDENT=""):

		print(f"INDENT!!!  '{INDENT}'")
		if intext is None:
			return ""

		intext = intext.strip()
		lines = intext.split("\n")
		outarray = []
		first_line = True
		current_indent = ""
		
		for g in range(len(lines)):
			if not first_line:
				current_indent = INDENT
				first_line = False
			foo = lines[g]
			temptext = ""
			foo = foo.strip()
			if len(foo) == 0:
				outarray.append(" ")
				firstline =  False
			else:
				arrayed = foo.split(" ")
				outtext = ""
				for bar in arrayed:
					if len(temptext) + len(bar) >= WRAP:
						outarray.append(current_indent + temptext)
						temptext = INDENT
						print("setting temptext to indent")  # DELETE ME
					temptext += current_indent + bar + " "
				outarray.append(current_indent + temptext)

		self.last_row_count = len(outarray)
		join_string = "\n"
		return_text = join_string.join(s for s in outarray)
		return return_text


	##########################################################################################
	def ClipboardSearch(self,event):
		print("WE ARE SEARCHING FROM CLIPBOARD") # DELETE ME
		self.answer_key = []
		self.explanation = []
		self.ResetAnswerKey()
		self.ResetCheckboxes()

		# get clipboard data
		win32clipboard.OpenClipboard()
		target = win32clipboard.GetClipboardData()
		win32clipboard.CloseClipboard()

		self.question = {"Question":"nah", "Explanation":"None", "Answers":[]}
		## Query for next question
		rows = self.cursor.execute(f"select qid, text, explanation from questions where family = '{self.family}' and lower(text) like lower('%' || '{target}' || '%')")

		for foo in rows:
			self.local_question_id = foo[0]
			self.question["Question"] = foo[1]
			self.question["Explanation"] = foo[2]
		print("Question ID = ", self.question_id)

		## Query for answers
		aqry = f"select text, correct from ANSWERS where qid = {self.local_question_id} and correct = True;"
		rows = self.cursor.execute(aqry)
		for foo in rows:
			print(foo)
			self.question["Answers"].append({"Answer":foo[0], "Correct":foo[1]})

		temptext = (self.SplitLongLine(self.question['Question'],WRAP=110))
		print(f"Last row count {self.last_row_count}")
		self.question_text.SetLabel("\n" + 	temptext)

		temp_answers = []
		for bar in self.question['Answers']:
			temp_answers.append(bar)

		for foo in self.bullets:
			self.HideCheckbox(foo)

		positiony = 140
		for bar in range(len(self.question['Answers'])):
			temptext = ("  %s.  %s" %(self.bullets[bar], self.SplitLongLine(temp_answers[bar]["Answer"],WRAP=42,INDENT='      ')))
			#temptext = ("  %s. %s" %(self.bullets[bar], temp_answers[bar]["Answer"]))
			lines = int(len(temptext) / 60)
			newheight = 20 + lines * 17

			self.SetCheckLabel(self.bullets[bar], temptext)
			self.MoveCheckBox(self.bullets[bar], 750, positiony)
			self.SizeCheckBox(self.bullets[bar], newheight)
			positiony += newheight
			self.ShowCheckbox(self.bullets[bar])

			if temp_answers[bar]['Correct'] == "True" or temp_answers[bar]['Correct'] == 1:
				self.answer_key.append(self.bullets[bar])

		self.HideSubmitBtn()
		self.ShowNextQuestionBtn()

		self.Layout()
		self.Update()


	##########################################################################################
	def NextQuestion(self,event):
		try:
			if self.open_window > 0:
				os.kill(self.open_window, signal.SIGTERM)
				self.open_window = 0
		except:
			pass

		if len(self.question_id_array) == 0:
			self.ShowResults(None)
			return
		self.answer_key = []
		self.explanation = []
		self.ResetAnswerKey()
		self.ResetCheckboxes()

		self.question = {"Question":"nah", "Explanation":"None", "Answers":[]}
		self.question_id = self.question_id_array.pop(0)
		print(f"The current QID is {self.question_id}")
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

		temptext = (self.SplitLongLine(self.question['Question'],WRAP=110))
		print(f"Last row count {self.last_row_count}")
		self.question_text.SetLabel("\n" + 	temptext)

		temp_answers = []
		for bar in self.question['Answers']:
			temp_answers.append(bar)
		#if self.randomize:
		#	random.shuffle(temp_answers)

		for foo in self.bullets:
			self.HideCheckbox(foo)

		positiony = 140
		for bar in range(len(self.question['Answers'])):
			temptext = ("  %s.  %s" %(self.bullets[bar], self.SplitLongLine(temp_answers[bar]["Answer"],WRAP=42, INDENT='  !  ')))
			#temptext = ("  %s. %s" %(self.bullets[bar], temp_answers[bar]["Answer"]))
			lines = len(temptext.split("\n"))
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

		if 'Data' in self.question.keys():
			print("Data file ", self.question['Data'])
			if self.question['Data'] != "":
				#excel, yxmd
				fullpath = self.question['Data'].strip()
				if fullpath.lower().find(".xls") > -1:
					print(f"YXMD path {fullpath}")
					self.ShowExcel(fullpath)
				if fullpath.lower().find(".yxm") > -1:
					print(f"YXMD path {fullpath}")
					self.ShowWorkflow(fullpath)

		self.question_number += 1

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
		if self.open_window > 0:
			try:
				os.kill(self.open_window, signal.SIGTERM)
				self.open_window = 0
			except:
				pass
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
	parser.add_argument('-family', type = str, required=False, help = 'Certification family, i.e. "SnowPro Core"')
	parser.add_argument('-qid', type = int, help = 'specific qid to target')
	parser.add_argument('-question_count', type = int, help = '# of questions to ask')
	parser.add_argument('-debug_level', type = int, help = 'Degug Level')

	args =  parser.parse_args()

	main(args)
