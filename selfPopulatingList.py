import urllib
import re,copy,os




def getFromFile():
	if(os.path.exists("listOfPeople.txt")):
		returnNumber = False
		file =open("listOfPeople.txt",'r')#opens file
		contents = file.read()
		file.close()
	else:
		returnNumber = True
		firstList = ["Barack Obama","Mahatma Gandhi","Adolf Hitler",
		"Jesus","Steve Jobs","Alexander The Great",
		"Kanye West","Narendra Modi","Akbar"]
		contents = listToStringConverter(firstList)
		file = open('listOfPeople.txt', 'w')#opesn file
		file.write(contents)l
		file.close()
	return contents,returnNumber

def getFromFileCheckNumber():
	if(os.path.exists("checkNumberToStart.txt")):
		returnNumber = False
		file =open("checkNumberToStart.txt",'r')#opens file
		contents = file.read()
		file.close()
	else:
		file = open('checkNumberToStart.txt', 'w')#opesn file
		contents = "1"
		file.write("1")
		file.close()
	return contents


def saveToFileCheckNumber(numberToStart):
	writeString = str(numberToStart+1)
	file = open('checkNumberToStart.txt', 'w')#opesn file
	file.write(writeString)
	file.close()


def saveToFile(contentsToWrite):
	file = open('listOfPeople.txt', 'w')#opesn file
	file.write(contentsToWrite)
	file.close()


	

def listToStringConverter(peopleList):
	listToBeSaved = ','.join(peopleList)
	return listToBeSaved


def stringToListConverter(stringOfList):
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


def listConverter(peopleList):
	orgStr  ="http://en.wikipedia.org/wiki/"
	urlList = []
	for i in xrange(len(peopleList)):
		peopleList[i] = peopleList[i].replace(" ","_")
		urlList.append(orgStr+peopleList[i])

	return urlList



def checkIsPerson(wikiLink):
	orgStr = "http://en.wikipedia.org/wiki/"
	wikiLink.replace(" ","_")
	wikiLink = orgStr+wikiLink
	htmlfile = urllib.urlopen(wikiLink)
	htmltext = htmlfile.read()
	if("<table" in htmltext):
		index = htmltext.index("<table")
		index2 = htmltext.index("</table>")
		htmltext =  htmltext[index:index2]
		toCheckString = "Born</th>"
		if(toCheckString in htmltext):
			return True
	return False



def findLinkTags(person,peopleList):
	toFindString = '<a href="/wiki/'
	finder = '"'
	fullFile = urllib.urlopen(person)
	fullText = fullFile.read()
	linkList = []
	checkedList = []
	while (fullText.find(toFindString)!= -1 and len(linkList)<3):
		startIndex = fullText.index(toFindString)
		endIndex = startIndex+len(toFindString)
		finderIndex = fullText.index(finder,endIndex)
		linkName = fullText[endIndex:finderIndex]
		fullText = fullText[finderIndex+1:]
		linkName = linkName.replace("_"," ")
		linkName = linkName.replace(",","")
		if(excessChecker(linkName)==True and linkName not in linkList
			and linkName not in checkedList and linkName not in peopleList):
			checkedList.append(linkName)
			print "Checking Page: "+linkName
			if(checkIsPerson(linkName)==True):	
				linkList.append(linkName)
	return linkList




def excessChecker(linkName):
	unwantedList = ["(disambiguation)",".jpg","Wikipedia","File",":","("]
	for excess in unwantedList:
		if(excess in linkName):
			return False
	if(linkName.count(" ")<1 or linkName.count(" ")>3):
		return False
	for number in xrange(0,10):
		if str(number) in linkName:
			return False
	return True



def getAllLinks():
	(peopleList,orgListCheck) = (getFromFile())
	numberToStart = int(getFromFileCheckNumber())
	print numberToStart
	peopleList = stringToListConverter(peopleList)
	maxVal = 10
	copyOfPeopleList= copy.deepcopy(peopleList)
	allPeople = listConverter(peopleList)
	lenoflist  = len(allPeople)
	if(orgListCheck):
		person = 0
		goThroughPerson  =person
	else:
		person = 0
		goThroughPerson = (maxVal*(numberToStart-1))-1

	while (person < lenoflist and person<maxVal):
		listOfLinkedPeople = findLinkTags(allPeople[goThroughPerson],copyOfPeopleList)
		copyOfPeopleList +=listOfLinkedPeople
		allPeople += listConverter(listOfLinkedPeople)
		person+=1
		goThroughPerson+=1
		lenoflist  = len(allPeople)
	stringToStore = listToStringConverter(copyOfPeopleList)
	saveToFile(stringToStore)
	saveToFileCheckNumber(numberToStart)
	return allPeople,copyOfPeopleList



print getAllLinks()






