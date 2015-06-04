$(document).ready(function(){
    $(".student-block").each(function(){
       initialize_student($(this).attr('pk'));
    });
});

function initialize_student(student_id){
    $.get( "api/student/"+student_id, function( data ) {
        $( "#read_week_"+student_id ).html( data.article_read.week );
        $( "#read_month_"+student_id ).html( data.article_read.month );
        $( "#read_total_"+student_id ).html( data.article_read.total );
        $( "#activity_"+student_id).html(data.engagement);
    });

}