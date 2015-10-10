import mako.template
import pandas as pd
from config import *

#schedule=pd.read_csv('SNRE2016.csv')
#x=schedule.to_dict('records')



#Get current term info
for thisTerm in terms:
    if thisTerm['name']==currentTermName:
        break

thisTermSchedule=pd.read_csv(thisTerm['termSchedule'])

#Load template file for majors
template=mako.template.Template(filename=majorTemplate)

for thisMajor in majors:
    #Get list of this majors classes. Drop any duplicates that show up for whatever reason
    classList=pd.read_csv(thisMajor['classFile']) 
    classList=classList[['coursePrefix','courseNum']]
    classList.drop_duplicates(inplace=True)

    #Cross reference it with the main schedule for this term using an inner merge, where only 
    #entries that are in both lists are used. Then make it a dictionary to pass to the template engine.
    crossRef=pd.merge(classList, thisTermSchedule, on=['coursePrefix','courseNum'], how='inner').to_dict('records')

    #major html page
    page='www/'+thisMajor['name']+'.html'

    #Write it out!
    with open(page, 'w') as f:
        f.write(template.render(classes=crossRef))
    
