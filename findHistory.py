from config import *
import pandas as pd


#Initialize full term list with 1st term,
#then import all old schedules
allTerms=pd.read_csv(terms[0]['termSchedule'])
allTerms['termName']=terms[0]['name']
for thisTerm in terms[1:]:
    newTerm=pd.read_csv(thisTerm['termSchedule'])
    newTerm['termName']=thisTerm['name']
    allTerms=allTerms.append(newTerm, ignore_index=True)


#Get rid of this term in the data
allTerms=allTerms[~allTerms['termName'].isin(termNames)]

#Only care about these two columns
allTerms=allTerms[['termName','title']]
allTerms.drop_duplicates(inplace=True)

#To figure out frequency
numTermHistory=len(terms)-1.0

def getFrequencyWords(value):
    if value==1.0:
        return 'Every Semester'
    elif value>= 0.2:
        return 'Most Years'
    elif value > 0:
        return 'Infrequent'
    else:
        return '1st Time Offered'

#To be called in rendering to find previous
#instances of this term
#Takes a class title. Returns the frequency as defined above, and
#if the frequency <1, the specific terms it's been seen
#class titles are about as unique as you can get
def getPriorTerms(title):
    priorNames=allTerms['termName'][allTerms['title']==title].values.tolist()
    prettyNames=[]
    for thisTerm in terms:
        if thisTerm['name'] in priorNames:
            prettyNames.append(thisTerm['prettyName'])

    freq=len(prettyNames)/numTermHistory*1.0
    if freq == 1.0:
        lastSeen='Every Semester'
    else:
        lastSeen=','.join(prettyNames)
    return( {'frequency': getFrequencyWords(freq),
             'lastSeen': lastSeen }
             )

#This is just for testing this script
#thisYear=pd.read_csv('semesterData/201601.csv')
#for thisClass in thisYear['title'].values.tolist():
#    print(getPriorTerms(thisClass))
