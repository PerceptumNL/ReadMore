$(document).ready(function(){
    $(".student-block").each(function(){
       initialize_student($(this).attr('pk'));
    });
    $(".group-block.category-block").each(function(){
       initialize_group($(this).attr('pk'));
    });
});

function initialize_student(student_id){
    $.get( "api/student/"+student_id, function( data ) {
        $( "#read_week_"+student_id ).html( data.article_read.week );
        $( "#student_activity_"+student_id).attr('src', '/static/img/engagement-0' +data.engagement+ '.png');
    });
}

function initialize_group(group_id){
    $.get( "/teacher/api/group/"+group_id, function( data ) {
        $( "#category_rank_1").html( data.categories[0]);
        $( "#category_rank_2").html( data.categories[1]);
        $( "#category_rank_3").html( data.categories[2]);
    });
}
