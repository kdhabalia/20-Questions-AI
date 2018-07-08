import os,copy,re,urllib,csv,ast

def getUnfilteredDict():
	unfilteredDict  = {}
	if(os.path.exists("finalDictionary.csv")):
		for key, val in csv.reader(open("finalDictionary.csv")):
			unfilteredDict[key] = val
	return unfilteredDict


def filterDict():
	unfilteredDict = getUnfilteredDict()
	filteredDict = copy.deepcopy(unfilteredDict)
	print "Length of dictionary before: ",len(unfilteredDict)
	keysToBeRemoved = []
	for nameKey in filteredDict:
		subDict = ast.literal_eval(filteredDict[nameKey])
		if("Age" not in subDict):keysToBeRemoved.append(nameKey)  
		if(subDict["Gender"]=="Unknown" or 
			(subDict["Birthyear"]=="Unknown" and 
			subDict["Deathyear"]=="Unknown" and
			subDict["Profession"]=="False" and
			subDict["Nationality"]=="Unknown") or 
			subDict["Age"]=="Unknown" ):
			keysToBeRemoved.append(nameKey)             
	for remove in keysToBeRemoved:
		del filteredDict[remove]
	print "Length of dictionary after: ",len(filteredDict)
	saveFilteredDictToFile(filteredDict)


		

def saveFilteredDictToFile(filteredDict):
	w = csv.writer(open("filteredDictionary.csv", "w"))
	for key, val in filteredDict.items():
	    w.writerow([key, val])


filterDict()