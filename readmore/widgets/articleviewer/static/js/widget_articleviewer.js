$.widget( "readmore.articleviewer", {
	// Default options
	options: {
		article: undefined
	},
	_create: function(){
		_self = this
		api_call(
			this.options.article,
			{},
			'GET',
			function(data, xhr){
				_self.element.html(data['body']);
				_self.process(_self.element);
			}
		);
	},
	process: function(data){
		$('.mw-editsection').remove();
		$('a').each(function(){
			var link = $(this).attr('href');
			if(link.substring(0,5) == "/wiki"){
				var link = '/sources/wikipedia' + link.substring(5);
				$(this).attr('href', link);
			}
			
		})
	}
})