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
        var _self = this;
		if(this.options.cover){
			$(this.options.cover).addClass('open');
		}
        $(this.options.cover).find("#closeCover").click(
                function(){ _self.close(_self.options.cover); });
        $(this.options.cover).find("#closeOnBackground").click(
                function(){ _self.close(_self.options.cover); });                
                
                
		this.carddeck = new CardDeck(this.element, this.decks(word));
	},
    close: function(cover){
		if(cover){
		    $(cover).removeClass('open');
        }
        $('#selected').addClass('prevSelected');
        $('.lastSelected').removeClass('lastSelected');
        $('#selected').addClass('lastSelected');
        $('#selected').removeAttr('id');
        this.carddeck.close();
    }
})
