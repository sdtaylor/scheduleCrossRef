import mako.template
import pandas as pd
import json
from config import *
from findHistory import *
import re

#render a page for a specific major in a specific term
#major is a dict with major info from config file. term is a single str for term, ie '201601'
def renderMajorPage(major, termInfo):

    thisTermSchedule=pd.read_csv(termInfo['termSchedule'])
    thisTermSchedule['coursePrefixNum']=thisTermSchedule['coursePrefix'] + thisTermSchedule['courseNum'].astype(str)

    #Load template file for majors
    template=mako.template.Template(filename=majorTemplate)

    #Get list of this majors classes. Drop any duplicates that show up for whatever reason
    classList=pd.read_csv(major['classFile']) 
    classList=classList[['coursePrefix','courseNum','title','subCategory']]
    classList.drop_duplicates(inplace=True)

    #Concatonate the prefix and number into one value
    classList['coursePrefixNum']=classList['coursePrefix'] + classList['courseNum'].astype(str)

    #classes happening this term that = one of the courses in the course list
    #or are in relevent departments like biology, forestry, etc. 
    crossRef=thisTermSchedule[(thisTermSchedule['coursePrefixNum'].isin(classList['coursePrefixNum'])) | 
                              (thisTermSchedule['coursePrefix'].isin(relevantDepts))].copy()

    #Initialize specialTopics and subCategory.
    crossRef['specialTopic']='No'
    crossRef['subCategory']=''


    #Set special topics flag. Also use this loop to set subCategories for non-special topics
    for index, row in crossRef.iterrows():
        if row['coursePrefixNum'] in specialTopicClasses:
            crossRef.loc[index,'specialTopic']='Yes'
        else:
            subCats=classList[classList['coursePrefixNum']==row['coursePrefixNum']]['subCategory'].tolist()
            subCats=','.join(subCats)
            crossRef.loc[index,'subCategory']=subCats
    
    #Drop any special topics that are not in relevant departments (defined in config file)
    #Keep any records with (specialTopics=No) OR (specialTopic=Yes AND couserPrefix=relevant)
    crossRef=crossRef[ (crossRef['specialTopic']=='No') |
                       ( (crossRef['specialTopic']=='Yes') & (crossRef['coursePrefix'].isin(relevantDepts)) )]

    #Drop research credit classes that are offerend every semester
    crossRef=crossRef[~crossRef['title'].isin(classTitleExclusions)]

    #Get history of when all the classes have been offered
    history=[]
    for thisClass in crossRef['title'].values.tolist():
        history.append(getPriorTerms(thisClass))
    history=pd.DataFrame(history, index=crossRef.index)

    #Add the history to the rest of the info.
    crossRef=crossRef.join(history)

    #Replace na's with blanks or JSON parsing breaks
    crossRef.fillna('', inplace=True)

    #Convert to dictionary for dumping out as json object
    crossRef=crossRef.to_dict('records')

    #this majors html page name
    page='www/'+major['name']+'_'+termInfo['name']+'.html'

    #Write it out!
    with open(page, 'w') as f:
        f.write(template.render(classes=crossRef, thisMajor=major, termInfo=termInfo))


    crossRef={'data' : crossRef}
    objectFile='www/'+major['name']+'objects'+'_'+termInfo['name']+'.txt'
    with open(objectFile, 'w') as f:
        json.dump(crossRef, f, indent=4)
    

#Information to put into the index.html page. The location of every major/term page
pages=[]

#Render each term with each configure major
for thisMajor in majors:
    for thisTermName in termNames:
        #Get current term info. (like pretty name, semester list file, etc.)
        for thisTermInfo in terms:
            if thisTermInfo['name']==thisTermName:
                break

        #Render the html page and json object for this major/term
        renderMajorPage(thisMajor, thisTermInfo)   

        #Add the page info for inclusion to index.html
        pages.append({'majorName' : thisMajor['name'],
                      'termPrettyName' : thisTermInfo['prettyName'],
                      'link' : thisMajor['name']+'_'+thisTermInfo['name']+'.html'})


#render the index page
template=mako.template.Template(filename='in/index.html.mako')
with open('www/index.html', 'w') as f:
    f.write(template.render(pages=pages))
