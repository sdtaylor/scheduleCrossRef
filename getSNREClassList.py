import urllib.request as urllib
from bs4 import BeautifulSoup as bs
import unicodedata
import pandas as pd
import os

baseURL='http://snre.ifas.ufl.edu/academics/graduate/courses-syllabi-and-curriculum/'
classListFile='majorClassLists/SNREList.csv'

html_titles = ['Principles of Ecology Courses','Particular Perspectives and Systems Ecology Courses',
               'Natural Science Courses','Social Sciences Courses',
               'Sustainability Studies Courses','Research and Design Methods Courses']
short_names = ['Principles of Ecology', 'Particular Systems', 'Natural Science',
               'Social Science', 'Sustainability', 'Research & Design']

catagories = pd.DataFrame({'html_title':html_titles,'subCatagory':short_names})


#Only run if this datafile doesn't exist
if os.path.exists(classListFile):
    print('SNRE List exists. Delete it if you want to remake it: ', classListFile)
    exit()

pageSoup=bs(urllib.urlopen(baseURL), 'lxml')


# deal with unicode
def convert_u(t):
    return unicodedata.normalize('NFKD', t)

################################################
# functions defining different html sections for
# use with beautifulsoup


# Class rows are 'tr' elements with exactly 4 'td' elements
def is_class_listing(tag):
    if tag.name=='tr':
        return len(tag.find_all('td')) == 4
    else:
        return False

######################################################
# Primary scraping code
class_list = []

for catagory_section in pageSoup.find_all('table'):
    html_title = convert_u(catagory_section.find('h3').text)
    subCatagory = catagories['subCatagory'][catagories.html_title==html_title].tolist()[0]
    
    for class_listing in catagory_section.find_all(is_class_listing):
        prefix_and_number = convert_u(class_listing.find_all('td')[0].text)
        title = convert_u(class_listing.find_all('td')[1].text).strip()
        
        prefix = prefix_and_number.split(' ')[0].strip()
        number = prefix_and_number.split(' ')[1].strip()
        
        class_list.append({'coursePrefix':prefix,
                           'courseNum':number,
                           'title':title,
                           'subCategory':subCatagory})

class_list = pd.DataFrame(class_list)

############################
#Some class have multiple sub catagories. Go thru and make one row per class
#with multiple subCatagoeries.

#There are duplicate rows where the only difference is the subcategory. First find
#all unique rows.
class_list_temp=class_list[['coursePrefix','courseNum','title']].drop_duplicates()
#Initialize a subCategory for the unique rows
class_list_temp['subCategory']=''
#Go thru row by row and pull the subCategories out, combining them where there are multiple
for index, row in class_list_temp.iterrows():
    #pull out the subcategories in a list
    subCats=class_list['subCategory'][class_list['title']==row['title']].drop_duplicates().tolist()
    #Clear any nan values that sneak in
    subCats=[x for x in subCats if str(x) != 'nan']
    #Combine them in a string and put them in the temp dataframe
    row['subCategory']=','.join(subCats)
    
class_list = class_list_temp

class_list.to_csv(classListFile, index=False)
