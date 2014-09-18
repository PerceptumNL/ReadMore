from readmore.content.thirdparty.wiktionary_api import WiktionaryParser

def create_term_card(term):
    clean = WiktionaryParser.clean_wikitext
    card = {'type': 'DictTermCard'}
    card['data'] = {
        'category': term.category_description,
        'word': term.entry,
        'meanings': []
    }
    synonyms = {}
    antonyms = {}
    for index, meaning in enumerate(term.meanings):
        definition = clean(meaning.definition)
        example = clean(meaning.example)
        if definition:
            card['data']['meanings'].append({
                'definition': definition,
                'example': example,
                'synonyms': meaning.synonyms,
                'antonyms': meaning.antonyms
                })
    return card

def create_verb_conj_card(term):
    clean = WiktionaryParser.clean_wikitext
    card = {'type': 'DictVerbConjCard'}
    card['data'] = {
        'word': term.entry,
        '1ps': clean(term.first_person_single),
        '2ps': clean(term.second_person_single),
        'plural': clean(term.plural),
        'past_single': clean(term.past_single),
        'past_plural': clean(term.past_plural),
        'auxiliary': clean(term.auxiliary),
        'past_participle': clean(term.past_participle)
    }
    return card
