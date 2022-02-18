'''
course_search is a Python script using a terminal based menu to help
students search for courses they might want to take at Brandeis
'''

from schedule import Schedule

schedule = Schedule()
schedule.load_courses()
schedule = schedule.enrolled(range(5, 1000))  # eliminate courses with no students

TOP_LEVEL_MENU = '''
quit
reset
term  (filter by term)
course (filter by course code, e.g. COSI 103a)
instructor (filter by instructor)
subject (filter by subject, e.g. COSI, or LALS)
title  (filter by phrase in title)
description (filter by phrase in description)
dayofweek (filter by day of week, e.g. w,th,f)
limit (filter by class enrollment limit)
'''

terms = {c['term'] for c in schedule.courses}


def topmenu():
    """
    topmenu is the top level loop of the course search app
    """
    global schedule
    while True:
        command = input(">> (press h for help) ")
        if command == 'quit':
            return
        elif command in ['h', 'help']:
            print(TOP_LEVEL_MENU)
            print('-' * 40 + '\n\n')
            continue
        elif command in ['r', 'reset']:
            schedule.load_courses()
            schedule = schedule.enrolled(range(5, 1000))
            continue
        elif command in ['t', 'term']:
            term = input("enter a term:" + str(terms) + ":")
            schedule = schedule.term([term]).sort('subject')
        elif command in ['s', 'subject']:
            subject = input("enter a subject:")
            schedule = schedule.subject([subject])
        elif command in ['d', 'description']:
            phrase = input('enter a keyword in the description: ')
            schedule = schedule.description(phrase)
        elif command in ['tt', 'title']:
            phrase = input("enter a keyword in the title of the course: ")
            schedule = schedule.title(phrase)
        elif command in ['l', 'limit']:
            limit = int(input("enter in a desired class limit: "))
            print('The courses listed have an enrollment limit less than or equal to', limit)
            schedule = schedule.limit(limit)
        elif command in ['i', 'instructor']:
            instructor = input("enter the last name of the desired instructor: ")
            schedule = schedule.lastname(instructor)
        elif command in ['c', 'course']:
            code = input("enter course code (e.g. COSI 103A): ")
            schedule = schedule.code(code)
        elif command in ['de', 'details']:
            phrase = input("enter a keyword in the details of the course: ")
            schedule = schedule.details(phrase)
        elif command in ['days', 'daysofweek']:
            phrase = input("enter the day of the week for the course, separate by commas: ")
            tmp = phrase.split(",")
            out = "Select courses that are offered on "
            res = []
            for item in tmp:
                item = item.strip().lower()
                if item.startswith("m"):
                    res.append("m")
                    out += "Monday, "
                elif item.startswith("tu"):
                    res.append("tu")
                    out += "Tuesday, "
                elif item.startswith("w"):
                    res.append("w")
                    out += "Wednesday, "
                elif item.startswith("th"):
                    res.append("th")
                    out += "Thursday, "
                elif item.startswith("f"):
                    res.append("f")
                    out += "Friday, "
            idx = out.rfind(",")
            out = out[:idx] +":"
            print(out)
            schedule=schedule.days(",".join(res))

        else:
            print('command', command, 'is not supported')
            continue
        print("Courses has",len(schedule.courses),'elements',end="\n\n")
        if len(schedule.courses) >=10:
            print('Here are the first 10: ')
            for course in schedule.courses[:10]:
                print_course(course)
        else:
            print ("Here are the available courses: ")
            for course in schedule.courses:
                print_course(course)
        print('\n' * 3)


def print_course(course):
    """
    print_course prints a brief description of the course
    """
    print(course['subject'], course['coursenum'], course['section'],
          course['name'], course['term'], course['instructor'])


if __name__ == '__main__':
    INFO = """
    Navigate through Brandeis's offered courses! Filter through the many courses by:
    term, course, instructor, subject, description keywords, title keywords, 
    day of instruction, and enrollment limit.
    """
    print(INFO)
    topmenu()
