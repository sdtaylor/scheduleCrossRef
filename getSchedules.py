import pandas as pd
import os.path
import config
from pyUFAPI import UFScheduleAPIClient

#if you add or subtract columns then you need to adjust the getClassList function accordingly
#xxxx2 are for when there is a 2nd row with more schedule info. For labs, meeting times in different buildings, etc.
columns=['coursePrefix','courseNum','fee','section','credits','prof','title',
         'days','times','building','room',
         'days2','times2','building2','room2']

class_api = UFScheduleAPIClient()


def get_meeting_info(api_meet_times, meet_number):
    info = {'days':None,
            'times':None,
            'building':None,
            'room':None}
    
    if len(api_meet_times)>0:
        matching_info = [t for t in api_meet_times if t['meetNo'] == meet_number]
        if len(matching_info)>0:
            
            # Save just the period number if it's a single period, or the range if it's multiple.
            if matching_info[0]['meetPeriodBegin'] == matching_info[0]['meetPeriodEnd']:
                times = matching_info[0]['meetPeriodBegin']
            else:
                times = '{p1}-{p2}'.format(p1 = matching_info[0]['meetPeriodBegin'], p2=matching_info[0]['meetPeriodEnd'])
                
            info['days'] = ','.join(matching_info[0]['meetDays'])
            info['times'] = times
            info['building'] = matching_info[0]['meetBuilding']
            info['room'] = matching_info[0]['meetRoom']

    return info

def format_profs(api_instructor_list):
    return ','.join([entry['name'] for entry in api_instructor_list])

for this_semester in config.terms:
    data_file = this_semester['termSchedule']
    if os.path.exists(data_file):
        print('Semester data file exists, skipping: ',data_file)
        continue
    
    class_api = UFScheduleAPIClient(default_term = this_semester['name'],
                                    default_category = 'RES')
    
    semester_course_list=pd.DataFrame(columns=columns)
    
    for major in config.majors:
        major_class_list = pd.read_csv(major['classFile'])
        
        
        for course in major_class_list.to_dict('records'):
            full_course_code = course['coursePrefix'] + course['courseNum']
            course_api_output = class_api.get_course_info(course = full_course_code)
            
            print(full_course_code, course_api_output['course_found'])
            
            if course_api_output['course_found']:
                for unique_course in course_api_output['course_info']:
                    for api_section_info in unique_course['sections']:
                        
                        course_info = {}
                        
                        course_info['coursePrefix'] = course['coursePrefix']
                        course_info['courseNum']    = course['courseNum']
                        course_info['fee']          = api_section_info['courseFee']
                        course_info['section']      = api_section_info['classNumber']
                        course_info['credits']      = api_section_info['credits']
                        course_info['title']      = unique_course['name']
                        course_info['prof']      = format_profs(api_section_info['instructors'])
                        
                        section_time_info1 = get_meeting_info(api_section_info['meetTimes'], 1)
                        section_time_info2 = get_meeting_info(api_section_info['meetTimes'], 2)

                        course_info['days'] = section_time_info1['days']
                        course_info['times'] = section_time_info1['times']
                        course_info['building'] = section_time_info1['building']
                        course_info['room'] = section_time_info1['room']
                        course_info['days2'] = section_time_info2['days']
                        course_info['times2'] = section_time_info2['times']
                        course_info['building2'] = section_time_info2['building']
                        course_info['room2'] = section_time_info2['room']
                
                        semester_course_list = semester_course_list.append(course_info, ignore_index=True)

    # no need to list things twice. This is especially prevalent for special topic classes
    semester_course_list = semester_course_list.drop_duplicates()
    
    #write semester data frame
    semester_course_list.to_csv(data_file, index=False)