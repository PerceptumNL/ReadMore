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
                block.addClass('articleTile');
                block.attr("style", "background-image: url('"+value.image+"');");
                var link = $("<a>");
                link.attr('href', value.url);
                block.append(link);
                
                var title = $('<div>');
                title.addClass("articleTitle");
                var par = $('<p>');
                par.html(value.title);
                title.html(par);
                block.append(title);
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
            block.addClass('articleTile');
            block.addClass('rating-block');
            block.attr("style", "background-image: url('"+data.rating.image+"');");
            var link = $("<a>");
            link.attr('href', data.rating.url);
            block.append(link);
            
            var title = $('<div>');
            title.addClass("articleTitle");
            var par = $('<p>');
            par.html(data.rating.title);
            title.html(par);
            block.append(title);
            
            var rating = $('<h2>');
            for (i = 0; i < 5; i++) {
                if (i < data.rating.rating) {
                    rating.append('<i class="fa fa-star">')
                } else {
                    rating.append('<i class="fa fa-star-o">')
                }
            }
            block.append(rating);
            
            $( "#rating").append(block);
        } else {
            var title = $("<h6 style='margin: 8px 8px 8px 24px'>");
            title.html("Er zijn nog geen ratings gegeven deze week");
            $( "#rating").append(title);
        }
        
        if (!$.isEmptyObject(data.difficulty)) {
            var block = $('<div>');
            block.addClass('articleTile');
            block.addClass('rating-block');
            block.attr("style", "background-image: url('"+data.difficulty.image+"');");
            var link = $("<a>");
            link.attr('href', data.difficulty.url);
            block.append(link);
            
            var title = $('<div>');
            title.addClass("articleTitle");
            var par = $('<p>');
            par.html(data.difficulty.title);
            title.html(par);
            block.append(title);
            
            var rating = $('<h2>');
            for (i = 0; i < 5; i++) {
                if (i < data.difficulty.rating) {
                    rating.append('<i class="fa fa-star">')
                } else {
                    rating.append('<i class="fa fa-star-o">')
                }
            }
            block.append(rating);
            
            $( "#difficulty").append(block);
        } else {
            var title = $("<h6 style='margin: 8px 8px 8px 24px'>");
            title.html("Er zijn nog geen ratings gegeven deze week");
            $( "#difficulty").append(title);
        }
        
        var graph = d3.select("#graph"),
            WIDTH = 450,
            HEIGHT = 350,
            MARGINS = {
                top: 20,
                right: 20,
                bottom: 50,
                left: 50
            },
            xScale = d3.scale.linear().range([MARGINS.left, WIDTH - MARGINS.right]).domain([-4, -1]),
            yScale = d3.scale.linear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([0, 10]),
            yAxis = d3.svg.axis().scale(yScale).tickFormat(d3.format("d")).orient('left');
        graph.append("svg:g")
            .attr("transform", "translate(" + (MARGINS.left) + ",0)")
            .call(yAxis);
        
        graph.selectAll("circle")
           .data(data.progress)
           .enter()
           .append("circle")
           .attr("cx", function(d, i) {
                return xScale(-4 + i);
           })
           .attr("cy", function(d, i) {
                return yScale(d);
           })
           .attr("r", 5)
           .attr("fill", "blue");
        
        
    });
}