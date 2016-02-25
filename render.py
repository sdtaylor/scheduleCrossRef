import mako.template
import pandas as pd
import json
from config import *
from findHistory import *
import re

#Get current term info
for thisTerm in terms:
    if thisTerm['name']==currentTermName:
        break

thisTermSchedule=pd.read_csv(thisTerm['termSchedule'])
thisTermSchedule['coursePrefixNum']=thisTermSchedule['coursePrefix'] + thisTermSchedule['courseNum'].astype(str)

#Load template file for majors
template=mako.template.Template(filename=majorTemplate)

#render the major pages one at a time.
for thisMajor in majors:
    #Get list of this majors classes. Drop any duplicates that show up for whatever reason
    classList=pd.read_csv(thisMajor['classFile']) 
    classList=classList[['coursePrefix','courseNum','title','subCategory']]
    classList.drop_duplicates(inplace=True)

    #Concatonate the prefix and number into one value
    classList['coursePrefixNum']=classList['coursePrefix'] + classList['courseNum'].astype(str)

    #classes happening this term that = one of the courses in the course list
    crossRef=thisTermSchedule[thisTermSchedule['coursePrefixNum'].isin(classList['coursePrefixNum'])]

    #Initialize specialTopics and subCategory.
    crossRef['specialTopic']='No'
    crossRef['subCategory']=''


    #Set special topics flag. Also use this loop to set subCategories for non-special topics
    for index, row in crossRef.iterrows():
        if row['coursePrefixNum'] in specialTopicClasses:
            row['specialTopic']='Yes'
        else:
            subCats=classList[classList['coursePrefixNum']==row['coursePrefixNum']]['subCategory'].tolist()
            subCats=','.join(subCats)
            row['subCategory']=subCats
    
    #Drop any special topics that are not in relevant departments (defined in config file)
    #Keep any records with (specialTopics=No) OR (specialTopic=Yes AND couserPrefix=relevant)
    crossRef=crossRef[ (crossRef['specialTopic']=='No') |
                       ( (crossRef['specialTopic']=='Yes') & (crossRef['coursePrefix'].isin(relevantDepts)) )]

    print(crossRef.shape)
    #Get history of when all the classes have been offered
    history=[]
    for thisClass in crossRef['title'].values.tolist():
        history.append(getPriorTerms(thisClass))
    history=pd.DataFrame(history, index=crossRef.index)

    #Add the history to the rest of the info, and convert it to a dict for passing to web object
    crossRef=crossRef.join(history)

    #Convert to dictionary for dumping out as json object
    crossRef=crossRef.to_dict('records')

    #this majors html page name
    page='www/'+thisMajor['name']+'.html'

    #Write it out!
    with open(page, 'w') as f:
        f.write(template.render(classes=crossRef, thisMajor=thisMajor))


    crossRef={'data' : crossRef}
    objectFile='www/'+thisMajor['name']+'objects.txt'
    with open(objectFile, 'w') as f:
        json.dump(crossRef, f, indent=4)
    
#render the index page
template=mako.template.Template(filename='in/index.html.mako')
with open('www/index.html', 'w') as f:
    f.write(template.render(majors=majors))
