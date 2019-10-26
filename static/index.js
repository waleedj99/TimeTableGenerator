
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



    $('#submit_btn').click(function(e){
        e.preventDefault();
        console.log('Ajax POST')

        let courses = $('.course-list')
        course_list = []
        courses.each(function(i, obj){
                course_list.push($(this).val())
        })

        let instructors = $('.instructors-list')
        instructors_list = []
        instructors.each(function(i, obj){
                instructors_list.push($(this).val())
        })

        let nrooms = $('#n_rooms').val()
        let start_time = $('#datetimepicker1').find('input').val()
        let duration = $('#duration').val()
        function check_day(d){

            if ($("#"+d.substring(0, 3)+"-check").prop('checked'))return true;
            return false;
        }
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        new_days = []
        days.forEach(function(it){
            if(check_day(it)){
                new_days.push(it)
            }
        })
        console.log(new_days)
        console.log(instructors_list)
        console.log(course_list)
        console.log(start_time)
    })


})

   function addCourse(divName,addBtn){
    var formLength = document.getElementById(divName + '-main').childElementCount
    console.log(addBtn.id)
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
                            <input type="text" class="course-list input-group-addon form-control" id="courses-in-`+ formLength +`">
                                <span class="input-group-addon">
                                    <span>
                                        <span  onclick="addCourse('courses',this)" class="input-group-append glyphicon glyphicon-plus" id=`+ formLength++ +` />
                                    </span>
                                </span>
                            </input>
                        </div>
                    </div>`
        document.getElementById(divName+'-main').appendChild(newDiv)
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
                            <span class="input-group-addon">
                                <span>
                                    <span onclick="addInfo('sinfo',this)"
                                        class="input-group-append glyphicon glyphicon-plus" id=`+ formLength++ +`" />
                                </span>
                            </span>
                            </input>
                        </div>
                    </div>`
        document.getElementById(divName + '-main').appendChild(newDiv)
    }

}

function addInstructor(divName,addBtn){
    var formLength = document.getElementById(divName + '-main').childElementCount
    console.log(addBtn.id)
    if (addBtn.className.includes("glyphicon-minus")) {
        addBtn.parentNode.parentNode.parentNode.parentNode.removeChild(addBtn.parentNode.parentNode.parentNode)
    }

    instructors_list_global.push($('#'+divName+'-in-'+(formLength-1)).val())

    items = []
    instructors_list_global.forEach(function(item){
        let i = `<option value=`+item+`">`+item+`</option>`
        items.push(i)
    })

    $('[name="instructor-choice"]').html(items)

    if (addBtn.className.includes("glyphicon-plus")) {
        addBtn.className = "input-group-append  glyphicon glyphicon-minus"
        var newDiv = document.createElement('div')
        newDiv.className = 'form-group'
        newDiv.id = "instructors-"+ formLength + ""
        newDiv.innerHTML = ` <div class="col-lg-12 ">
                            <div class="input-group form-group">
                            <input type="text" class="instructors-list input-group-addon form-control" id="instructors-in-`+ formLength +`">
                                <span class="input-group-addon">
                                    <span>
                                        <span  onclick="addInstructor('instructors',this)" class="input-group-append glyphicon glyphicon-plus" id=`+ formLength++ +` />
                                    </span>
                                </span>
                            </input>
                        </div>
                    </div>`
        document.getElementById(divName+'-main').appendChild(newDiv)
    }

}


