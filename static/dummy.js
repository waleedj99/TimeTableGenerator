var data = [
    {'day': 'Monday', 'period': '09:00-10:00', 'student_group': 'CS-A', 'room': '201', 'course': 'WEB' },
    {'day': 'Monday', 'period': '10:00-11:00', 'student_group': 'CS-A', 'room': '201', 'course': 'ML' }, 
    {'day': 'Monday', 'period': '11:00-12:00', 'student_group': 'CS-A', 'room': '201', 'course': 'CS' }, 
    {'day': 'Monday', 'period': '13:00-14:00', 'student_group': 'CS-A', 'room': '201', 'course': 'WEB'},
    { 'day': 'Monday', 'period': '14:00-15:00', 'student_group': 'CS-A', 'room': '201', 'course': 'CS' },
    { 'day': 'Monday', 'period': '15:00-16:00', 'student_group': 'CS-A', 'room': '201', 'course': 'MATH' },

    
    { 'day': 'Monday', 'period': '09:00-10:00', 'student_group': 'CS-B', 'room': '202', 'course': 'WEB'},
    { 'day': 'Monday', 'period': '10:00-11:00', 'student_group': 'CS-B', 'room': '202', 'course': 'ML' },
    { 'day': 'Monday', 'period': '11:00-12:00', 'student_group': 'CS-B', 'room': '202', 'course': 'CS' },
    { 'day': 'Monday', 'period': '13:00-14:00', 'student_group': 'CS-B', 'room': '202', 'course': 'WEB' },
    { 'day': 'Monday', 'period': '14:00-15:00', 'student_group': 'CS-B', 'room': '202', 'course': 'CS' },
    { 'day': 'Monday', 'period': '15:00-16:00', 'student_group': 'CS-B', 'room': '202', 'course': 'MATH' },

    { 'day': 'Tuesday', 'period': '09:00-10:00', 'student_group': 'CS-A', 'room': '201', 'course': 'WEB' },
    { 'day': 'Tuesday', 'period': '10:00-11:00', 'student_group': 'CS-A', 'room': '201', 'course': 'WEB' },
    { 'day': 'Tuesday', 'period': '11:00-12:00', 'student_group': 'CS-A', 'room': '201', 'course': 'WEB' },
    { 'day': 'Tuesday', 'period': '13:00-14:00', 'student_group': 'CS-A', 'room': '201', 'course': 'WEB' },
    { 'day': 'Tuesday', 'period': '14:00-15:00', 'student_group': 'CS-A', 'room': '201', 'course': 'CS' },
    { 'day': 'Tuesday', 'period': '15:00-16:00', 'student_group': 'CS-A', 'room': '201', 'course': 'CS' },

    
    { 'day': 'Tuesday', 'period': '09:00-10:00', 'student_group': 'CS-B', 'room': '202', 'course': 'WEB' },
    { 'day': 'Tuesday', 'period': '10:00-11:00', 'student_group': 'CS-B', 'room': '202', 'course': 'WEB' },
    { 'day': 'Tuesday', 'period': '11:00-12:00', 'student_group': 'CS-B', 'room': '202', 'course': 'WEB' },
    { 'day': 'Tuesday', 'period': '13:00-14:00', 'student_group': 'CS-B', 'room': '202', 'course': 'WEB' },
    { 'day': 'Tuesday', 'period': '14:00-15:00', 'student_group': 'CS-B', 'room': '202', 'course': 'CS' },
    { 'day': 'Tuesday', 'period': '15:00-16:00', 'student_group': 'CS-B', 'room': '202', 'course': 'CS' },
        ]
$(document).ready(function () {

    generateTable(data)    

})
function generateTable(data){

    var lookup = {};
    var items = data
    var result = [];

    for (var item, i = 0; item = items[i++];) {
        var name = item.student_group;

        if (!(name in lookup)) {
            if(name===undefined){
                continue
            }
            lookup[name] = 1;
            result.push(name);
        }
    }


    console.log(result)

    for (let i = 0; i < result.length; i++) {
        $('body').append(
            `<table align ="center" style="border:solid" id = "`+result[i]+`">
               <h3 align="center"> `+ result[i]+`
            </h3> </table>`
        )
    }
    var days_list = []
    lookup = {};
    for (var item, i = 0; item = items[i++];) {
        var name = item.day;

        if (!(name in lookup)) {
            if (name === undefined) {
                continue
            }
            lookup[name] = 1;
            days_list.push(name);
        }
    }


    result.forEach(className =>{
        days_list.forEach(day=>{
            $('#' + className).append(`<tr id = "day-` +day +'-'+className +`">
                <td>
                <b> `+ day + `</b>
                </td> 
             </tr>`) 
            
        })
        
    })
    data.forEach(dataItem => {
        $('#day-' + dataItem.day + '-' + dataItem.student_group).append(
            `<td id = "sub-` + dataItem.course + `"> 
                         `+ dataItem.course + `
                    </td>`
        )
    })
}
// for (let k = 1; k <= data[0].n_periods; k++) {
//     $('#day-' + data[j].day + i + j).append(
//         `<div class = "col-sm-3" id = "sub-"` + data[k].period + i + j + k + `">
//                 `+ data[k].period + `
//             </div>`
//     )


// }