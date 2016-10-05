import pandas as pd
from config import *

allClasses=pd.DataFrame(columns=['coursePrefix','courseNum','title','semesters'])

for thisSemester in terms[1:5]:
    thisSemesterData=pd.read_csv(thisSemester['termSchedule'])
    thisSemesterData=thisSemesterData[['coursePrefix','courseNum','title']]
    
    print(thisSemesterData.shape)
    thisSemesterData=thisSemesterData.drop_duplicates(subset=['coursePrefix','courseNum','title'])
    print(thisSemesterData.shape)

    #Remove trailing letters from course numbers to filter out undergraduate classes
    thisSemesterData['courseNumStrict']=thisSemesterData['courseNum'].str.replace(r'[a-zA-Z]','').astype('int')
    thisSemesterData=thisSemesterData[thisSemesterData.courseNumStrict>=5000]
    thisSemesterData.drop('courseNumStrict', axis=1, inplace=True)
    print(thisSemesterData.shape)
    thisSemesterData['semesters']=thisSemester['prettyName']

    allClasses=allClasses.append(thisSemesterData)

print(allClasses.shape)
print(allClasses)
