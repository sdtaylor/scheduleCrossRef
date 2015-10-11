import mako.template
import pandas as pd
import json
from config import *
from findHistory import *

#schedule=pd.read_csv('SNRE2016.csv')
#x=schedule.to_dict('records')



#Get current term info
for thisTerm in terms:
    if thisTerm['name']==currentTermName:
        break

thisTermSchedule=pd.read_csv(thisTerm['termSchedule'])

#Load template file for majors
template=mako.template.Template(filename=majorTemplate)

#render the major pages one at a time.
for thisMajor in majors:
    #Get list of this majors classes. Drop any duplicates that show up for whatever reason
    classList=pd.read_csv(thisMajor['classFile']) 
    classList=classList[['coursePrefix','courseNum']]
    classList.drop_duplicates(inplace=True)

    #Cross reference it with the main schedule for this term using an inner merge, where only 
    #entries that are in both lists are used. Then make it a dictionary to pass to the template engine.
    crossRef=pd.merge(classList, thisTermSchedule, on=['coursePrefix','courseNum'], how='inner').fillna('')

    #Get history of when all the classes have been offered
    history=[]
    for thisClass in crossRef['title'].values.tolist():
        history.append(getPriorTerms(thisClass))
    history=pd.DataFrame(history, index=crossRef.index)

    #Add the history to the rest of the info, and convert it to a dict for passing to web object
    crossRef=crossRef.join(history).to_dict('records')



    #major html page
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
