$.widget( "readmore.seemore", {
	// Default options
	options: {
		controlwidget: "articleviewer"
	},
	_create: function(){
		var _self = this
		console.log(this.options);
		// Find any instance of the controlwidget and
		// bind to the `wordclick' event
		$(":readmore-"+this.options.controlwidget).bind(
			this.options.controlwidget+"wordclick",
			function(event, data){
				_self.load(data['word']);
			}
		)
	},
	load: function(){
	}
})
