var course_instructor_mapping = Object()
let course_list=[]
let instructors_list = ['wal']
let new_days = []
let start_time
let url = "/"
let periods_per_day
let student_groups = []


var instructors_list_global = []

$(document).ready(function(){


    


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
            console.log('COurse:'+v2+" ins="+v3)
            course_instructor_mapping[v2] = v3
        })
    

        $.ajax({
            type: "POST",
            url: url,
            data: {
                start_time: start_time,
                duration: duration,
                working_data: new_days,
                periods_per_day: periods_per_day,
                course_instructors: course_instructor_mapping,
                courses: course_list,
                student_groups: student_groups
            },
            success:(res)=>{
                console.log("HMMM")
            },
            dataType: 'json'
        });

    })

})

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
                            <div class="input-group form-group">
                            <input type="text" class="course-list input-group-addon form-control" id="courses-in-`+ formLength +`" name="course">
                            <input type=text" class="course-list input-group-addon form-control" name="instructors">
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



