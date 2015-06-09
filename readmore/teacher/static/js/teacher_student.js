$(document).ready(function(){
    $(".student-block").each(function(){
       initialize_student($(this).attr('pk'));
    });
});

function initialize_student(student_id){
    $.get("/teacher/api/student/"+student_id+"?filter=2", function( data ) {
        var clicked_list = "<ul>";
        for (var i in data.clicked_words) {
            clicked_list += "<li>" +data.clicked_words[i]+ "</li>";
        }
        clicked_list += "</ul>";
        $("#clicked_words").html(clicked_list);
        
        var read_list = "<ul>";
        for (var i in data.articles_read) {
            read_list += "<li>" +data.articles_read[i]+ "</li>";
        }
        read_list += "</ul>";
        $("#articles_read").html(read_list);
    });
}