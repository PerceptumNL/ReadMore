function Loader(container){
	var _self = this;

	_self.cache = {};

	// Series of CSS background-image statements, which will be appended with
	// the url of the article's image.
	var css_background_image = [
		"",
		"-webkit-gradient(linear, left top, left bottom,"+
			"from(rgba(0,0,0,0)), to(rgba(0,0,0,255))),",
		"-webkit-linear-gradient(top, rgba(0,0,0,0), rgba(0,0,0,0),"+
			"rgba(0,0,0,0), rgba(0,0,0,255)),",
		"-moz-linear-gradient(top, rgba(0,0,0,0), rgba(0,0,0,0),"+
			"rgba(0,0,0,0), rgba(0,0,0,255)),",
		"-ms-linear-gradient(top, rgba(0,0,0,0), rgba(0,0,0,0),"+
			"rgba(0,0,0,0), rgba(0,0,0,255)),",
		"-o-linear-gradient(top, rgba(0,0,0,0), rgba(0,0,0,0),"+
			"rgba(0,0,0,0), rgba(0,0,0,255)),",
		"linear-gradient(to bottom, rgba(0,0,0,0), rgba(0,0,0,0),"+
			"rgba(0,0,0,0), rgba(0,0,0,255)),"];

	_self.create_article = function(data){
		var article = $("<div class='articleTile'>");
		var inner = $("<a>").attr("href", data['url']);
		var content = $("<div class='articleContent'>");
		var css = "background: "+data['category-color']+";";
		css += "background-size: cover;";
		for(var i = 0; i < css_background_image.length; i++){
			css += "background-image: "+css_background_image[i]+
				"url('"+data['image']+"');"
		}
		content.attr('style', css);
		var title = $("<div class='articleTitle'>")
		title.append($("<h4>").text(data['title']))
		content.append(title);
		inner.append(content);
		article.append(inner);
		return article;
	}

	_self.clear = function(){
		var elems = $(container).isotope('getItemElements');
		$(container).isotope('remove', elems);
	}

	_self.load = function(data){
		for(var i=0; i < data['articles'].length; i++){
			var article = _self.create_article(data['articles'][i]);
			$(container).isotope('insert', article);
		}
		_self.cache[location.hash] = data;
	}

	_self.update = function(){
		_self.clear();
		if( location.hash in _self.cache ){
			_self.load(_self.cache[location.hash]);
		} else {
			var category = $(location.hash);
			if( category && category.attr('data-url') ){
				$.get(category.attr('data-url'),_self.load)
			}
		}
	}

	$(window).hashchange(_self.update);
}
