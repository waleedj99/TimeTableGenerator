


var instructors_list_global = []

$(document).ready(function(){

var course_instructor_mapping = Object()
let course_list=[]
let instructors_list = []
let new_days = []
let start_time
let url = "/"
let periods_per_day
let student_groups = []
    


    console.log('Loaded')
    $(function () {
        $('#datetimepicker1').datetimepicker(
            {
                format: 'HH:mm'
            }
        );
    });

    let year_list = []
    let section_list = []
    
    $('#submit_btn').click(function(e){
        e.preventDefault();
        console.log('Ajax POST')

        let courses = $('.course-list')
        courses.each(function(i, obj){
                course_list.push($(this).val())
        })

        let instructors = $('.instructors-list')
        instructors_list = []
        instructors.each(function(i, obj){
                instructors_list.push($(this).val())
        })

        periods_per_day = $('[name="n_periods"]').val()

        let nrooms = $('#n_rooms').val()
        start_time = $('#datetimepicker1').find('input').val()
        let duration = $('#duration').val()
        function check_day(d){

            if ($("#"+d.substring(0, 3)+"-check").prop('checked'))return true;
            return false;
        }
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        
        days.forEach(function(it){
            if(check_day(it)){
                new_days.push(it)
            }
        })

    let years = $('.year-list')
        years.each(function (i, obj) {
            year_list.push($(this).val())
        })
        let section = $('.section-list')
        section.each(function(i,obj){
             section_list.push($(this).val())
             console.log(section_list)
        })
        
        for(var i =0;i<year_list.length;i++){
            
            student_groups.push(year_list[i]+ '-' + section_list[i])
            
        }
        console.log("Student Group" + student_groups)
        console.log(duration)
        console.log(new_days)
        console.log(instructors_list)
        console.log(course_list)
        console.log(start_time)
        let v1 = $('[name="instructor-course"]')
        v1.each(function(i, obj){
            let v2 = $(this).find("[name='course']").val()
            let v3 = $(this).find("[name='instructors']").val().split(',')
            console.log('Course:'+v2+" ins="+v3)
            course_instructor_mapping[v2] = v3
        })
        console.log(course_instructor_mapping)
        $(this).text('Loading')
        $.ajax({
            type: "POST",
            url: '/',
            data: JSON.stringify({
                start_time: '9:00',
                duration: 1,
                working_data: ["monday", "tuesday"],
                periods_per_day: 6,
                course_instructors: course_instructor_mapping,
                courses: course_list,
                student_groups: student_groups,
                rooms: nrooms
            }),

            contentType: 'application/json;charset=UTF-8',
        }).done(function(res){
            console.log(res)
            $(this).text("Submit")
            console.log(res)
            generateTable(res)
        });

    })

})

function generateTable(data) {

    var lookup = {};
    var items = data
    var result = [];

    for (var item, i = 0; item = items[i++];) {
        var name = item.student_group;

        if (!(name in lookup)) {
            if (name === undefined) {
                continue
            }
            lookup[name] = 1;
            result.push(name);
        }
    }


    console.log(result)

    for (let i = 0; i < result.length; i++) {
        $('body').append(
            `<table align ="center" style="border:solid" id = "` + result[i] + `">
               <h3 align="center"> `+ result[i] + `
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


    result.forEach(className => {
        days_list.forEach(day => {
            $('#' + className).append(`<tr id = "day-` + day + '-' + className + `">
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
   function addCourse(divName,addBtn){
    var formLength = document.getElementById(divName + '-main').childElementCount
    console.log(addBtn.id)

    items = []
    instructors_list_global.forEach(function(item){
        let i = `<option value=`+item+`">`+item+`</option>`
        items.push(i)
    })


    if (addBtn.className.includes("glyphicon-minus")) {
        addBtn.parentNode.parentNode.parentNode.parentNode.removeChild(addBtn.parentNode.parentNode.parentNode)
    }
    if (addBtn.className.includes("glyphicon-plus")) {
        addBtn.className = "input-group-append  glyphicon glyphicon-minus"
        var newDiv = document.createElement('div')
        newDiv.className = 'form-group'
        newDiv.id = "courses-"+ formLength + ""
        newDiv.innerHTML = ` <div class="col-lg-12 ">
                            <div class="input-group form-group" name="instructor-course">
                            <input type="text"  placeholder="Enter Course"  class="course-list input-group-addon form-control" id="courses-in-`+ formLength +`" name="course">
                            <input placeholder="Enter Instructors for the Course" type="text" class="course-list input-group-addon form-control" name="instructors">
                                <span onclick="addCourse('courses',this.children[0].children[0])" class="input-group-addon">
                                    <span>
                                        <span   class="input-group-append glyphicon glyphicon-plus" id=`+ formLength++ +` />
                                    </span>
                                </span>
                            </input>
                        </div>
                    </div>`
        document.getElementById(divName+'-main').appendChild(newDiv)
            $('[name="instructor-choice"]').html(items)

    }

}


function addInfo(divName, addBtn) {
    var formLength = document.getElementById(divName + '-main').childElementCount
    if (addBtn.className.includes("glyphicon-minus")) {
        addBtn.parentNode.parentNode.parentNode.parentNode.removeChild(addBtn.parentNode.parentNode.parentNode)
    }
    if (addBtn.className.includes("glyphicon-plus")) {
        addBtn.className = "input-group-append  glyphicon glyphicon-minus"
        var newDiv = document.createElement('div')
        newDiv.className =" form-group"
        newDiv.id = 'sinfo-'+formLength
        newDiv.innerHTML = `
                    <div class="col-lg-12 ">
                        <div class="input-group form-group">
                            <input placeholder = "Year" type="text" class="year-list input-group-addon form-control"name="year-in-0" id="year-in-0">
                            <input placeholder="Section" type="text" class="section-list input-group-addon form-control" name="section-in-0" id="section-in-0">
                            <span onclick="addInfo('sinfo',this.children[0].children[0])" class="input-group-addon">
                                <span>
                                    <span class="input-group-append glyphicon glyphicon-plus" id=`+ formLength++ +`" />
                                </span>
                            </span>
                            </input>
                        </div>
                    </div>`
        document.getElementById(divName + '-main').appendChild(newDiv)
    }

}



