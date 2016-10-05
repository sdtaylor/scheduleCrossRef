#Make a list of every graduate class ever offered and the
#terms which it was offered in

import pandas as pd
import json
from config import *

allClasses=pd.DataFrame(columns=['coursePrefix','courseNum','title','semesters'])

for thisSemester in terms:
    thisSemesterData=pd.read_csv(thisSemester['termSchedule'])
    thisSemesterData=thisSemesterData[['coursePrefix','courseNum','title']]
    
    thisSemesterData=thisSemesterData.drop_duplicates(subset=['coursePrefix','courseNum','title'])

    #Remove trailing letters from course numbers to filter out undergraduate classes
    thisSemesterData['courseNumStrict']=thisSemesterData['courseNum'].str.replace(r'[a-zA-Z]','').astype('int')
    thisSemesterData=thisSemesterData[thisSemesterData.courseNumStrict>=5000]
    thisSemesterData.drop('courseNumStrict', axis=1, inplace=True)

    thisSemesterData['semesters']=thisSemester['prettyName']

    allClasses=allClasses.append(thisSemesterData)

#Combine entries for each class into a single line
def combineSemesters(classes):
    semestersSingleString=', '.join(classes.tolist())
    return(semestersSingleString)
allClasses=allClasses.groupby(['coursePrefix','courseNum','title']).agg(combineSemesters).reset_index()

#Convert to dict for writing out as json objet
allClasses=allClasses.to_dict('records')

allClasses={'data' : allClasses}
objectFile='classSearchDB.txt'
with open(objectFile, 'w') as f:
    json.dump(allClasses, f, indent=4)

