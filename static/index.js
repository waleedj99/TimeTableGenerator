


$(document).ready(()=>{

console.log('loaded')

$('#datetimepicker1').datetimepicker(
        {
            format: 'HH:mm'
        }
    );
$('#submit_btn').click(function(e){
    e.preventDefault()
    console.log('Ajax post')
    let n_rooms = $('#roomLength').val()
    let rooms = [...Array(n_rooms).keys()];
    courses = $('.course-list').val()
    console.log(courses)


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
        newDiv.innerHTML = ` <div class="form-group" id="courses-`+ formLength + `">
                    <div class="col-lg-12 ">
                        <div class="input-group form-group">
                            <input type="text" class="input-group-addon form-control" id="courses">
                                <span class="input-group-addon">
                                    <span>
                                        <span  onclick="addCourse('courses',this)" class="input-group-append glyphicon glyphicon-plus" id=`+ formLength++ +` />
                                    </span>
                                </span>
                            </input>
                        </div>
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
                            <input placeholder = "Year" type="text" class="input-group-addon form-control" id="courses">
                            <input placeholder="Section" type="text" class="input-group-addon form-control" id="courses">
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

