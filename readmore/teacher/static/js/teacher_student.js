$(document).ready(function(){
    $(".student-block").each(function(){
       initialize_student($(this).attr('pk'));
    });
});

function initialize_student(student_id){
    $.get("/teacher/api/student/"+student_id+"?filter=2", function( data ) {
        if(data.articles_read.length>0){
            $.each( data.articles_read, function( index, value ){
                var block = $('<div>');
                block.addClass('article-block');
                block.addClass('link-div');
                // Link
                var link = $("<a>");
                link.attr('href', value.url);
                block.append(link);
                // Image
                var image_div = $("<div>");
                image_div.addClass("article-image");
                var image = $("<img>");
                image.attr('src', value.image);
                image_div.append(image);
                block.append(image_div);
                // Title
                var title_div = $("<div>");
                title_div.addClass("article-title");
                var title = $("<h6>");
                title.html(value.title);
                title_div.append(title);
                block.append(title_div);
                
                $( "#articles_read").append(block);
            });
        } else{
            var title = $("<h6 style='margin: 8px 8px 8px 24px'>");
            title.html("Er zijn nog geen artikelen gelezen deze week");
            $( "#articles_read").append(title);
        }
        
        if(data.clicked_words.length>0){
            $.each( data.clicked_words, function( index, value ){
                var block = $('<div>');
                block.addClass('word-block');
                var link = $("<a>");
                link.attr('href', 'http://nl.wiktionary.org/wiki/'+value);
                link.html(value);
                var title = $("<h6>");
                title.html(link);
                block.append(title);
                
                $( "#clicked_words").append(block);
            });
        } else {
            var title = $("<h6 style='margin: 8px 8px 8px 24px'>");
            title.html("Er zijn nog geen woorden bekeken deze week");
            $( "#clicked_words").append(title);
        }
        
        if (!$.isEmptyObject(data.rating)) {
            var block = $('<div>');
            block.addClass('rating-block');
            var link = $("<a>");
            link.attr('href', data.rating.link);
            link.html(data.rating.title);
            
            for (i = 0; i < 5; i++) {
                if (i < data.rating.rating) {
                    link.append('<i class="fa fa-star">')
                } else {
                    link.append('<i class="fa fa-star-o">')
                }
            }
            
            var title = $("<h5>");
            title.html(link);
            block.append(title);
            $( "#rating").append(block);
        } else {
            var title = $("<h6 style='margin: 8px 8px 8px 24px'>");
            title.html("Er zijn nog geen ratings gegeven deze week");
            $( "#rating").append(title);
        }
        
        if (!$.isEmptyObject(data.difficulty)) {
            var block = $('<div>');
            block.addClass('rating-block');
            var link = $("<a>");
            link.attr('href', data.difficulty.link);
            link.html(data.difficulty.title);
            
            for (i = 0; i < 5; i++) {
                if (i < data.difficulty.rating) {
                    link.append('<i class="fa fa-star">')
                } else {
                    link.append('<i class="fa fa-star-o">')
                }
            }
            
            var title = $("<h5>");
            title.html(link);
            block.append(title);
            $( "#difficulty").append(block);
        } else {
            var title = $("<h6 style='margin: 8px 8px 8px 24px'>");
            title.html("Er zijn nog geen ratings gegeven deze week");
            $( "#difficulty").append(title);
        }
        
        //data.progress
    });
}