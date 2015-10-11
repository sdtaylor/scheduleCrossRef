currentTermName='201601'

majorTemplate='in/majorPage.html.mako'

majors=[
     {'name': 'SNRE', 'classFile': 'majorClassLists/SNREList.csv', 'asof': 'Oct 10,2015'},
     {'name': 'WEC', 'classFile': 'majorClassLists/WECList.csv', 'asof': 'Oct 10,2015'}
]

terms=[
     {'name' :'201601', 'prettyName':'Spring 2016', 'termSchedule': 'semesterData/201601.csv'}, 
     {'name' :'201508', 'prettyName':'Fall 2015', 'termSchedule': 'semesterData/201508.csv'}, 
     {'name' :'201501', 'prettyName':'Spring 2015', 'termSchedule': 'semesterData/201501.csv'}, 
     {'name' :'201408', 'prettyName':'Fall 2014', 'termSchedule': 'semesterData/201408.csv'}, 
     {'name' :'201401', 'prettyName':'Spring 2014', 'termSchedule': 'semesterData/201401.csv'}, 
     {'name' :'201308', 'prettyName':'Fall 2013', 'termSchedule': 'semesterData/201308.csv'}, 
     {'name' :'201301', 'prettyName':'Spring 2013', 'termSchedule': 'semesterData/201301.csv'}, 
     {'name' :'201208', 'prettyName':'Fall 2012', 'termSchedule': 'semesterData/201208.csv'}, 
     {'name' :'201201', 'prettyName':'Spring 2012', 'termSchedule': 'semesterData/201201.csv'}, 
     {'name' :'201108', 'prettyName':'Fall 2011', 'termSchedule': 'semesterData/201108.csv'}, 
     {'name' :'201101', 'prettyName':'Spring 2011', 'termSchedule': 'semesterData/201101.csv'}, 
     {'name' :'201008', 'prettyName':'Fall 2010', 'termSchedule': 'semesterData/201008.csv'} 
]

#Every dept has 'Special Topic' codes that we may need to petition to take.
#Theres probably a better way to do this. maybe scrap the grad catalog website
specialTopicClasses=['ZOO6927',
                     'WIS6934',
                     'SWS6932',
                     'ALS5932',
                     'AOM6932',
                     'AEC6932',
                     'STA6934',
                     'ANS6932',
                     'ENY6932',
                     'NEM6932',
                     'AEB6933',
                     'PHC6937',
                     'LAS6938',
                     'GEO6938',
                     'HOS6932',
                     'MCB6937',
                     'PBC6937',
                     'FAS6932',
                     'AGR6932',
                     'BOT6935',
                     'ANG6930',
                     'ENV6935',
                     'FOR6934',
                     'MAT6932'
                     ]
