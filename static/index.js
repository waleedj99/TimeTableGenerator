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

        let courses = $('.course-list').val()
        console.log(courses);


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