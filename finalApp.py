from Tkinter import *
from eventBasedAnimationClass import EventBasedAnimationClass
import os,copy,csv,random,re,urllib,ast
from datetime import date


class TwentyQuestionsGame(EventBasedAnimationClass):

	def __init__(self):
		super(TwentyQuestionsGame,self).__init__(800,600)
		self.width =800
		self.height =600
		self.file = "background1.gif"
		self.timerDelay =1



	def initAnimation(self):
		self.buttonWidth = self.width/3
		self.buttonHeight = self.height/8
		self.buttonMargin = 3.2
		self.startButtonX =(self.width/2)-self.buttonWidth/2
		self.startButtonY =self.height/2
		self.buttonUpMain = self.rgbString(240,240,240)
		self.buttonUpLine = "gray70"
		self.buttonDownMain = self.rgbString(190,195,199)
		self.buttonDownLine = "gray60"
		self.canvas.bind("<Motion>", self.onMouseMotion)
		self.YesHovered = False
		self.NoHovered = False
		self.isButtonPressed = False
		self.startScreen = True
		self.decisionTree = self.makeDecisionTree()
		self.fullDict = self.getFullDict()
		self.eliminatedDict = copy.deepcopy(self.fullDict)
		self.decisionYN = None
		self.gameOver=False
		self.keyToAsk = None
		self.ishelpButtonPressed  =False
		self.questionToAsk = None
		self.helpHovered = False
		self.YesFinalHovered = False
		self.NoFinalHovered = False
		self.isFinalNoPressed = False
		self.isFinalYesPressed= False
		self.disableRestart = False
		self.DoneHovered = False
		self.onNoScreen =False
		self.DonePressed = False
		self.enteredText = ""
		self.questionsDict()


	def makeDecisionTree(self):
		ageDecision4  =["Age","return","return"]
		professionDecision2 = ["Profession",ageDecision4,ageDecision4]
		nationalityDecision2 = ["Nationality",professionDecision2,professionDecision2]
		ageDecision3 = ["Age",nationalityDecision2,nationalityDecision2]
		professionDecision = ["Profession",ageDecision3,ageDecision3]
		naionalityDecision = ["Nationality",professionDecision,professionDecision]
		ageDecision2  = ["Age",naionalityDecision,naionalityDecision]
		ageDecision = ["Age",ageDecision2,ageDecision2]
		childrenDecision = ["Children",ageDecision,ageDecision]
		marriedDecision = ["Married",childrenDecision,ageDecision]
		genderDecision = ["Gender",marriedDecision,marriedDecision]
		firstDecision = ["Alive",genderDecision,genderDecision]
		decisionTree = firstDecision
		return decisionTree


	def getFullDict(self):
		fullDict  = {}
		if(os.path.exists("filteredDictionary.csv")):
			for key, val in csv.reader(open("filteredDictionary.csv")):
				fullDict[key] = val
		return fullDict



	def eliminator(self,eliminatedDict,decisionTree,attribute):
		decisionList = copy.deepcopy(decisionTree)
		if(type(decisionList)==str or len(eliminatedDict)<5):
			self.gameOver = True
			return eliminatedDict,decisionList
		else:
			choice = self.decisionYN
			eliminatedDict = self.removeFromDict(choice,eliminatedDict,decisionList[0],attribute)
			if(choice=="y"):
				decisionList = decisionList[1]
			elif(choice=="n"):
				decisionList = decisionList[2]
			if(len(eliminatedDict)<5):
				self.gameOver = True
			return eliminatedDict,decisionList
			

	def questionAsker(self,decisionList,eliminatedDict):
		if(type(decisionList)==str or len(eliminatedDict)<5):
			self.gameOver = True
			return decisionList[0],None
		else:
			if(decisionList[0]=="Nationality"):
				nationality = self.mostCommonNationality(eliminatedDict)
				return decisionList[0],nationality
			elif(decisionList[0]=="Profession"):
				profession = self.mostCommonProfession(eliminatedDict)
				return decisionList[0],profession
			elif(decisionList[0]=="Age"):
				age = self.halfAgeCalculator(eliminatedDict)
				return decisionList[0],age
			else:
				return decisionList[0],None






	def removeFromDict(self,choice, eliminatedDict,key,attribute):
		keysToBeRemoved = []
		if(choice=="y"):
			if(key=="Profession" or key=="Nationality"):
				for nameKey in eliminatedDict:
					subDict = ast.literal_eval(eliminatedDict[nameKey])
					if(subDict[key]!=attribute and subDict[key]!="Unknown"):
						keysToBeRemoved.append(nameKey)
			elif(key=="Age"):
				for nameKey in eliminatedDict:
					subDict = ast.literal_eval(eliminatedDict[nameKey])
					if(int(subDict[key])<attribute):
						keysToBeRemoved.append(nameKey)
			else:
				for nameKey in eliminatedDict:
					subDict = ast.literal_eval(eliminatedDict[nameKey])
					if(subDict[key]==False or subDict[key]=="Female"):
						keysToBeRemoved.append(nameKey)

		if(choice=="n"):
			if(key=="Profession" or key=="Nationality"):
				for nameKey in eliminatedDict:
					subDict = ast.literal_eval(eliminatedDict[nameKey])
					if(subDict[key]==attribute and subDict[key]!="Unknown"):
						keysToBeRemoved.append(nameKey)
			elif(key=="Age"):
				for nameKey in eliminatedDict:
					subDict = ast.literal_eval(eliminatedDict[nameKey])
					if(int(subDict[key])>=attribute):
						keysToBeRemoved.append(nameKey)
			else:
				for nameKey in eliminatedDict:
					subDict = ast.literal_eval(eliminatedDict[nameKey])
					if(subDict[key]==True or subDict[key]=="Male"):
						keysToBeRemoved.append(nameKey)

		for remove in keysToBeRemoved:
			del eliminatedDict[remove]
		return eliminatedDict


			
	def halfAgeCalculator(self,eliminatedDict):
		ageTotal = 0
		for nameKey in eliminatedDict:
			subDict = ast.literal_eval(eliminatedDict[nameKey])
			ageTotal += int(subDict["Age"])
		ageAverage = ageTotal/len(eliminatedDict)
		return ageAverage

	def mostCommonProfession(self,eliminatedDict):
		professionList = ["president","prime minister",
		"actor","rapper","vice-president","politician",
		"chef","writer","singer","official","teacher","poet",
		"painter","scluptor","mathematician","scientist","inventor",
		"engineer","leader","judge","dancer","model","actress",
		"basketball player","soccer player","football player",
		"entrepreneur","author","pope"]
		professionFrequency = [0]*len(professionList)
		for nameKey in eliminatedDict:
			subDict = ast.literal_eval(eliminatedDict[nameKey])
			if(subDict["Profession"]!="Unknown" and subDict["Profession"]!=False):
				indexToAdd = professionList.index(subDict["Profession"])
				professionFrequency[indexToAdd]+=1
		if(len(professionFrequency)>1):
			maxFreq = max(professionFrequency)
			indexToGet = professionFrequency.index(maxFreq)
			mostCommonProfessionToAsk = professionList[indexToGet]
		else:
			mostCommonProfessionToAsk = "scientist"
		return mostCommonProfessionToAsk


	def mostCommonNationality(self,eliminatedDict):
		nationalityList = []
		nationalityFreqList  = []
		for nameKey in eliminatedDict:
			subDict = ast.literal_eval(eliminatedDict[nameKey])
			if(subDict["Nationality"] in nationalityList):
				indexToAppend = nationalityList.index(subDict["Nationality"])
				nationalityFreqList[indexToAppend]+=1
			else:
				if(subDict["Nationality"]!="Unknown"):
					nationalityList.append(subDict["Nationality"])
					nationalityFreqList.append(1)
		if(len(nationalityFreqList)>1):
			maxFreq = max(nationalityFreqList)
			indexToGet = nationalityFreqList.index(maxFreq)
			mostCommonNationalityToAsk = nationalityList[indexToGet]
		else:
			mostCommonNationalityToAsk = "Chinese"
		return mostCommonNationalityToAsk



	def onMouseMotion(self, event):
		self.motionX = event.x
		self.motionY = event.y
		if(self.startScreen==False):
			self.checkCursorOnButton()
		if(self.gameOver==True):
			self.checkCursorOnFinalButton()
			if(self.onNoScreen==True):
				self.checkCursorOnDoneButton()


	def checkCursorOnButton(self):
		self.YesHovered = False
		self.NoHovered = False
		self.helpHovered = False
		if(self.YesStartX<self.motionX<self.YesEndX 
			and self.YesStartY<self.motionY<self.YesEndY):
			self.YesHovered  =True
		elif(self.NoStartX<self.motionX<self.NoEndX 
			and self.NoStartY<self.motionY<self.NoEndY):
			self.NoHovered = True
		elif(self.helpButtonLeftX<self.motionX<self.helpButtonRightX
			and self.helpButtonUpY<self.motionY<self.helpButtonDownY):
			self.helpHovered = True

	def checkCursorOnFinalButton(self):
		self.YesFinalHovered = False
		self.NoFinalHovered = False
		if(self.YesLeftXFinal<self.motionX<self.YesRightXFinal
			and self.YesTopYFinal<self.motionY<self.YesBottomYFinal):
			self.YesFinalHovered = True
		elif(self.NoLeftXFinal<self.motionX<self.NoRightXFinal
			and self.NoTopYFinal<self.motionY<self.NoBottomYFinal):
			self.NoFinalHovered = True

	def checkCursorOnDoneButton(self):
		self.DoneHovered = False
		if(self.DoneLeftX<self.motionX<self.DoneRightX
			and self.DoneUpY<self.motionY<self.DoneDownY):
			self.DoneHovered = True

	def addToDict(self):
		basicInfo = self.wikipediaInfoScraper(self.enteredText)
		firstPara = self.getFirstPara(self.enteredText)
		dictPerson = self.makePersonDict(basicInfo,firstPara)
		dictPerson["Name"] = self.enteredText
		peopleDict  = self.getFromFinalDict()
		peopleDict = copy.deepcopy(peopleDict)
		peopleDict[self.enteredText] = dictPerson
		self.saveToFinalDict(peopleDict)



	def getFromFinalDict(self):
		peopleDict  = {}
		if(os.path.exists("filteredDictionary.csv")):
			for key, val in csv.reader(open("filteredDictionary.csv")):
				peopleDict[key] = val
		return peopleDict

	def saveToFinalDict(self,peopleDict):
		w = csv.writer(open("filteredDictionary.csv", "w"))
		for key, val in peopleDict.items():
		    w.writerow([key, val])

	def singleConverter(self,person):
		orgStr  ="http://en.wikipedia.org/wiki/"
		person = person.replace(" ","_")
		personLinked = (orgStr+person)
		return personLinked



	def buttonPressed(self):
		self.isButtonPressed = False
		self.yesButtonPressed = False
		self.NoButtonPressed = False
		self.decisionYN = None
		if(self.YesStartX<self.pressX<self.YesEndX 
			and self.YesStartY<self.pressY<self.YesEndY):
			self.isButtonPressed = True
			self.yesButtonPressed = True
			self.decisionYN = "y"
			(self.eliminatedDict,self.decisionTree) =  self.eliminator(self.eliminatedDict,self.decisionTree,self.attribute)
			(self.keyToAsk,self.attribute) = self.questionAsker(self.decisionTree,self.eliminatedDict)
			self.questionSelector()
		elif(self.NoStartX<self.pressX<self.NoEndX 
			and self.NoStartY<self.pressY<self.NoEndY):
			self.isButtonPressed = True
			self.NoButtonPressed = True
			self.decisionYN = "n"
			(self.eliminatedDict,self.decisionTree) =  self.eliminator(self.eliminatedDict,self.decisionTree,self.attribute)
			(self.keyToAsk,self.attribute) = self.questionAsker(self.decisionTree,self.eliminatedDict)
			self.questionSelector()

	def helpButtonPressed(self):
		if(self.helpButtonLeftX<self.pressX<self.helpButtonRightX
			and self.helpButtonUpY<self.pressY<self.helpButtonDownY):
			self.ishelpButtonPressed = not(self.ishelpButtonPressed)
	
	def finalButtonsPressed(self):
		if(self.YesLeftXFinal<self.pressX<self.YesRightXFinal
			and self.YesTopYFinal<self.pressY<self.YesBottomYFinal):
			self.isFinalYesPressed = True
		elif(self.NoLeftXFinal<self.pressX<self.NoRightXFinal
			and self.NoTopYFinal<self.pressY<self.NoBottomYFinal):
			self.isFinalNoPressed = True
			self.onNoScreen = True

	def doneButtonPressed(self):
		if(self.DoneLeftX<self.pressX<self.DoneRightX
			and self.DoneUpY<self.pressY<self.DoneDownY):
			self.DonePressed = True
			self.addToDict()


	def onMousePressed(self,event):
		try:
			self.pressX = event.x
			self.pressY = event.y
			if(self.gameOver!=True):
				(self.keyToAsk,self.attribute) = self.questionAsker(self.decisionTree,self.eliminatedDict)
				self.questionSelector()
			if(self.startScreen==True):
				self.startScreen = False
			elif(self.gameOver==True):
				self.finalButtonsPressed()
				if(self.onNoScreen==True):
					self.doneButtonPressed()
			else:
				self.buttonPressed()
				self.helpButtonPressed()
				if(self.isButtonPressed==True):
					imageNumber  = random.randint(1,7)
					self.file = "background"+str(imageNumber)+".gif"
		except:
			pass




	def onKeyPressed(self,event):
		if(self.DonePressed==True):
			if(event.keysym=='r'):
				try:
					self.__init__()
					self.initAnimation()
				except:
					pass
		elif(self.disableRestart==False):
			if(event.keysym=='r'):
				try:
					self.__init__()
					self.initAnimation()
				except:
					pass
		else:
			if(event.keysym=="BackSpace"):
				if(self.enteredText!=""):
					self.enteredText = self.enteredText[:len(self.enteredText)-1]
			elif(event.keysym=="??"):
				pass
			elif(event.keysym=="space"):
				self.enteredText+=" "
			else:
				self.enteredText+=event.keysym

	def rgbString(self,red, green, blue):
	    return "#%02x%02x%02x" % (red, green, blue)

	def redrawAll(self):
		if(self.startScreen==True):
			self.drawStartScreen()
		elif(self.gameOver==True):
			self.drawGameOverScreen()
			self.drawFinalButtons()
			if(self.isFinalNoPressed==True):
				self.disableRestart = True
				self.drawInputScreen()
				self.drawDoneButton()
				if(self.DonePressed==True):
					self.drawDoneScreen()
			elif(self.isFinalYesPressed==True):
				self.drawFinalScreen()
		elif(self.ishelpButtonPressed==True):
			self.drawHelpScreen()
			self.drawHelpButton()	
		else:
			self.drawBackground()
			self.drawButtons()
			self.drawQuestionBox()
			self.drawHelpButton()
			self.drawQuestion()
			self.drawButtonText()
			

	def drawFinalButtons(self):
		self.drawFinalYesButton()
		self.drawFinalNoButton()

	def drawDoneScreen(self):
		self.canvas.create_rectangle(0,0,self.width,self.height,fill ="turquoise4",
			outline ="turquoise4")
		doneScreenBoxSize = 200
		self.canvas.create_rectangle(5,self.height/2-doneScreenBoxSize,self.width-2,
			self.height/2+doneScreenBoxSize,
			fill = "white",outline = "gray70",width = 5)
		finalText ="""   Character Added

  Press 'r' to restart
		"""
		self.canvas.create_text(self.width/2,self.height/2,text = finalText,
			font = "Helvetica 30 bold",fill = "gray27")


	def drawFinalScreen(self):
		self.canvas.create_rectangle(0,0,self.width,self.height,fill ="turquoise4",
			outline ="turquoise4")
		lastScreenBoxSize = 200
		self.canvas.create_rectangle(5,self.height/2-lastScreenBoxSize,self.width-2,
			self.height/2+lastScreenBoxSize,
			fill = "white",outline = "gray70",width = 5)
		finalText ="""      GAME OVER

  Press 'r' to restart
		"""
		self.canvas.create_text(self.width/2,self.height/2,text = finalText,
			font = "Helvetica 30 bold",fill = "gray27")

	def drawInputScreen(self):
		self.canvas.create_rectangle(0,0,self.width,self.height,fill ="turquoise4",
			outline ="turquoise4")
		lastScreenBoxSize = 170
		self.canvas.create_rectangle(5,self.height/2-lastScreenBoxSize,self.width-2,
			self.height/2+lastScreenBoxSize,
			fill = "white",outline = "gray70",width = 5)
		self.canvas.create_rectangle(self.width/5,250,self.width-self.width/5,350)
		self.canvas.create_text(self.width/2,self.height/2-lastScreenBoxSize+60,
			text = "Enter the character you were thinking about:",
			font ="Helvetica 25 bold",
			fill = "gray27" )
		self.canvas.create_text(self.width/2,self.height/2,text = self.enteredText,
			font = "Helvetica 25 bold",fill = "gray27")


	def drawDoneButton(self):
		self.DoneLeftX = self.width/2-self.buttonWidth/2.3
		self.DoneRightX = self.width/2+self.buttonWidth/2.3
		self.DoneUpY =self.height-self.height/10-34
		self.DoneDownY = self.height-self.height/10+34
		if(self.DoneHovered==False):
			self.canvas.create_rectangle(self.DoneLeftX,self.DoneUpY,
				self.DoneRightX,self.DoneDownY,fill = self.buttonUpMain,
				outline = self.buttonUpMain)
			self.canvas.create_rectangle(self.DoneLeftX,self.DoneDownY-self.buttonMargin,
				self.DoneRightX,self.DoneDownY,fill = self.buttonUpLine,
				outline = self.buttonUpLine)
			self.canvas.create_text(self.width/2,self.height-self.height/10,
				text = "Done",font = "Helvetica 22 bold",fill = "gray27")
		else:

			self.canvas.create_rectangle(self.DoneLeftX,self.DoneUpY,
				self.DoneRightX,self.DoneDownY,fill = self.buttonDownMain,
				outline = self.buttonDownMain)
			self.canvas.create_rectangle(self.DoneLeftX,self.DoneUpY,
				self.DoneRightX,self.DoneUpY+self.buttonMargin,fill = self.buttonDownLine,
				outline = self.buttonDownLine)
			self.canvas.create_text(self.width/2,self.height-self.height/10,
				text = "Done",font = "Helvetica 22 bold",fill = "gray27")



	def drawFinalYesButton(self):
		self.YesLeftXFinal =self.width/6-self.buttonWidth/2.5
		self.YesTopYFinal = self.height-self.height/8-self.buttonHeight/2
		self.YesRightXFinal = self.width/6+self.buttonWidth/2.5
		self.YesBottomYFinal = self.height-self.height/8+self.buttonHeight/2
		self.YesTextCenterX = self.width/6
		self.YesTextCenterY = self.height-self.height/8
		if(self.YesFinalHovered==False):
			self.canvas.create_rectangle(self.YesLeftXFinal,self.YesTopYFinal,
				self.YesRightXFinal,
				self.YesBottomYFinal,fill = self.buttonUpMain,outline = self.buttonUpMain)
			self.canvas.create_rectangle(self.YesLeftXFinal,self.YesBottomYFinal-self.buttonMargin,
				self.YesRightXFinal,self.YesBottomYFinal,fill =self.buttonUpLine,
				outline = self.buttonUpLine)
			self.canvas.create_text(self.YesTextCenterX,self.YesTextCenterY,
			text= 'Yes',font = "Helvetica 22 bold",fill = "gray27")
		else:
			self.canvas.create_rectangle(self.YesLeftXFinal,self.YesTopYFinal,
				self.YesRightXFinal,
				self.YesBottomYFinal,fill = self.buttonDownMain,outline = self.buttonDownMain)
			self.canvas.create_rectangle(self.YesLeftXFinal,self.YesTopYFinal,
				self.YesRightXFinal,self.YesTopYFinal+self.buttonMargin,fill =self.buttonDownLine,
				outline = self.buttonDownLine)
			self.canvas.create_text(self.YesTextCenterX,self.YesTextCenterY,
			text=  'Yes',font = "Helvetica 22 bold",fill = "gray27")


	def drawFinalNoButton(self):
		self.NoLeftXFinal =self.width-self.width/6-self.buttonWidth/2.5
		self.NoTopYFinal = self.height-self.height/8-self.buttonHeight/2
		self.NoRightXFinal = self.width-self.width/6+self.buttonWidth/2.5
		self.NoBottomYFinal = self.height-self.height/8+self.buttonHeight/2
		self.NoTextCenterX = self.width-self.width/6
		self.NoTextCenterY =self.height-self.height/8

		if(self.NoFinalHovered==False):
			self.canvas.create_rectangle(self.NoLeftXFinal,self.NoTopYFinal,
				self.NoRightXFinal,
				self.NoBottomYFinal,
				fill = self.buttonUpMain,outline = self.buttonUpMain)

			self.canvas.create_rectangle(self.NoLeftXFinal,self.NoBottomYFinal-self.buttonMargin,
				self.NoRightXFinal,self.NoBottomYFinal,
				fill =self.buttonUpLine,outline = self.buttonUpLine)
			self.canvas.create_text(self.NoTextCenterX,self.NoTextCenterY,
			text=  'No',font = "Helvetica 25 bold",fill = "gray27")
		else:
			self.canvas.create_rectangle(self.NoLeftXFinal,self.NoTopYFinal,
				self.NoRightXFinal,
				self.NoBottomYFinal,fill = self.buttonDownMain,
				outline = self.buttonDownMain)

			self.canvas.create_rectangle(self.NoLeftXFinal,self.NoTopYFinal,
				self.NoRightXFinal,self.NoTopYFinal+self.buttonMargin,
				fill =self.buttonDownLine,
				outline = self.buttonDownLine)
			self.canvas.create_text(self.NoTextCenterX,self.NoTextCenterY,
			text=  'No',font = "Helvetica 25 bold",fill = "gray27")




	def drawHelpScreen(self):
		self.canvas.create_rectangle(0,0,self.width,self.height,fill ="turquoise4",outline ="turquoise4")
		helpBoxSize = 200
		self.canvas.create_rectangle(5,self.height/2-helpBoxSize ,self.width-2,self.height/2+helpBoxSize,
			fill = "white",outline = "gray70",width = 5)
		helpText = """INSTRUCTIONS

     1. Think of a famous personality.
     2. Answer the questions.
     3. Be astonished.
     4. If your character is not in the list add it!
     5. Press 'r' to restart .
     6. Click '?' to enter/exit help screen.
				"""
		self.canvas.create_text(self.width/2,self.height/2,fill ="gray27",text = helpText,
			font ="Helvetica 30 bold")



	def drawGameOverScreen(self):
		self.canvas.create_rectangle(0,0,self.width,self.height,fill  ="turquoise4",outline = "turquoise4")
		displayBoxSize = 150
		self.canvas.create_rectangle(5,self.height/2-displayBoxSize ,self.width-2,self.height/2+displayBoxSize,
			fill = "white",outline = "gray70",width = 5)
		self.canvas.create_text(self.width/2,self.height/2.9,text= "Were you thinking of: "+"\n",
								fill = "gray27", font = "Helvetica 30 bold")
		text = ""
		for key in self.eliminatedDict:
			text += str(key)+"\n"
		self.canvas.create_text(self.width/2,self.height/1.8,text = text,fill = "gray27",
								font = "Helvetica 30 bold")
	def drawBackground(self):
		image = PhotoImage(file=self.file)
		self.canvas.data["image"] = image
		image = self.canvas.data["image"]
		self.canvas.create_image(self.width/2,self.height/2,image=image)

	def drawStartScreen(self):
		image = PhotoImage(file = "StartScreen.gif")
		self.canvas.data["image"] = image
		image = self.canvas.data["image"]
		self.canvas.create_image(self.width/2,self.height/2,image=image)

	def questionsDict(self):
		self.questionsDict = {}
		self.questionsDict["Gender"] = "Is your character's gender male?"
		self.questionsDict["Alive"] = "Is your character alive?"
		self.questionsDict["Age"] = "Is/Was your character older than or equal to "
		self.questionsDict["Nationality"] = "Is your character's nationality "
		self.questionsDict["Profession"] = "Is your character a "
		self.questionsDict["Married"] = "Is/Was your character married?"
		self.questionsDict["Children"] = "Does/Did your character have children?"


	def questionSelector(self):
		if(self.keyToAsk!=None):
			if(self.attribute!=None):
				self.questionToAsk = self.questionsDict[self.keyToAsk]+str(self.attribute)+"?"
			else:
				self.questionToAsk = self.questionsDict[self.keyToAsk]



	def drawQuestion(self):
		if(self.questionToAsk!=None):
			text = self.questionToAsk
			self.canvas.create_text(self.width/2,self.height/4,
				text=  text,font = "Helvetica 30 bold",fill = "gray27")

	def drawButtons(self):
		self.drawYesButton()
		self.drawNoButton()



	def drawButtonText(self):
		self.canvas.create_text(self.width/2,self.startButtonY+self.buttonHeight/2,
			text=  'Yes',font = "Helvetica 25 bold",fill = "gray27")
		self.canvas.create_text(self.width/2,
			self.startButtonY+self.buttonHeight/2+(self.buttonHeight*2),
			text=  'No',font = "Helvetica 25 bold",fill = "gray27")
	
	def drawHelpButton(self):
		ovalRadius = 16
		self.helpButtonLeftX = self.width-self.width/15-ovalRadius
		self.helpButtonRightX = self.width-self.width/15+ovalRadius
		self.helpButtonUpY = self.height-self.height/15-ovalRadius
		self.helpButtonDownY = self.height-self.height/15+ovalRadius
		if(self.helpHovered==False):
			self.canvas.create_oval(self.helpButtonLeftX,
				self.helpButtonUpY,self.helpButtonRightX,
				self.helpButtonDownY,fill = "white",outline = "gray70",
				width=2.5)
			self.canvas.create_text(self.width-self.width/15,self.height-self.height/15,
				text = "?",font ="Helvetica 19 bold",fill = "gray27")
		else:
			self.canvas.create_oval(self.helpButtonLeftX,
				self.helpButtonUpY,self.helpButtonRightX,
				self.helpButtonDownY,fill = self.buttonDownMain,
				outline = self.buttonDownLine,
				width=2.5)
			self.canvas.create_text(self.width-self.width/15,self.height-self.height/15,
				text = "?",font ="Helvetica 19 bold",fill = "gray27")



	
	def drawQuestionBox(self):
		rectangleSize = 45
		self.canvas.create_rectangle(5,self.height/4-rectangleSize,self.width-3,
			self.height/4+rectangleSize,fill = "white",outline = "gray70",width = 5)


	def drawYesButton(self):
		self.YesStartX =self.startButtonX
		self.YesStartY = self.startButtonY
		self.YesEndX = self.startButtonX+self.buttonWidth
		self.YesEndY = self.startButtonY+self.buttonHeight

		if(self.YesHovered==False):
			self.canvas.create_rectangle(self.YesStartX,self.YesStartY,self.YesEndX,
				self.YesEndY,fill = self.buttonUpMain,outline = self.buttonUpMain)

			self.canvas.create_rectangle(self.YesStartX,self.YesEndY-self.buttonMargin,
				self.YesEndX,self.YesEndY,fill =self.buttonUpLine,outline = self.buttonUpLine)
		else:
			self.canvas.create_rectangle(self.YesStartX,self.YesStartY,self.YesEndX,
				self.YesEndY,fill = self.buttonDownMain,outline = self.buttonDownMain)

			self.canvas.create_rectangle(self.YesStartX,self.YesStartY,
				self.YesEndX,self.YesStartY+self.buttonMargin,fill =self.buttonDownLine,
				outline = self.buttonDownLine)



	def drawNoButton(self):
		self.NoStartX =self.startButtonX
		self.NoStartY = self.startButtonY+(self.buttonHeight*2)
		self.NoEndX = self.startButtonX+self.buttonWidth
		self.NoEndY = self.startButtonY+self.buttonHeight+(self.buttonHeight*2)

		if(self.NoHovered==False):
			self.canvas.create_rectangle(self.NoStartX,self.NoStartY,self.NoEndX,
				self.NoEndY,fill = self.buttonUpMain,outline = self.buttonUpMain)

			self.canvas.create_rectangle(self.NoStartX,self.NoEndY-self.buttonMargin,
				self.NoEndX,self.NoEndY,fill =self.buttonUpLine,outline = self.buttonUpLine)
		else:
			self.canvas.create_rectangle(self.NoStartX,self.NoStartY,self.NoEndX,
				self.NoEndY,fill = self.buttonDownMain,outline = self.buttonDownMain)

			self.canvas.create_rectangle(self.NoStartX,self.NoStartY,
				self.NoEndX,self.NoStartY+self.buttonMargin,fill =self.buttonDownLine,
				outline = self.buttonDownLine)


#The code from here is directly taken from the dictMaker file
	def singleConverter(self,person):
		orgStr  ="http://en.wikipedia.org/wiki/"
		person = person.replace(" ","_")
		personLinked = (orgStr+person)
		return personLinked


	def fullTextGetter(self,person):
		url = self.singleConverter(person)
		fullFile = urllib.urlopen(url)
		fullText= fullFile.read()
		return fullText


	def wikipediaInfoScraper(self,person):
		url = self.singleConverter(person)
		htmlfile = urllib.urlopen(url)
		htmltext = htmlfile.read()
		fullFile = copy.deepcopy(htmltext)
		index = htmltext.index("<table")
		index2 = htmltext.index("</table>")
		htmltext =  htmltext[index:index2]
		found = True
		return htmltext


	def getFirstPara(self,person):
		try:
			urlFind = self.singleConverter(person)
			htmlfile = urllib.urlopen(urlFind)
			htmltext = htmlfile.read()
			startParaFound = False
			while startParaFound==False:
				indexOfParaStart = htmltext.index("<p>")
				indexOfParaEnd = htmltext.index("</p>",indexOfParaStart)
				if(indexOfParaEnd-indexOfParaStart>=300):
					startParaFound= True
				else:
					htmltext  =htmltext[indexOfParaStart+1:]

			indexOfEndPara = htmltext.index("</p>",indexOfParaStart)
			uneditedFirstPara = htmltext[indexOfParaStart:indexOfEndPara+1]
			editedFirstPara = self.tagRemover(uneditedFirstPara)
			editedFirstPara = editedFirstPara.lower()
		except:
			editedFirstPara = ""
		return editedFirstPara




	#The following function makes key-val tag pairs for a particular inputted person
	def makePersonDict(self,personInfo,firstPara):
		personDict = dict()
		gender = self.getGender(firstPara)
		profession = self.getProfession(firstPara)
		personDict["Profession"]  =profession
		personDict["Gender"] = gender
		personDict["Children"] = False
		personDict["Married"] = False
		personDict["Nationality"] = "Unknown"
		personDict["Alive"] = True
		nextIndex = 0
		while(personInfo.find('<tr>')!=-1):
			tableRowTextStartIndex = personInfo.find("<tr>",nextIndex)
			if(personInfo.find("<tr>",nextIndex)==-1):
				break
			tableRowTextEndIndex = personInfo.find("</tr>",nextIndex)
			nextIndex =tableRowTextEndIndex+1
			tableRowText = personInfo[tableRowTextStartIndex:tableRowTextEndIndex]
			if(self.doubleTagChecker(tableRowText)==True):
				thText=  self.getThTag(tableRowText)
				tdText =self.getTdTag(tableRowText)
				thKey = self.thkeyGetter(thText)
				tdVal = self.tdValGetter(tdText)
				if(thKey == "Born"):
					personDict = self.bornTagSegregator(tableRowText,personDict)
				elif(thKey=="Died"):
					personDict = self.diedTagSegregator(tableRowText,personDict)
				else:
					personDict = self.otherTagsChecker(thKey,personDict,tdVal)
		return personDict



	def getGender(self,text):
		hisNumber = text.count("his ")+text.count("His ")
		himNumber = text.count("him ")+text.count("Him ")
		heNumber  =	text.count("he ")+text.count("He ")
		sheNumber = text.count("she ")+text.count("She ")
		herNumber = text.count("her ")+text.count("Her ")
		theNumber = text.count("the ")+text.count("The ")
		heNumber  = heNumber- theNumber - sheNumber
		if(hisNumber+heNumber)>(sheNumber+herNumber):
			gender = "Male"
		elif(hisNumber+heNumber)<(sheNumber+herNumber):
			gender = "Female"
		elif(himNumber>0):
			gender = "Male"
		else:
			gender = "Unknown"
		return gender

	def getProfession(self,text):
		finalProfession =False
		professionList = ["president","prime minister",
		"actor","rapper","vice-president","politician",
		"chef","writer","singer","official","teacher","poet",
		"painter","scluptor","mathematician","scientist","inventor",
		"engineer","leader","judge","dancer","model","actress",
		"basketball player","soccer player","football player",
		"entrepreneur","author","pope"]
		startProfessionIndex = len(text)
		for profession in xrange(len(professionList)):
			if(professionList[profession] in text):
				if(text.index(professionList[profession])
					<=startProfessionIndex):
					finalProfession = professionList[profession]
					startProfessionIndex = text.index(professionList[profession])
		return finalProfession





	def otherTagsChecker(self,thKey,personDict,tdVal):
		if(thKey=="Spouse(s)" or thKey =="Wives"):
			personDict["Married"] = True
		elif(thKey=="Children"):
			personDict["Children"] = True
		elif(thKey=="Nationality"):
			personDict["Nationality"] = tdVal
		return personDict


	def thkeyGetter(self,thText):
		while(thText.find(">")!=-1):
			startThTagIndex = thText.index("<")
			endThTagIndex = thText.index(">",startThTagIndex)
			thText = thText[:startThTagIndex]+thText[endThTagIndex+1:]
		return thText



	def tdValGetter(self,tdText):
		while(tdText.find(">")!=-1):
			startTdTagIndex = tdText.index("<")
			endTdTagIndex = tdText.index(">",startTdTagIndex)
			tdText = tdText[:startTdTagIndex]+tdText[endTdTagIndex+1:]
		return tdText


	def getThTag(self,text):
		try:
			startThIndex = text.index("<th")
			endThIndex = text.index("</th>")
			thText = text[startThIndex:endThIndex+len("</th>")]
		except:
			thText = "None"
		return thText


	def getTdTag(self,text):
		try:
			startTdIndex = text.index("<td")
			endTdIndex = text.index("</td>")
			tdText = text[startTdIndex:endTdIndex+len("</td>")]
		except:
			tdText = "None"
		return tdText



	def tagRemover(self,text):
		while(text.find(">")!=-1):
			openTagIndex = text.index("<")
			closeTagIndex = text.index(">",openTagIndex)
			text = text[:openTagIndex]+text[closeTagIndex+1:]
		return text

	#The following function checks whether <th> and <td> both exist in a <tr> tag
	def doubleTagChecker(self,partOfText):
		if('<th' in partOfText and '<td' in partOfText):
			return True
		return False


		
	def bornTagSegregator(self,text,personDict):
		text = copy.deepcopy(text)
		try:
			indexToCheckFrom = text.find("bday")
			indexOfTagAfterBirthday = text.find(">",indexToCheckFrom)
			indexAfterBirthYear = text.find("-",indexOfTagAfterBirthday)
			birthYear = text[indexOfTagAfterBirthday+1:indexAfterBirthYear]
			personDict["Birthyear"] = str(birthYear)
			age = (date.today().year)-int(birthYear)
			personDict["Age"]  =str(age)
			personDict["Deathyear"] = False
		except:
			personDict["Birthyear"] = "Unknown"
			personDict["Age"] = "Unknown"
			personDict["Deathyear"] = False

		return personDict


		

	def diedTagSegregator(self,text,personDict):
		try:
			indexToCheckFrom = text.find("deathdate")
			indexDateTime = text.find("datetime",indexToCheckFrom)
			deathYear = "Unknown"
			if(indexDateTime!=-1):
				indexOfInvertedComma = text.find('"',indexDateTime)
				indexAfterDeathYear = text.find("-",indexOfInvertedComma)
				deathYear = text[indexOfInvertedComma+1:indexAfterDeathYear]
			else:
				indexOfTagAfterDeathday = text.find(">",indexToCheckFrom)
				indexAfterDeathYear = text.find("-",indexOfTagAfterDeathday)
				deathYear = text[indexOfTagAfterDeathday+1:indexAfterDeathYear]
			personDict["Deathyear"] = str(deathYear)
			ageDied = int(personDict["Deathyear"])-int(personDict["Birthyear"])
			personDict["Age"] = str(ageDied)
			personDict["Alive"]  =False
		except:
			personDict["Deathyear"] = "Unknown"
			personDict["Age"] = "Unknown"
			personDict["Alive"] = False

		return personDict



playGame = TwentyQuestionsGame()

playGame.run()
