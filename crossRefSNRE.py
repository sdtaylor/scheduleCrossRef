#SNRE has a long list of specific classes that are part of the curriculum
#this does a simple merge with the current semester class list to see what
#SNRE classes are available this semester
import pandas as pd

snreClasses=pd.read_csv('SNREList.csv')
currentSchedule=pd.read_csv('semesterData/201601.csv')

#Just compare on unique codes. This will cause *all* special topics classes
#to be included in the list. But whatever, most of them are SNRE worthy anyway.
snreClasses.drop('title', axis=1, inplace=True)
snreClasses.drop_duplicates(inplace=True)
snreInCurrent=pd.merge(snreClasses, currentSchedule, on=['coursePrefix','courseNum'], how='inner')

snreInCurrent.to_csv('foo.csv', index=False)
