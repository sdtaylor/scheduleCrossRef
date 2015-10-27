# scheduleCrossRef
Cross reference the UFL main schedule with department curriculum to get an easy list of available classes. 

I made this to help look for classes that actually match my major. The class lists are classes for this semester that are cross referenced to a curriculum list for a particular major.

###Main files
config.py - configuration detailing terms, majors, etc. 

getSchedules.py - downloads full UF schedules that are configured in config.py

getSNREClassList.py - downloads the SNRE curriculum

render.py - compiles everything into static html pages in the www folder. 


###Instructions for rendering
1. Run getSchedules.py. This downloads all the primary UF schedules
2. Run getSNREClassList.py. This downloads the SNRE curriculum.
3. In config.py set the currentTerm to the current semester.
3. Run render.py. This creates all the html content in the www folder. These are static pages and only things in www need to be hosted somewhere to display the schedule. 

###Adding a semester
1. In config.py add an entry to the terms{} dictionary according to the instructions. 
2. Re-run the getSchedules.py and render.py scripts.

###Updating a semester
1. If the schedule gets updated, delete that terms csv in the semesterData folder. Re-run getSchedules.py and render.py

###Adding a major
1. Add an entry in config.py in the majors{} dictionary according to the instructions. 
2. Compile a csv of the majors class curriculum. There are several ways to do this. For example the SNRE class list is pulled automatically from the SNRE website via a script. The WEC list was copied and pasted from a PDF. 
3. The csv file should have 2 columns. 'coursePrefix' and 'courseNum'. For example: 

coursePrefix,courseNum

AGR,6311

BOT,5685C

BOT,5695

.....

4. With the new csv class list in place and the config.py updated. Run render.py to generate the site with the new major added. RE-run getSchedules.py if needed. 
