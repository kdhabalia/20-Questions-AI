import os,copy,csv,random,re,urllib,ast

def getFullDict():
	fullDict  = {}
	if(os.path.exists("filteredDictionary.csv")):
		for key, val in csv.reader(open("filteredDictionary.csv")):
			fullDict[key] = val
	return fullDict


def makeDecisionTree():
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


def eliminatorWrapper():
	fullDict = getFullDict()
	eliminatedDict = copy.deepcopy(fullDict)
	decisionTree = makeDecisionTree()
	eliminatedDict = eliminator(eliminatedDict,decisionTree)
	for key in eliminatedDict:
		print key
	return eliminatedDict


def eliminator(eliminatedDict,decisionTree):
	decisionList = copy.deepcopy(decisionTree)
	if(type(decisionList)==str or len(eliminatedDict)<5):
		return eliminatedDict
	else:
		if(decisionList[0]=="Nationality"):
			print decisionList[0]
			nationality = mostCommonNationality(eliminatedDict)
			print nationality
			choice = raw_input("Enter choice: ")
			eliminatedDict = removeFromDict(choice,eliminatedDict,decisionList[0],nationality)
			if(choice=="y"):
				decisionList = decisionList[1]
			elif(choice=="n"):
				decisionList = decisionList[2]
			return eliminator(eliminatedDict,decisionList)
		elif(decisionList[0]=="Profession"):
			print decisionList[0]
			profession = mostCommonProfession(eliminatedDict)
			print profession
			choice = raw_input("Enter choice: ")
			eliminatedDict = removeFromDict(choice,eliminatedDict,decisionList[0],profession)
			if(choice=="y"):
				decisionList = decisionList[1]
			elif(choice=="n"):
				decisionList = decisionList[2]
			return eliminator(eliminatedDict,decisionList)
		elif(decisionList[0]=="Age"):
			print decisionList[0]
			age = halfAgeCalculator(eliminatedDict)
			print "Greater than: ", age
			choice = raw_input("Enter choice: ")
			eliminatedDict = removeFromDict(choice,eliminatedDict,decisionList[0],age)
			if(choice=="y"):
				decisionList = decisionList[1]
			elif(choice=="n"):
				decisionList = decisionList[2]
			return eliminator(eliminatedDict,decisionList)
		else:
			print decisionList[0]
			choice = raw_input("Enter choice: ") 
			eliminatedDict = removeFromDict(choice,eliminatedDict,decisionList[0],None)
			if(choice=="y"):
				decisionList = decisionList[1]
			elif(choice=="n"):
				decisionList = decisionList[2]
			return eliminator(eliminatedDict,decisionList)

def removeFromDict(choice, eliminatedDict,key,attribute):
	print "Before removing: ",len(eliminatedDict)
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
				if(int(subDict[key])<=attribute):
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
				if(int(subDict[key])>attribute):
					keysToBeRemoved.append(nameKey)
		else:
			for nameKey in eliminatedDict:
				subDict = ast.literal_eval(eliminatedDict[nameKey])
				if(subDict[key]==True or subDict[key]=="Male"):
					keysToBeRemoved.append(nameKey)

	for remove in keysToBeRemoved:
		del eliminatedDict[remove]
	print "After removing: ",len(eliminatedDict)
	return eliminatedDict



	


		
def halfAgeCalculator(eliminatedDict):
	ageTotal = 0
	for nameKey in eliminatedDict:
		subDict = ast.literal_eval(eliminatedDict[nameKey])
		ageTotal += int(subDict["Age"])
	ageAverage = ageTotal/len(eliminatedDict)
	return ageAverage

def mostCommonProfession(eliminatedDict):
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

	maxFreq = max(professionFrequency)
	indexToGet = professionFrequency.index(maxFreq)
	mostCommonProfessionToAsk = professionList[indexToGet]
	return mostCommonProfessionToAsk


def mostCommonNationality(eliminatedDict):
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
	maxFreq = max(nationalityFreqList)
	indexToGet = nationalityFreqList.index(maxFreq)
	mostCommonNationalityToAsk = nationalityList[indexToGet]
	return mostCommonNationalityToAsk



eliminatorWrapper()

