import urllib
import re,copy,csv,os
from datetime import date


def singleConverter(person):
	orgStr  ="http://en.wikipedia.org/wiki/"
	person = person.replace(" ","_")
	personLinked = (orgStr+person)
	return personLinked


def fullTextGetter(person):
	url = singleConverter(person)
	fullFile = urllib.urlopen(url)
	fullText= fullFile.read()
	return fullText


def wikipediaInfoScraper(person):
	url = singleConverter(person)
	htmlfile = urllib.urlopen(url)
	htmltext = htmlfile.read()
	fullFile = copy.deepcopy(htmltext)
	index = htmltext.index("<table")
	index2 = htmltext.index("</table>")
	htmltext =  htmltext[index:index2]
	found = True
	return htmltext


def getFirstPara(person):
	try:
		urlFind = singleConverter(person)
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
		editedFirstPara = tagRemover(uneditedFirstPara)
		editedFirstPara = editedFirstPara.lower()
	except:
		editedFirstPara = ""
	return editedFirstPara




#The following function makes key-val tag pairs for a particular inputted person
def makePersonDict(personInfo,firstPara):
	personDict = dict()
	gender = getGender(firstPara)
	profession = getProfession(firstPara)
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
		if(doubleTagChecker(tableRowText)==True):
			thText=  getThTag(tableRowText)
			tdText =getTdTag(tableRowText)
			thKey = thkeyGetter(thText)
			tdVal = tdValGetter(tdText)
			if(thKey == "Born"):
				personDict = bornTagSegregator(tableRowText,personDict)
			elif(thKey=="Died"):
				personDict = diedTagSegregator(tableRowText,personDict)
			else:
				personDict = otherTagsChecker(thKey,personDict,tdVal)
	return personDict



def getGender(text):
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

def getProfession(text):
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





def otherTagsChecker(thKey,personDict,tdVal):
	if(thKey=="Spouse(s)" or thKey =="Wives"):
		personDict["Married"] = True
	elif(thKey=="Children"):
		personDict["Children"] = True
	elif(thKey=="Nationality"):
		personDict["Nationality"] = tdVal


	return personDict

def thkeyGetter(thText):
	while(thText.find(">")!=-1):
		startThTagIndex = thText.index("<")
		endThTagIndex = thText.index(">",startThTagIndex)
		thText = thText[:startThTagIndex]+thText[endThTagIndex+1:]
	return thText



def tdValGetter(tdText):
	while(tdText.find(">")!=-1):
		startTdTagIndex = tdText.index("<")
		endTdTagIndex = tdText.index(">",startTdTagIndex)
		tdText = tdText[:startTdTagIndex]+tdText[endTdTagIndex+1:]
	return tdText


def getThTag(text):
	try:
		startThIndex = text.index("<th")
		endThIndex = text.index("</th>")
		thText = text[startThIndex:endThIndex+len("</th>")]
	except:
		thText = "None"
	return thText


def getTdTag(text):
	try:
		startTdIndex = text.index("<td")
		endTdIndex = text.index("</td>")
		tdText = text[startTdIndex:endTdIndex+len("</td>")]
	except:
		tdText = "None"
	return tdText



def tagRemover(text):
	while(text.find(">")!=-1):
		openTagIndex = text.index("<")
		closeTagIndex = text.index(">",openTagIndex)
		text = text[:openTagIndex]+text[closeTagIndex+1:]
	return text

#The following function checks whether <th> and <td> both exist in a <tr> tag
def doubleTagChecker(partOfText):
	if('<th' in partOfText and '<td' in partOfText):
		return True
	return False


	
def bornTagSegregator(text,personDict):
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


	

def diedTagSegregator(text,personDict):
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



def saveToFinalDict(peopleDict):
	w = csv.writer(open("finalDictionary.csv", "w"))
	for key, val in peopleDict.items():
	    w.writerow([key, val])

def getFromFinalDict():
	peopleDict  = {}
	if(os.path.exists("finalDictionary.csv")):
		for key, val in csv.reader(open("finalDictionary.csv")):
			peopleDict[key] = val
	return peopleDict

def getListFromPreMadeFile():
	if(os.path.exists("listOfPeople.txt")):
		file =open("listOfPeople.txt",'r')#opens file
		stringOfList = file.read()
		file.close()
		stringToAdd = ""
		listOfString = []
		for letter in xrange(len(stringOfList)):
			if(letter==len(stringOfList)-1):
				stringToAdd+=stringOfList[letter]
				listOfString.append(stringToAdd)
			elif(stringOfList[letter]!=','):
				stringToAdd +=stringOfList[letter]
			else:
				listOfString.append(stringToAdd)
				stringToAdd = ""
	return listOfString


def getFromFileDictNumber():
	if(os.path.exists("dictNumberToStart.txt")):
		returnNumber = False
		file =open("dictNumberToStart.txt",'r')#opens file
		contents = file.read()
		file.close()
	else:
		file = open('dictNumberToStart.txt', 'w')#opesn file
		contents = "1"
		file.write("1")
		file.close()
	return contents


def saveToFileDictNumber(numberToStore):
	writeString = str(numberToStore)
	file = open('dictNumberToStart.txt', 'w')#opesn file
	file.write(writeString)
	file.close()


#Makes a dict with Names as the Key and their tags as the val
def makePeopleDict():
	#Stores the names of the people
	peopleList = getListFromPreMadeFile()
	numberToStart = int(getFromFileDictNumber())
	packOfPeople = 10
	peopleList = peopleList[(packOfPeople*(numberToStart-1)):(packOfPeople*(numberToStart))]
	print peopleList
	nameOfPeople  = copy.deepcopy(peopleList) 
	#makes a dict that will contain all the people
	peopleDict = getFromFinalDict()
	#Makes a wikipedis searchable list of people
	for person in xrange(len(nameOfPeople)):
		personInfo = wikipediaInfoScraper(nameOfPeople[person])
		fullText = fullTextGetter(nameOfPeople[person])
		firstPara = getFirstPara(nameOfPeople[person])
		print "Making Dict for Person: "+str(nameOfPeople[person])
		personDict = makePersonDict(personInfo,firstPara)
		personDict["Name"] = str(nameOfPeople[person])
		if(("Birthyear" not in personDict) or ("Deathyear" not in personDict)):
			personDict = bornTagSegregator(fullText,personDict)
			personDict = diedTagSegregator(fullText,personDict)
		peopleDict[nameOfPeople[person]] = personDict
	saveToFinalDict(peopleDict)
	numberToStore = numberToStart+1
	print numberToStore
	saveToFileDictNumber(numberToStore)
	return peopleDict#returns the dict of people made



makePeopleDict()


"""
info = wikipediaInfoScraper("Akbar")
firstPara = getFirstPara("Akbar")
print makePersonDict(info,firstPara)
"""
