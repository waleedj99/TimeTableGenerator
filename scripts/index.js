
$(function () {
    $('#datetimepicker1').datetimepicker(
        {
            format: 'HH:mm'
        }
    );
});

function addCourse(divName,addBtn){
    var formLength = document.getElementById(divName + '-main').childElementCount
    console.log(addBtn.id)
    if (addBtn.className.includes("glyphicon-minus")) {
        addBtn.parentNode.parentNode.parentNode.parentNode.removeChild(addBtn.parentNode.parentNode.parentNode)
    }
    if (addBtn.className.includes("glyphicon-plus")) {
        addBtn.className = "input-group-append  glyphicon glyphicon-minus"
        var newDiv = document.createElement('div')
        newDiv.innerHTML = ` <div class="form-group" id="courses-" `+ formLength + `>
                    <div class="col-lg-12 ">
                        <div class="input-group form-group">
                            <input type="text" class="input-group-addon form-control" id="courses">
                                <span class="input-group-addon">
                                    <span>
                                        <span  onclick="addDiv('courses',this)" class="input-group-append glyphicon glyphicon-plus" id=`+ formLength++ +` />
                                    </span>
                                </span>
                            </input>
                        </div>
                    </div>
                </div>`
        document.getElementById(divName+'-main').appendChild(newDiv)
    }
    
}