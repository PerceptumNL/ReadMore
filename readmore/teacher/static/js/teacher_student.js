function initialize_student(student_resource){
    $.get(student_resource, function( data ) {
		draw_activity("#student_activity", data.engagement);
		draw_category_list("#student_categories", data.categories);
		draw_word_list("#student_words", data.words)
		draw_article_list("#student_articles", data.articles);
		// Load last interesting rating
        if (!$.isEmptyObject(data.rating)) {
			draw_rating_block("#rating", data.rating)
        } else {
            var title = $("<h6 style='margin: 8px 8px 8px 24px'>");
            title.html("Er zijn nog geen ratings gegeven deze week");
            $( "#rating").append(title);
        }
		// Load last difficulty rating
        if (!$.isEmptyObject(data.difficulty)) {
			draw_rating_block("#difficulty", data.difficulty)
        } else {
            var title = $("<h6 style='margin: 8px 8px 8px 24px'>");
            title.html("Er zijn nog geen ratings gegeven deze week");
            $( "#difficulty").append(title);
        }
        // Progress graph
        data.progress.forEach(function(d, i) {
            draw_progress_graph("#progress", d, data.week_nr -4 +i);
        });
    });
}
