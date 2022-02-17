"""
schedule maintains a list of courses with features for operating on that list
by filtering, mapping, printing, etc.
"""

import json


class Schedule:
    """
    Schedule represent a list of Brandeis classes with operations for filtering
    """

    def __init__(self, courses=()):
        """ courses is a tuple of the courses being offered """
        self.courses = tuple(courses)

    def load_courses(self):
        """ load_courses reads the course data from the courses.json file"""
        print('getting archived regdata from file')
        with open("courses20-21.json", "r", encoding='utf-8') as jsonfile:
            courses = json.load(jsonfile)
        for course in courses:
            course['instructor'] = tuple(course['instructor'])
            course['coinstructors'] = [tuple(f) for f in course['coinstructors']]
        self.courses = tuple(courses)  # making it a tuple means it is immutable

    def lastname(self, names):
        """ lastname returns the courses by a particular instructor last name"""
        return Schedule([course for course in self.courses if course['instructor'][1] in names])

    def email(self, emails):
        """ email returns the courses by a particular instructor email"""
        return Schedule([course for course in self.courses if course['instructor'][2] in emails])

    def term(self, terms):
        """ email returns the courses in a list of term"""
        return Schedule([course for course in self.courses if course['term'] in terms])

    def enrolled(self, vals):
        """ enrolled filters for enrollment numbers in the list of vals"""
        return Schedule([course for course in self.courses if course['enrolled'] in vals])

    def subject(self, subjects):
        """ subject filters the courses by subject """
        return Schedule([course for course in self.courses if course['subject'] in subjects])

    def sort(self, field):
        """ sort results according to subject """
        if field == 'subject':
            return Schedule(sorted(self.courses, key=lambda course: course['subject']))
        print("can't sort by " + str(field) + " yet")
        return self

    def title(self, phrase):
        """ title filters the course by title """
        return Schedule([course for course in self.courses if phrase in course['name']])

    def description(self, phrase):
        """ description filters the course by description """
        return Schedule([course for course in self.courses if phrase in course['description']])

    def code(self, phrase):
        """ code filters the course by course code"""
        return Schedule([course for course in self.courses \
                         if phrase in ' '.join(course['code'])])

    def limit(self, limits):
        """ limit filters the course by capacity """
        return Schedule([course for course in self.courses \
                         if course['limit'] is not None and course['limit'] <= limits])

    def days(self, phrase):
        """ days filters thte course by days of week """
        course_list = []
        for course in self.courses:
            for time in course['time']:
                # Assume that users will provide days separated with ',', so as to be sonsistent
                # with the original data and compatible with sourse_search, 'tu' for Tuesday,
                # 'th' for Thursday, so detecting single character is bad
                for char in phrase.split(','):
                    if char in time['days']:
                        course_list.append(course)
                        break

        return Schedule(course_list)
