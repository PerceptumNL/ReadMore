$.widget( "readmore.carddeck", {
	// Default options
	options: {
		controlwidget: "articleviewer",
		cover: null,
		carddecks: [{ 'url': '/widgets/dictionary/', 'params': {'word':"%%WORD%%"}}]
	},
	_create: function(){
		var _self = this
		// Find any instance of the controlwidget and
		// bind to the `wordclick' event
		$(":readmore-"+this.options.controlwidget).bind(
			this.options.controlwidget+"wordclick",
			function(event, data){
				_self.load(data['word']);
			}
		)
	},
	decks: function(word){
		decks = []
		for(var i = 0; i < this.options.carddecks.length ; i++){
			var url = this.options.carddecks[i].url;
			var params = {};
			for(key in this.options.carddecks[i].params){
				params[key] = this.options.carddecks[i].params[key]
					.replace("%%WORD%%", word);
			}
			decks.push({'url':url, 'params':params});
		}
		return decks;
	},
    load: function(word){
		$(this.element).html("");
		if(this.options.cover){
			$(this.options.cover).addClass('open');
		}
		CardDeck(this.element, this.decks(word))
	}
})
