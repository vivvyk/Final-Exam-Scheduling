import random

depts = ['ANTH', 'ARTS', 'BIO', 'CHEM', 'CMPT', 'ECON', 'FREN', 'HIST', 'LIT', 'MATH', 'MUS', 'NATS', 'PHIL', 'PSYC', 'SART', 'SPAN']

nums = ['100', '101', '103', '109', '110', '116', '157', '175', '200', '201', '202', '203', '205', '206', '207', '209', '210', '211', '214', '216', '218', '221', '222', '243', '261', '303', '306', '310', '311', '321', '321', '322', '331', '353', '364', '365']

exams = ['BIO100', 'BIO310', 'ECON101', 'FREN101', 'MATH321', 'PSYC100', 'PSYC206', 'CHEM303', 'CMPT200', 'LIT157', 'LIT321', 'PSYC209', 'SPAN101A', 'SPAN101B', 'ANTH214', 'BIO331', 'CMPT100', 'NATS116', 'PHYS101', 'CHEM306', 'CMPT243', 'PHIL175', 'PSYC203', 'SART218', 'ARTS211', 'ARTS311', 'CHEM101A', 'CHEM101B', 'CMPT353', 'FREN205', 'MATH365', 'PHIL222', 'PSYC322', 'BO200', 'CHIN101', 'MATH109', 'MATH221A', 'MATH221B', 'PHIL216', 'BIO201', 'MATH210', 'MUS207', 'CMPT364', 'HIST261', 'MATH110A', 'MATH110B', 'PHIL103', 'ANTH202', 'MATH211A', 'MATH211B', 'MATH364']

numstudents = 200

sectionletters = ['A', 'B', 'C', 'D', 'E']

fyle = open('randomData.txt', 'w')

for i in range(numstudents):
    c = 0
    numcourses = random.randint(3, 6)
    courses = ""
    for j in range(numcourses):
        if c % 3 == 0:
            course = random.randint(0, len(exams) - 1)
            courses += exams[course]
        else:
            coursename = random.randint(0, len(depts) - 1)
            coursenum = random.randint(0, len(nums) - 1)
            courses += depts[coursename] + nums[coursenum]
            multisection = random.randint(0, 9)
            if multisection >= 7:
                sections = multisection % 5
            else:
                sections = -1
            if sections >= 0:
                courses += sectionletters[sections]
        courses += ', '
        c += 1
    courses = courses[:-2] + '\n'
    fyle.write(courses)

fyle.close()
