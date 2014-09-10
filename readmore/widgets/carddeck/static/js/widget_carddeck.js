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
			deck = this.options.carddecks[i];
			for(key in deck.params){
				deck.params[key] = deck.params[key].replace("%%WORD%%", word);
			}
			decks.push(deck);
		}
		return decks;
	},
    load: function(word){
		if(this.options.cover){
			$(cover).addClass('open');
		}
		CardDeck(this.element, this.decks(word))
	}
})
