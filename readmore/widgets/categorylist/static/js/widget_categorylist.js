$.widget( "readmore.categorylist", {
	// Default options
	options: {
		sources: ['wikipedia'],
		click_cb: function(source, id){
			document.location = "/sources/"+source+"/"+id
		}
	},
	_create: function(){
		_self = this
		this.element.append("<ul>")
		for(var i = 0; i < this.options.sources.length; i++){

			api_call(
				'/sources/'+this.options.sources[i]+'/cat/',
				{},
				'GET',
				function(source){ return function(data, xhr){
					_self.add_categories(source, data)
				};}(this.options.sources[i])
			);
		}
	},
	add_categories: function(source, categories){
		_self = this
		for(var i = 0; i < categories.length; i++){
			this.element.first().append(
				$("<li>").html(categories[i]['title'])
				.click(function(source, id){ return function(){
					_self.options.click_cb(source, id);
				}; }(source, categories[i]['id']))
			);
		}
	}
})
