from flask import Flask, request, render_template, jsonify
from timetable import Data, Driver, Instructor, Class, Course, StudentGroup, Room
import json
import random
import itertools
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        # received_data = json.loads(request.data)
        # working_days = {}
        # working_days_ = received_data['working_data']  # dictionary, day-bool
        # total_days = {'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'}
        # for d in working_days_:
        #     if d in total_days:
        #         working_days[d] = True
        #     else:
        #         working_days[d] = False
        # print(working_days)
        # start_time = received_data['start_time']
        # duration = received_data['duration']
        # ppd = 4
        # rooms = int(received_data['rooms'])
        # course_instructors = received_data['course_instructors']
        # print(received_data['course_instructors'])
        # rooms = ["Room" + str(i) for i in range(rooms)]
        # courses = course_instructors.keys()
        # student_groups = received_data.get('student_groups')
        # classes_ = []
        # courses_ = []
        # student_groups_ = []
        # rooms_ = []
        # instructors_ = []
        # if "" in course_instructors:
        #     del course_instructors[""]
        #
        # for n in range(3):
        #     for c in courses:
        #         ins = course_instructors[c]
        #         for stg, r in zip(student_groups, rooms):
        #             i = random.choice(ins)
        #             room_ = Room(r)
        #             rooms_.append(room_)
        #             stg_ = StudentGroup(stg)
        #             student_groups_.append(stg_)
        #             course_ = Course(c, "")
        #             courses_.append(course_)
        #             inst_ = Instructor(i)
        #             instructors_.append(inst_)
        #             class_ = Class(course=course_, type='Lec', instructor=inst_, student_group=stg_, allowed_room=room_)
        #             classes_.append(class_)
        #
        #             print('Class:', str(class_))
        #
        # Data.courses = courses_
        # Data.set_working_days(working_days)
        # Data.rooms = rooms_
        # Data.instructors = instructors_
        # Data.student_groups = student_groups_
        # Data.set_classes(classes_)
        # Data.periods_per_day = ppd
        # Data.set_periods(start_time, duration)

        course0 = Course("MATH", "101")
        course1 = Course("CHEM", "103")
        course2 = Course("PIC", "104")
        course3 = Course("CAED", "105")
        course4 = Course("ELN", "106")
        course5 = Course("BCP", "107")

        ins0 = Instructor("Padma")
        ins1 = Instructor("Shiva")
        ins2 = Instructor("Harish")
        ins3 = Instructor("Shiv")
        ins4 = Instructor("Shobha")
        ins5 = Instructor("Rahul")
        ins6 = Instructor("Meena")

        ins7 = Instructor("Soumya")
        ins8 = Instructor("Uma")
        ins9 = Instructor("Deepak")
        ins10 = Instructor("Dhruva")

        room0 = Room("308")
        room1 = Room("309")

        stg0 = StudentGroup("1A")
        stg1 = StudentGroup("1B")

        c0 = Class(course=course0, type="Lec", instructor=ins0, student_group=stg0, allowed_room=room0)
        c1 = Class(course=course0, type="Lec", instructor=ins0, student_group=stg0, allowed_room=room0)
        c2 = Class(course=course0, type="Lec", instructor=ins0, student_group=stg0, allowed_room=room0)
        c3 = Class(course=course1, type="Lec", instructor=ins1, student_group=stg0, allowed_room=room0)
        c4 = Class(course=course1, type="Lec", instructor=ins1, student_group=stg0, allowed_room=room0)
        c5 = Class(course=course1, type="Lec", instructor=ins1, student_group=stg0, allowed_room=room0)
        c6 = Class(course=course2, type="Lec", instructor=ins2, student_group=stg0, allowed_room=room0)
        c7 = Class(course=course2, type="Lec", instructor=ins2, student_group=stg0, allowed_room=room0)
        c8 = Class(course=course2, type="Lec", instructor=ins2, student_group=stg0, allowed_room=room0)
        c9 = Class(course=course3, type="Lec", instructor=ins3, student_group=stg0, allowed_room=room0)
        c10 = Class(course=course3, type="Lec", instructor=ins3, student_group=stg0, allowed_room=room0)
        c11 = Class(course=course3, type="Lec", instructor=ins3, student_group=stg0, allowed_room=room0)
        c12 = Class(course=course4, type="Lec", instructor=ins4, student_group=stg0, allowed_room=room0)
        c14 = Class(course=course4, type="Lec", instructor=ins4, student_group=stg0, allowed_room=room0)
        c15 = Class(course=course5, type="Lec", instructor=ins6, student_group=stg0, allowed_room=room0)
        c16 = Class(course=course5, type="Lec", instructor=ins6, student_group=stg0, allowed_room=room0)

        c18 = Class(course=course0, type="Lec", instructor=ins0, student_group=stg1, allowed_room=room1)
        c19 = Class(course=course0, type="Lec", instructor=ins0, student_group=stg1, allowed_room=room1)
        c20 = Class(course=course0, type="Lec", instructor=ins0, student_group=stg1, allowed_room=room1)
        c21 = Class(course=course1, type="Lec", instructor=ins7, student_group=stg1, allowed_room=room1)
        c22 = Class(course=course1, type="Lec", instructor=ins7, student_group=stg1, allowed_room=room1)
        c23 = Class(course=course1, type="Lec", instructor=ins7, student_group=stg1, allowed_room=room1)
        c24 = Class(course=course2, type="Lec", instructor=ins8, student_group=stg1, allowed_room=room1)
        c25 = Class(course=course2, type="Lec", instructor=ins8, student_group=stg1, allowed_room=room1)
        c26 = Class(course=course2, type="Lec", instructor=ins8, student_group=stg1, allowed_room=room1)
        c27 = Class(course=course3, type="Lec", instructor=ins9, student_group=stg1, allowed_room=room1)
        c28 = Class(course=course3, type="Lec", instructor=ins9, student_group=stg1, allowed_room=room1)
        c29 = Class(course=course3, type="Lec", instructor=ins9, student_group=stg1, allowed_room=room1)
        c30 = Class(course=course4, type="Lec", instructor=ins10, student_group=stg1, allowed_room=room1)
        c32 = Class(course=course4, type="Lec", instructor=ins10, student_group=stg1, allowed_room=room1)
        c33 = Class(course=course5, type="Lec", instructor=ins6, student_group=stg1, allowed_room=room1)
        c34 = Class(course=course5, type="Lec", instructor=ins6, student_group=stg1, allowed_room=room1)

        Data.courses = [course0, course1]
        Data.set_working_days({'monday': True, 'tuesday': True, 'wednesday': True, 'thursday': True, 'friday': True,
                               'saturday': True})
        Data.rooms = [room0, room1]
        Data.instructors = [ins0, ins1, ins2, ins3, ins4, ins5, ins6, ins7, ins8, ins9, ins10]
        Data.student_groups = [stg0, stg1]
        Data.set_classes(
            [c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c12, c14, c15, c16, c18, c19, c20, c21, c22, c23,
             c24,
             c25, c26, c27, c28, c29, c30, c32, c33, c34])
        Data.periods_per_day = 4
        Data.set_periods("9:00", 1)

        driver = Driver()
        ans = driver.generate_timetable()
        res = driver.generate_timetable_response(ans)
        return jsonify((res))


if __name__ == '__main__':
    app.run(debug=True)
