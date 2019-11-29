"""
An interface to the UFL class schedule API.

api = UFScheduleAPIClient(default_term = 2201,
                          default_category = 'RES')

# Returns a dictionary of api query.
c = api.get_course_info(course = 'chm2040')

# list of info on each class section is in
c[0]['COURSES']

"""

import requests as r
import warnings

class UFScheduleAPIClient():
    def __init__(self, 
                 hostname='https://one.ufl.edu/apix/soc/schedule/',
                 default_term=None,
                 default_category=None):
        self.headers={}
        self.hostname = hostname
        self.default_term = default_term
        self.default_category = default_category
    
    def _make_request(self, http_method,params=None, data=None):
        request = http_method(self.hostname, 
                              headers = self.headers,
                              params = params,
                              data = data)
        if not request.ok:
            try:
                error = request.json()
            except:
                error = ''
            raise RuntimeError('request failed',
                               error)
        
        return request.json()
    
    def _get_default(self, default_value, input_value, param_name):
        """
        Use the inputed value if it's used, otherwise the default, and
        throw an error if neither are set.
        """
        if input_value is not None:
            return input_value
        else:
            if default_value is not None:
                return default_value
            else:
                raise ValueError(param_name + ' must be set')
    
    def _check_course_info(self, request_output, search_term):
        """
        Parse the output down to only the course info. Remove any extranous courses
        included (ie. CHM2047 will also return listings for CHM2047L).
        """
        request_output = request_output[0]
        checked_output = {'course_found'     : True,
                          'multiple_courses' : False,
                          'course_info'      : None}
        
        if request_output['TOTALROWS'] == 0:
            matching_courses = []
        else:
            matching_courses = [c for c in request_output['COURSES'] if c['code'].lower() == search_term.lower()]
            
            
        if len(matching_courses) == 0:
            checked_output['course_found'] = False
        elif len(matching_courses) > 1:
            checked_output['multiple_courses'] = True
            #warnings.warn('More than 1 course found for '+search_term)
            
        checked_output['course_info'] = matching_courses
        return checked_output
   
    def get_course_info(self, course, term=None, category=None):
        term = self._get_default(self.default_term, term, 'term')
        category = self._get_default(self.default_category, category, 'category')
        
        parameters = {'term':term,
                      'category':category,
                      'course-code':course}
        
        request_output =  self._make_request(r.get, params=parameters)
        request_output = self._check_course_info(request_output, course)
        return request_output
