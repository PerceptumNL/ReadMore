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
			}
		);
	},
})