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

classList=pd.DataFrame(columns=['coursePrefix','courseNum','title'])

#
for sub in pageSoup.find_all(isSubCatagory):
    for classListing in sub.find_all(isClassListing):
        classEntry={}
        classListing=classListing.find_all('td')
        classEntry['coursePrefix']=classListing[0].get_text().split(' ')[0]
        classEntry['courseNum']=classListing[0].get_text().split(' ')[1]
        classEntry['title']=classListing[1].get_text()

        classList=classList.append(classEntry, ignore_index=True)

classList.to_csv(classListFile, index=False)
