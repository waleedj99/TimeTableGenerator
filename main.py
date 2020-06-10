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


@app.route('/g', methods=['GET', 'POST'])
def get():
    if request.method == 'POST':
        main_json = request.get_json()

        ga = GeneticAlgorithm(main_json['no_days'], main_json['no_classes'])
        fittest = ga.run_algorithm(main_json['days_list'], main_json['time_list'], main_json['subject_list'],
                                   main_json['rooms'], main_json['teacher_list'], main_json['student_groups'])
        print(fittest)
        main_dic = OrderedDict()
        class_dic = OrderedDict()
        for clname in fittest.std_grp_list:
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

        for index1, day in enumerate(fittest.timetable):
            for index2, period in enumerate(day):
                for cl in period:
                    subject, clname, teacher, room = str(cl).split(' ')[0:4]
                    class_dic[clname][fittest.day_list[index1]][fittest.class_timings_list[index2]] = {
                        'subject': subject, 'teacher': teacher, 'room': room}
        main_dic["time_table"] = class_dic
        main_dic["days"] = fittest.day_list
        main_dic["times"] = fittest.class_timings_list
        print(main_dic)
        return json.dumps(main_dic)


if __name__ == '__main__':
    app.run(debug=True)
