from flask import Flask, request, render_template, jsonify
from timetable import Data, Driver, Instructor, Class, Course, StudentGroup, Room

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    else:

        working_days = request.form.get('working_data')  # dictionary, day-bool
        start_time = request.form.get('start_time')
        duration = request.form.get('duration')
        ppd = request.form.get('periods_per_day')
        rooms = request.form.get('rooms')
        courses = request.form.get('courses')
        instructors = request.form.get('instructors')
        student_groups = request.form.get('student_groups')
        classes_ = []
        courses_ = []
        instructors_ = [Instructor(fn) for fn in instructors]
        student_groups_ = [StudentGroup(nm) for nm in student_groups]
        rooms_ = [Room(nm) for nm in rooms]
        for c in courses:
            n_classes = c['n_classses']
            ins = Instructor(c['instructor_name'])
            std_group = StudentGroup(c['student_group'])
            course = Course(c['course_name'], c['course_code'])
            allowed_room = c['room']
            courses_.append(course)
            for i in range(n_classes):
                cl = Class(course=course, type='Lec', instructor=ins, student_group=std_group,
                           allowed_room=allowed_room)
                classes_.append(cl)

        Data.set_working_days(working_days)
        Data.periods_per_day = int(ppd)
        Data.set_periods(start_time, int(duration))
        Data.courses = courses_
        Data.rooms = rooms_
        Data.instructors = instructors_
        Data.set_classes(classes_)
        Data.student_groups = student_groups_

        driver = Driver()
        ans = driver.generate_timetable()
        res = driver.generate_timetable_response(ans)
        return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True)
