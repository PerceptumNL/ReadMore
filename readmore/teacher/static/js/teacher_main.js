$(document).ready(function(){
    $(".group-block").each(function(){
       initialize_group($(this).attr('pk'));
    });
});

function initialize_group(group_id){
    $.get( "api/group/"+group_id, function( data ) {
        $( "#groupsize_"+group_id ).html( data.student_count );
        $( "#read_week_"+group_id ).html( data.article_read.week );
        $( "#read_month_"+group_id ).html( data.article_read.month );
        $( "#read_total_"+group_id ).html( data.article_read.total );
        $( "#word_week_"+group_id ).html( data.article_word.week );
        $( "#word_month_"+group_id ).html( data.article_word.month );
        $( "#word_total_"+group_id ).html( data.article_word.total );
        $( "#activity_"+group_id).html(data.engagement);
        $( "#group_activity_"+group_id).attr('src', '/static/img/engagement-0'+data.engagement+'.png');
        
        $.each( data.articles, function( index, value ){
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
            
            // Freq
            var freq = $("<span>");
            freq.addClass("article-freq");
            freq.html(value.freq + "x");
            
            title.append(freq);
            title_div.append(title);
            block.append(title_div);
            
            $( "#articles_"+group_id).append(block);
        });
        
    });

}

/*
 <div class="article-block link-div">
                <a href="{% url 'article' article.pk %}"></a>
                <div class="article-image">
                    <img src="{{article.image}}">
                </div>
                <div class="article-title">
                    <h6>{{article.title}}<span class="article-freq">22x</span></h6>
                </div>
            </div>
*/
