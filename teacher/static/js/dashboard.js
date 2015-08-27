function getCookie(name) {
	// Helper function for cookie retrieval
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

function draw_rating_block(container, data){
    var block = $('<div class="articleTile rating-block">');
    block.attr("style", "background-image: url('"+data.image+"');");
	block.append("<a href='"+data.url+"'>");
    block.append('<div class="articleTitle"><p>'+data.title+'</p></div>');
	var rating = $('<h2 style="margin-top: 0;">');
	for (i = 0; i < 5; i++) {
		if (i < data.rating) {
			rating.append('<i class="fa fa-star">')
		} else {
			rating.append('<i class="fa fa-star-o">')
		}
	}
	$(container).append(rating);
	$(container).append(block);
}

function draw_word_list(container, words){
	$.each( words, function( index, value ){
		var block = $('<div class="word-block">');
		var link = $("<a>");
		link.attr('href', 'http://nl.wiktionary.org/wiki/'+value);
		link.html(value);
		block.append($("<h6>").html(link))
		$(container).append(block);
	});
}

function draw_category_list(container, categories){
	$(container).addClass("category-block");
	var list = $("<ul>")
	$.each( categories, function( index, value ){
		list.append("<li><h5>"+value+"</h5></li>")
	});
	$(container).append(list)
}

function draw_article_list(container, articles){
	$.each( articles, function( index, value ){
		var block = $('<div class="articleTile">');
		if(value.image){
			block.attr("style", "background-image: url('"+value.image+"');");
		}
		block.append("<a href='"+value.url+"'>");
		block.append('<div class="articleTitle"><p>'+value.title+'</p></div>');
		$(container).append(block);
	});
}

function draw_activity(container, activity){
	$(container).addClass("activity-block");
	$(container).append("<img src='/static/img/engagement-0"+activity+".png'>")
	$(container).append($("<div class='cover'>").append(
			"<h1><h1><sup>"+activity+"</sup>&frasl;<sub>5</sub></h1>"))
}

function draw_progress_graph(container, engagement, week){
    var dy = 50;
    var img = $("<img>");
    img.attr("src", "/static/img/engagement-0"+engagement.toString()+".png");
    img.attr("style", "margin-top:"+((5-engagement)*dy).toString()+"px;"+
        "margin-bottom:"+(engagement*dy).toString()+"px");
    $(container+"_images").append($("<td>").html(img));
    var week = $("<h5>").html("Week "+week.toString());
    $(container+"_weeks").append($("<td>").html(week));
}

$(function(){
	$(".form-show").click(function(){
		current_id = $(this).attr('id').split("-")[0];
		$("#"+current_id+"-form").slideToggle();
	});
	$(".student-show").click(function(){
		current_id = $(this).attr('id').split("-")[0];
		$("#"+current_id+"-students").slideToggle();
	})
});
