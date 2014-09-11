function CardDeck(container, decks){
	var _self = this;

	this.create_empty_card = function(){
		return $("<div class='element-item col-lg-4 col-md-6 col-xs-12'>");
	}

	this.load_deck = function(deck){
		for(var i = 0; i < deck.length; i++){
			if(deck[i]['type'] in window){
				card = _self.create_empty_card();
				window[deck[i]['type']](card, deck[i]['data']);
				$(container).isotope('insert', card);
			}
		}
	}

	for(var i = 0; i < decks.length; i++){
		api_call(decks[i]['url'], decks[i]['params'], 'get', this.load_deck)
	}
}

function Card(container, title){
	container.append($("<span class='title'>"+title+"</span>"))
}

function DictTermCard(container, data){
	Card(container, "Betekenis van <b>"+data['word']+"</b>")
	container.addClass("dict_term_card")
	container.append($('<span class="word">'+data['word']+'</span>'));
	container.append($('<span class="category">('+data['category']+')</span>'));
	if(!$.isEmptyObject(data['meanings'])){
		meanings = $("<dl>");
		container.append(meanings);
		for(index in data['meanings']){
			meaning = data['meanings'][index];
			meanings.append($('<dt>').text(index+"."));
			meanings.append($('<dd>').text(meaning['definition']));
			if(meaning['example']){
				meanings.append($('<dd>').text(meaning['example']));
			}
		}
	}
}

function DictSynonymCard(container, data){
	Card(container, "Hetzelfde als <b>"+data['word']+"</b>")
	container.append($('<span class="word">'+data['word']+'</span>'));
	container.append(
		$('<span class="category">('+data['term_category']+')</span>'));
	if(!$.isEmptyObject(data['synonyms'])){
		synonyms = $("<dl>");
		container.append(synonyms);
		for(index in data['synonyms']){
			synonym_list = data['synonyms'][index];
			synonyms.append($('<dt>').text(index+"."));
			synonyms.append($('<dd>').text(synonym_list.join(", ")));
		}
	}
}

function DictAntonymCard(container, data){
	Card(container, "Tegenovergestelde van <b>"+data['word']+"</b>")
	container.append($('<span class="word">'+data['word']+'</span>'));
	container.append(
		$('<span class="category">('+data['term_category']+')</span>'));
	if(!$.isEmptyObject(data['antonyms'])){
		antonyms = $("<dl>");
		container.append(antonyms);
		for(index in data['antonyms']){
			antonym_list = data['antonyms'][index];
			antonyms.append($('<dt>').text(index+"."));
			antonyms.append($('<dd>').text(antonym_list.join(", ")));
		}
	}
}
