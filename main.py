from flask import Flask, request, render_template, jsonify
from collections import OrderedDict 
import json
import random
import itertools
from flask import send_file , make_response
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)


def _build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.mimetype = "application/pdf"
    return response

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        pass

@app.route('/g', methods=['GET', 'POST'])
def get():
    if request.method == 'POST':
        
        from timetable import GeneticAlgorithm
        main_json = request.get_json()
        
        ga = GeneticAlgorithm(main_json['no_days'], main_json['no_classes'])
        fittest = ga.run_algorithm(main_json['days_list'], main_json['time_list'], main_json['section_list'], main_json['subject_list'], ['400', '401', '402', '404', '405'], ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10'])
        print(fittest)
        main_dic = OrderedDict()
        class_dic = OrderedDict()  
        for clname in fittest.std_grp_list:
            #print(clname)
            class_dic[clname] = OrderedDict()
            for day in fittest.day_list:
                #day_dic[day] = period_dic
                #print(day)
                class_dic[clname][day] = OrderedDict()
                for pnum in fittest.class_timings_list:
                    #print(pnum)
                    class_dic[clname][day][pnum]=OrderedDict()
                    #period_dic[pnum] = {}

        for index1,day in enumerate(fittest.timetable): 
            for index2,period in enumerate(day):
                for cl in period:
                    subject,clname,teacher,room = str(cl).split(' ')[0:4]
                    class_dic[clname][fittest.day_list[index1]][fittest.class_timings_list[index2]] = {'subject':subject,'teacher':teacher,'room':room}
        main_dic["time_table"] = class_dic
        main_dic["days"] = fittest.day_list
        main_dic["times"] = fittest.class_timings_list
        print(main_dic)
        return(json.dumps(main_dic))
if __name__ == '__main__':
    app.run(debug=True)
