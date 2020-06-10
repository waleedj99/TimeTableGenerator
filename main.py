from flask import Flask, request, render_template
from collections import OrderedDict
import json
from timetable import GeneticAlgorithm

app = Flask(__name__, static_folder='../TimeTableGen_FE/TimetableFE/time-table/build/static',
            template_folder='../TimeTableGen_FE/TimetableFE/time-table/build')


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        pass


@app.route('/generate', methods=['GET', 'POST'])
def get():
    if request.method == 'POST':
        main_json = request.get_json()

        ga = GeneticAlgorithm(main_json['no_days'], main_json['no_classes'])
        fittest = ga.run_algorithm(main_json['days_list'], main_json['time_list'], main_json['subject_list'],
                                   main_json['rooms'], main_json['teacher_list'], main_json['student_groups'])
        main_dic = OrderedDict()
        class_dic = OrderedDict()
        for clname in range(len(fittest.student_groups)):
            # print(clname)
            class_dic[clname] = OrderedDict()
            for day in fittest.day_list:
                # day_dic[day] = period_dic
                # print(day)
                class_dic[clname][day] = OrderedDict()
                for pnum in fittest.class_timings_list:
                    # print(pnum)
                    class_dic[clname][day][pnum] = OrderedDict()
                    # period_dic[pnum] = {}
        for k, sg in enumerate(fittest.student_groups):
            for i, day in enumerate(fittest.day_list):
                for j, cltime in enumerate(fittest.class_timings_list):
                    subject = fittest.timetable[i][j][k].subject.name
                    teacher = fittest.timetable[i][j][k].teacher.name
                    room = fittest.timetable[i][j][k].room.name
                    class_dic[k][day][cltime] = {
                        'subject': "" if subject == 'empty' else subject, 'teacher': teacher, 'room': room}
        main_dic["time_table"] = class_dic
        main_dic["days"] = fittest.day_list
        main_dic["times"] = fittest.class_timings_list
        print(main_dic)
        return json.dumps(main_dic)


if __name__ == '__main__':
    app.run(debug=True)
