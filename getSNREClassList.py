import urllib.request as urllib
from bs4 import BeautifulSoup as bs
import pandas as pd
import os.path

baseURL='http://snre.ufl.edu/graduate/curriculum.htm'
classListFile='SNREList.csv'

#Only run if this datafile doesn't exist
if os.path.exists(classListFile):
    print('SNRE List exists. Delete it if you want to remake it: ', classListFile)
    exit()

pageSoup=bs(urllib.urlopen(baseURL), 'lxml')

#find the different class catagories. Priciples of Ecology, Particular Perspectives, etc
def isSubCatagory(tag):
    return tag.name=='div' and 'id' in tag.attrs \
            and 'fragment' in tag.attrs['id']

#Within each subcatagory, find the rows (tr) that are actuall class listings.
#They will have more than 2 <td> entries
def isClassListing(tag):
    return tag.name=='tr' and len(tag.find_all('td'))>2

classList=pd.DataFrame(columns=['coursePrefix','courseNum','title','subCategory'])

#
#Setup subcategories with curriculum. 
subCategoryList=['Principles of Ecology',
        'Particular Systems',
        'Natural Science',
        'Social Science',
        'Sustainability',
        'Research & Design']


subCategoryCount=0
for sub in pageSoup.find_all(isSubCatagory):
    thisSubCategory=subCategoryList[subCategoryCount]
    subCategoryCount+=1
    for classListing in sub.find_all(isClassListing):
        classEntry={}
        classListing=classListing.find_all('td')

        #Some one off entries that need special handling
        if '6215L' in classListing[0].get_text():
            classListing[0].string='ENV 6215/ENV 6215L'
        if '4043C' in classListing[0].get_text():
            classListing[0].string='PCB 4043C'
        #Some entries have two course numbers for one class, seperated by a /
        #If thats the case, put the 2nd on in the list, then take it out and add
        #the first one as normal
        if '/' in classListing[0].get_text():
            #Add the 2nd entry to the list
            secondEntry={}
            secondEntry['coursePrefix']=classListing[0].get_text().split('/')[1].split(' ')[0]
            secondEntry['courseNum']=classListing[0].get_text().split('/')[1].split(' ')[1]
            secondEntry['title']=classListing[1].get_text()
            classList=classList.append(secondEntry, ignore_index=True)
            #Remove the 2nd entry so the 1st gets added below
            classListing[0].string=classListing[0].get_text().split('/')[0]

        classEntry['coursePrefix']=classListing[0].get_text().split(' ')[0]
        classEntry['courseNum']=classListing[0].get_text().split(' ')[1]
        classEntry['title']=classListing[1].get_text()
        classEntry['subCategory']=thisSubCategory

        classList=classList.append(classEntry, ignore_index=True)

classList.to_csv(classListFile, index=False)
