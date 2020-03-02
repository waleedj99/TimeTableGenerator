from flask import Flask, request, render_template, jsonify

import json
import random
import itertools
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        pass
@app.route('/g', methods=['GET', 'POST'])
def get():
    if request.method == 'GET':
        from timetable import GeneticAlgorithm
        ga = GeneticAlgorithm(5, 8)
        fittest = ga.run_algorithm(['Mon', 'Tues', 'Wed', 'Thurs', 'Fri'], ['9-10', '10-11', '11-12', '12-13', '13-14', '14-15', '15-16', '16-17'], ['A', 'B', 'C'], ['math',
                                                                                                                                                              'science', 'social', 'history', 'english', 'hindi', 'computers'], ['400', '401', '402', '404', '405'], ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10'])
        class_dic  = {}

        for clname in fittest.std_grp_list:
            #class_dic[clname] = day_dic
            class_dic[clname] = {}
            for day in fittest.day_list:
                #day_dic[day] = period_dic
                class_dic[clname][day] ={}
                for pnum in fittest.class_timings_list:
                    class_dic[clname][day][pnum]={}
                    #period_dic[pnum] = {}

        for index1,day in enumerate(fittest.timetable): 
            for index2,period in enumerate(day):
                for index3,cl in enumerate(period):
                    subject,clname,teacher,room = str(fittest.timetable[index1][index2][index3]).split(' ')[0:4]
                    class_dic[clname][fittest.day_list[index1]][fittest.class_timings_list[index2]] = {'subject':subject,'teacher':teacher,'room':room}
        return(class_dic)
if __name__ == '__main__':
    app.run(debug=True)
