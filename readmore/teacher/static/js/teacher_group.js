$(document).ready(function(){
    $(".student-block").each(function(){
       initialize_student($(this).attr('pk'));
    });
    $(".group-block.category-block").each(function(){
       initialize_group($(this).attr('pk'));
    });
});

function initialize_student(student_id){
    $.get( "/teacher/api/student/"+student_id+"?filter=1", function( data ) {
        $( "#read_week_"+student_id ).html( data.articles_week );
        $( "#student_activity_"+student_id).attr('src', '/static/img/engagement-0' +data.engagement+ '.png');
    });
}

function initialize_group(group_id){
    $.get( "/teacher/api/group/"+group_id+"?filter=2", function( data ) {
        $( "#category_rank_1").html( data.categories[0]);
        $( "#category_rank_2").html( data.categories[1]);
        $( "#category_rank_3").html( data.categories[2]);
    });
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
