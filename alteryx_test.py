#!/python311/python

from exam_questions import *
import os
import random
import sys
import textwrap
import time
import wx

if True:#try:
	from missed_exam_questions import *
	print("Using missed questions")
	print("Total questions = %d" %len(exam_question_dict_array))
if False:#except:
	print("Not using missed questions")
	pass
	


class Main_Window(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title = title, size = (1200,1000), pos=(20,20))
		self.start_time = time.time()

		self.SetBackgroundColour("#c2f1f5")
		self.bullets = "ABCDEF"

		self.missed_questions = ""
		self.question = {}
		self.answer_key = []
		self.explanation = []
		self.randomize = True
		
		self.correct_count = 0
		self.button_size = (200,20)

		font1 = wx.Font(10, family = wx.DECORATIVE, style = 0, weight = 90,underline = False, faceName ="", encoding = wx.FONTENCODING_DEFAULT)
		font2 = wx.Font(12, family = wx.DECORATIVE, style = 1, weight = 90,underline = False, faceName ="", encoding = wx.FONTENCODING_DEFAULT)
		font3 = wx.Font(14, 72, 0, 90, underline = False,faceName ="")

		if True:
			count = 50
			while count < 1100:
				tic = wx.StaticText(self, pos=(count,50))  
				tic.SetLabel(f"{count}")
				tic.SetFont(font1)
				tic.SetBackgroundColour("#c2f1f5")
				count += 50
			


		self.question_header = wx.StaticText(self, name='question_header', style = wx.BORDER_DOUBLE | wx.ALIGN_CENTER| wx.ST_NO_AUTORESIZE, size=(650,30), pos=(40,20))  
		self.question_header.SetLabel("Question")
		self.question_header.SetFont(font3)
		self.question_header.SetBackgroundColour("#c2f1f5")


		self.answer_header = wx.StaticText(self, name='answer_header', style = wx.BORDER_DOUBLE | wx.ALIGN_CENTER| wx.ST_NO_AUTORESIZE, size=(450,30), pos=(700,20))  
		self.answer_header.SetLabel("Possible Answers")
		self.answer_header.SetFont(font3)
		self.answer_header.SetBackgroundColour("#c2f1f5")


		self.question_text = wx.StaticText(self, name='question_field', style = wx.BORDER_DOUBLE | wx.TE_MULTILINE, size=(650,430), pos=(40,80)) #Text area with multiline    
		self.question_text.SetFont(font1)
		self.question_text.SetBackgroundColour("#c2f1f5")
		self.question_text.SetLabel("\nGreg\n\t\tRoeper\n\t\t\trocks")

		self.user_message = wx.TextCtrl(self, name='message_field', style = wx.TE_MULTILINE | wx.BORDER_DOUBLE | wx.TE_READONLY, size=(650,350), pos=(40,520)) #Text area with multiline
		self.user_message.SetBackgroundColour("#c2f1f5")

		self.checkboxes = {}
		
		self.checkboxes['A'] = wx.CheckBox(self, -1, label= "*"*120, pos=(900,105))
		self.checkboxes['B'] = wx.CheckBox(self, -1, label= " "*120, pos=(900,135))
		self.checkboxes['C'] = wx.CheckBox(self, -1, label= " "*120, pos=(900,220))
		self.checkboxes['D'] = wx.CheckBox(self, -1, label= " "*120, pos=(900,240))
		self.checkboxes['E'] = wx.CheckBox(self, -1, label= " "*120, pos=(900,295))
		self.checkboxes['F'] = wx.CheckBox(self, -1, label= " "*120, pos=(900,360))
		#self.checkboxes['A'].Move(300,300)
		
		row_offset = 800
		self.submit_btn = wx.Button(self, label="Submit Answer", name="two", size=(self.button_size), pos=(850,row_offset))
		self.submit_btn.Bind(wx.EVT_BUTTON, self.checkAnswers)
		row_offset += 50
		self.next_question_btn = wx.Button(self, label="Next Question", name="next",  size=(self.button_size), pos=(850,row_offset))
		self.next_question_btn.Bind(wx.EVT_BUTTON, self.next_question)
		row_offset += 50

		self.exit_btn = wx.Button(self, label="Exit", name="quit", size=(self.button_size), pos=(850,row_offset))
		self.exit_btn.Bind(wx.EVT_BUTTON, self.OnExit)
		self.exit_btn.Hide()
		row_offset += 50
		self.end_test_btn = wx.Button(self, label="End Test", name="quit", size=(self.button_size), pos=(500,850))
		self.end_test_btn.Bind(wx.EVT_BUTTON, self.show_results)
		row_offset += 50

		self.save_missed_questions_btn = wx.Button(self, label="Save missed questions for later", name="save", size=(self.button_size), pos=(850,700))
		self.save_missed_questions_btn.Bind(wx.EVT_BUTTON, self.SaveMissedQuestions)

		self.save_missed_questions_btn.Hide()
			
		self.clear_missed_questions_btn = wx.Button(self, label="Clear missed questions", name="quit", size=(self.button_size), pos=(850,745))
		self.clear_missed_questions_btn.Bind(wx.EVT_BUTTON, self.ClearMissedQuestions)

		self.clear_missed_questions_btn.Hide()

		#self.show_notes = wx.CheckBox(self, -1, label= "Show Explanation if Available", pos=(100,880))
		self.show_mistakes = wx.CheckBox(self, -1, label= "Show Wrong Answers During Test", pos=(100,900))
		self.number_of_questions = wx.TextCtrl(self, name='message_field', size=(40,25), style = wx.BORDER_DOUBLE , pos=(100,930)) 
		self.number_of_questions.ChangeValue("75")
		
		self.lbl1 = wx.StaticText(self, name='lbl1', style = wx.BORDER_DOUBLE | wx.ALIGN_CENTER| wx.ST_NO_AUTORESIZE, size=(150,25), pos=(140,930))  
		self.lbl1.SetLabel("# of questions")
		
		self.question_number = 0
		self.correct_answers = 0
		self.answer_dict = {}
		self.explanation_dict = {}
		self.question_number_list = []
		self.question_dict = {}
		self.answer_dict[0] = []
		self.explanation_dict[0] = []
		self.question_dict[0] = []
		
		self.questions = exam_question_dict_array
		if self.randomize:
			random.shuffle(self.questions)
		self.answered_questions = 0
		self.total_questions = len(self.questions)
		
		self.next_question(None)



# FUNCTIONS
# ------------------------------------------------------------------------------

	##########################################################################################
	def split_long_line(self, intext, WRAP=58, INDENT="   "):
	
		if intext is None:
			return ""
		arrayed = intext.split(" ")
		outarray = []
		temptext = INDENT
		
		for foo in arrayed:
			if len(temptext) + len(foo) > WRAP:
				outarray.append(temptext)
				temptext = ""
			temptext += foo + " "
	
		outarray.append(temptext)
		
		join_string = "\n" + INDENT
		
		return join_string.join(s for s in outarray)

	##########################################################################################
	def next_question(self,event):
		print(f"Question number {self.question_number} out of {len(self.questions)}")
		max_questions = 0
		try:
			max_questions = int(self.number_of_questions.GetValue())
			print(max_questions, len(self.questions), self.question_number )
		except:
			wx.MessageDialog(self, "The number of questions must be an integer!", "Warning!", wx.OK | wx.ICON_WARNING).ShowModal()

		if (len(self.questions) <= self.question_number) or max_questions <= (self.question_number):
			print(self.question_number, len(self.questions))
			self.show_results(None)
			return
		self.answer_key = []
		self.explanation = []
		self.ResetAnswerKey()
		self.ResetCheckboxes()
		self.question = self.questions[self.question_number]
		#print("Correct questions = %d" %self.correct_count)
		self.question_header.SetLabel("Question %d out of %d" %(self.question_number+1,min(self.total_questions,max_questions)))

		temptext = (self.split_long_line(self.questions[self.question_number]['Question'],WRAP=82))
		self.question_text.SetLabel("\n" + 	temptext)
		
		temp_answers = []
		for bar in self.questions[self.question_number]['Answers']:
			temp_answers.append(bar)
		if self.randomize:
			random.shuffle(temp_answers)

		for foo in self.bullets:
			self.HideCheckbox(foo)

		positiony = 105
		for bar in range(len(self.questions[self.question_number]['Answers'])):
			print(">>>>", temp_answers[bar]['Answer'])  # DELETE ME
			temptext = ("%s.  %s" %(self.bullets[bar], self.split_long_line(temp_answers[bar]['Answer'],WRAP=54)))
			#print(">>>", temptext)
			lines = len(temptext.split("\n"))
			newheight = 20 + lines * 15
			#print("new height = ", newheight)
			
			self.SetCheckLabel(self.bullets[bar], temptext)
			self.MoveCheckBox(self.bullets[bar], 750, positiony)		
			#print(self.bullets[bar], newheight)		
			self.SizeCheckBox(self.bullets[bar], newheight)		
			positiony += newheight	
			self.ShowCheckbox(self.bullets[bar])

			if temp_answers[bar]['Correct']:
				self.answer_key.append(self.bullets[bar])
		
		self.submit_btn.Move(800, positiony)
		self.next_question_btn.Move(800, positiony)

		for giggles in self.questions[self.question_number]['Explanation']:
			self.explanation.append(giggles)

		self.HideExplanation()
		self.ShowSubmitBtn()
		self.HideNextQuestionBtn()

		self.question_number += 1

		self.Layout()
		self.Update()

	##########################################################################################
	def MoveCheckBox(self,keyvalue, x, y):
		self.checkboxes[keyvalue].Move((x,y))

	##########################################################################################
	def SizeCheckBox(self,keyvalue, height):
		self.checkboxes[keyvalue].SetSize(450,height)
		

	##########################################################################################
	def show_results(self,event):
		temptext = "\n\n\n"
		self.correct_answers = self.correct_count
		if self.question_number:
			temptext += ("\t%d correct answer(s) out of %d	\n\n\t%.0f %%\n\n\n" %(self.correct_answers, self.question_number, 100*self.correct_answers/self.question_number))
		
		elapsed = time.strftime("%H:%M:%S", time.gmtime(time.time() - self.start_time))
		temptext += (f"	Time: {elapsed}")

		self.question_text.SetLabel(temptext)

		self.save_missed_questions_btn.Show()
		self.clear_missed_questions_btn.Show()
		self.exit_btn.Show()
		self.next_question_btn.Hide()
		self.end_test_btn.Hide()
		self.HideExplanation()
		#self.Hide()
		self.Layout()
		self.Update()

	# ------------------------------------------------------------------------------
	def SaveMissedQuestions(self, event):
		with open("missed_exam_questions.py","w") as f:
			f.writelines("#!/opt/homebrew/bin/python3\n\nexam_question_dict_array =  [\n")
			f.writelines(self.missed_questions)
			f.writelines("\n]\n")

	# ------------------------------------------------------------------------------
	def ClearMissedQuestions(self, event):
		with open("missed_exam_questions.py","w") as f:
			pass

	# ------------------------------------------------------------------------------
	def OnExit(self, event):
		self.Close(True) #Close the frame

	#----------------------------------------------------------------------
	def SetCheckLabel(self, keyvalue, value):
		self.checkboxes[keyvalue].SetLabel(value.replace("(Correct)",""))
		#print("set label", keyvalue, value)
		
	#----------------------------------------------------------------------
	def HideNextQuestionBtn(self):
		self.next_question_btn.Hide()
		#print("Hid submit button")

	#----------------------------------------------------------------------
	def ShowNextQuestionBtn(self):
		self.next_question_btn.Show()
		#print("submit button")

	#----------------------------------------------------------------------
	def HideSubmitBtn(self):
		self.submit_btn.Hide()
		#print("Hid submit button")

	#----------------------------------------------------------------------
	def ShowSubmitBtn(self):
		self.submit_btn.Show()
		#print("submit button")

	#----------------------------------------------------------------------
	def HideCheckbox(self, keyvalue):
		self.checkboxes[keyvalue].Hide()
		#print("Hid box", keyvalue)

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
	def HideExplanation(self):
		""""""
		self.SetMessage("")

		self.Layout()
		self.Update()
		
	#----------------------------------------------------------------------
	def ResetAnswerKey(self):
		self.answer_key = []
		
	#----------------------------------------------------------------------
	def GetValue(self, inbox):
		return inbox.GetValue()

	#----------------------------------------------------------------------
	def checkAnswers(self, event):
		my_answer = ""
		for foo in self.checkboxes.keys():
			if self.GetValue(self.checkboxes[foo]):
				my_answer += foo

		
		output = "\n\n"
		explained = ""
		correct_answer = "".join(s for s in self.answer_key)
		#("*%s* ??? *%s*" %(correct_answer, my_answer))

		if correct_answer == my_answer:
			output += ("\nYou are correct!  The answer(s) are	 %s\n\n"  %",".join(s for s in self.answer_key))			
			self.correct_count += 1
			#print(f"Correct count = {self.correct_count}")
		else:
			output += ("\n\nSorry, that is incorrect")
			output += ("\n\nThe correct answer(s) are:  %s\n\n"  %",".join(s for s in self.answer_key))
			self.StoreMissedQuestion()
			output += "\n"
			for bar in self.explanation:
				explained += (self.split_long_line(bar,WRAP=75) + "\n")
		output += "\n"
		if self.GetValue(self.show_mistakes):
			#print("showing mistakes")
			output += explained
			self.SetMessage(output)
			self.HideSubmitBtn()
			self.ShowNextQuestionBtn()
			self.Layout()
			self.Update()
		else:
			self.next_question(None)
			#if self.GetValue(self.show_notes):
			#print("explained length = ", len(explained))
			if len(explained) > 0:
				explained = "\n\nNotes on previous question:\n" + explained
				self.SetMessage(explained)
				#print(explained)
				self.Layout()
				self.Update()


	# ------------------------------------------------------------------------------
	def StoreMissedQuestion(self):
		self.missed_questions += str(self.question) + ",\n"




def main():

	app = wx.App(False)
	frame = Main_Window(None, "App GUI")
	frame.Centre(direction = wx.BOTH)
	frame.Show()
	app.MainLoop()

if __name__ == "__main__" :
	main()