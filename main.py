from flask import Flask, request, render_template, jsonify
from timetable import Data, Driver, Instructor, Class, Course, StudentGroup, Room
import json

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        received_data = json.loads(request.data)
        working_days = {}
        working_days_ = received_data['working_data']  # dictionary, day-bool
        total_days = {'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'}
        for d in working_days_:
            if d in total_days:
                working_days[d] = True
            else:
                working_days[d] = False
        print(working_days)
        start_time = received_data['start_time']
        duration = received_data['duration']
        ppd = received_data['periods_per_day']
        rooms = int(received_data['rooms'])
        course_instructors = received_data['course_instructors']
        print(received_data['course_instructors'])
        rooms = ["Room" + str(i) for i in range(rooms)]
        courses = course_instructors.keys()
        student_groups = received_data.get('student_groups')
        classes_ = []
        courses_ = []
        student_groups_ = []
        rooms_ = []
        instructors_ = []
        if "" in course_instructors:
            del course_instructors[""]
        for r, stg in zip(rooms, student_groups):
            for c in courses:
                ins = course_instructors[c]
                for i in ins:
                    room_ = Room(r)
                    rooms_.append(room_)
                    stg_ = StudentGroup(stg)
                    student_groups_.append(stg_)
                    course_ = Course(c, "")
                    courses_.append(course_)
                    inst_ = Instructor(i)
                    instructors_.append(inst_)
                    class_ = Class(course=course_, type='Lec', instructor=inst_, student_group=stg_, allowed_room=room_)
                    classes_.append(class_)

                    print('Class:', str(class_))

        Data.courses = courses_
        Data.set_working_days(working_days)
        Data.rooms = rooms_
        Data.instructors = instructors_
        Data.student_groups = student_groups_
        Data.set_classes(classes_)
        Data.periods_per_day = ppd
        Data.set_periods(start_time, duration)
        res = []
        try:
            driver = Driver()
            ans = driver.generate_timetable()
            res = driver.generate_timetable_response(ans)
            res = [{'error': False, 'periods_per_day': ppd, 'days_per_week': len(received_data['working_data'])}] + res
        except Exception:
            res = [{'error': True}]

        finally:
            return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True)
