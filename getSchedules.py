import urllib.request as urllib
from bs4 import BeautifulSoup as bs
import pandas as pd
import os.path

baseURL='http://www.registrar.ufl.edu/soc/'
#Semesters are yyyy + 08 for spring, 01 for fall, 06 for summer
semesters=['201008',
           '201108','201101',
           '201208','201201',
           '201308','201301',
           '201408','201401',
           '201508','201501',
           '201601'
           ]

semesterFolder='semesterData/'
#if you add or subtract columns then you need to adjust the getClassList function accordingly
#xxxx2 are for when there is a 2nd row with more schedule info. For labs, meeting times in different buildings, etc.
columns=['coursePrefix','courseNum','fee','section','credits','days','times','building','room','title','prof',
         'days2','times2','building2','room2']


def getDepts(url):
    #for each semester's beginning schedule page, get a list of all dept sub pages
    #with actual classes on them
    pageHTML=urllib.urlopen(url)
    pageSoup=bs(urllib.urlopen(url), 'lxml')
    deptPages=[]
    for thisRow in pageSoup.find_all('table')[0].find_all('option'):
        #The 1st entry for these isn't something we want
        if thisRow.attrs['value']:
            deptPages.append(thisRow.attrs['value'])
    return(deptPages)


def getClassList(url):
    #accepts a url for a specific dept/semester and extracts all classes from it. 
    #returns a pandas DF
    pageHTML=urllib.urlopen(url)
    pageSoup=bs(urllib.urlopen(url), 'lxml')

    courseList=pd.DataFrame(columns=columns)

    for thisRow in pageSoup.find_all('table')[1].find_all('tr'):
        #Skip the beginning few rows which are header info
        if len(thisRow)!=22:
            continue
        #Get a list of all 'td' (which corrospond to columns)
        #and pull out relevant info from each
        thisRow=thisRow.find_all('td')

        #The 1st entry is like "WIS 6934", so split those up to be more usefull
        first=thisRow[0].get_text().split(' ')

        #if the the 1st entry is empty then this row is extra info from the prior row.
        #append the date information to the previous entry and move on
        if len(first)==1:
            #Index for the previous row is just the length -1
            priorRow=courseList.shape[0]-1

            courseList.loc[priorRow,'days2']=thisRow[7].get_text().strip()
            courseList.loc[priorRow,'times2']=thisRow[8].get_text()
            courseList.loc[priorRow,'building2']=thisRow[9].get_text()
            courseList.loc[priorRow,'room2']=thisRow[10].get_text()

            continue

        #If row is a new class append it to a new row in the DF using a dict
        rowData={}
        rowData['coursePrefix']=first[0]
        rowData['courseNum']=first[1]

        rowData['fee']=thisRow[1].get_text()
        rowData['section']=thisRow[5].get_text().replace('\n','') #section #'s all have annoying newlines
        rowData['credits']=thisRow[6].get_text().strip() #get rid of leading spaces
        rowData['days']=thisRow[7].get_text().strip()
        rowData['times']=thisRow[8].get_text()
        rowData['building']=thisRow[9].get_text()
        rowData['room']=thisRow[10].get_text()
        rowData['title']=thisRow[12].get_text().replace('\n','') #get rid of newlines
        rowData['prof']=thisRow[13].get_text().replace('\n','',1).replace('\n',';')
                                                                 #get rid of newlines but keep a seperater between
                                                                 #multiple profs

        
        courseList=courseList.append(rowData, ignore_index=True)

    return(courseList)

#Check that a semesters class list is downloaded, if not go and get it
#If you want to re-download a semester (like for updated classes), then 
#just delete that one in the local folder
for thisSemester in semesters:
    dataFile=semesterFolder+thisSemester+'.csv'
    if os.path.exists(dataFile):
        print('Semester data file exists, skipping: ',dataFile)
        continue

    #Get all the dept subpages of schedules, process each and add to
    #a large dataframe for this semester.
    semesterURL=baseURL+thisSemester+'/all/'
    deptList=getDepts(semesterURL)
    semesterCourseList=pd.DataFrame(columns=columns)
    for thisDept in deptList:
        deptURL=semesterURL+thisDept
        try:
            semesterCourseList=semesterCourseList.append( getClassList(deptURL), ignore_index=True)
        #Continue on if it's just a 404 error, otherwise halt
        except urllib.HTTPError as err:
            if err.code ==404:
                print('page not found', deptURL)
                continue
            else:
                raise

    
    #write semester data frame
    semesterCourseList.to_csv(dataFile, index=False)

