"""Wiktionary API module.

The Wiktionary API module provides a main class WiktionaryAPI, through which
information from a wiktionary site about a word can be retrieved, and a set of
classes in which this information is represented. In order to understand the
purpose of each of these representation classes, it is useful to first
understand what information needs to be represented.

First of all, a word can have multiple meanings. For each of these meanings,
one might give an example sentence or there might be synonyms or antonyms.
However, words can not only have multiple meanings. Words can also be used in
the role of different lexical categories, e.g. `bank' can be used as both a
noun and a verb. Furthermore, the word `bank' is part of multiple languages.

In this module, all information about the word within the context of a specific
language is stored in a TermSet object. Specifically it contains a list of Term
objects. A Term object represents all information of the word within the
context of one lexical category (e.g. noun). It contains various information
depending on the lexical category it represents, including a list of
Meaning objects. Each Meaning object represents one particular meaning of the
word, linking definitions, synonyms, antonyms and example sentences. See the
docstrings of the individual classes for more details.

In many cases, a word is not in its normal form. For example, a noun might be
in its plural form. In this module the word `banks' is referred to a form or
the word `bank'. Where the word `bank' was represented by a (subclass of a)
Term object, the word 'banks' is represented by a (subclass of a) TermForm
object. These objects contain the form they are, and of which word. See the
docstrings of the individual classes for more details.

The representation classes are created by the WiktionaryParser, which parses
raw wikitext. Normally you would not need to interact with this parser object.
This module provides a WiktionaryAPI class that combines retreving the wikitext
from a wiktionary site with executing the parser. Calling the `get_info'
method will return all wiktionary information about a given word.

Known issues:
    * Does not support any other wiktionary formats than the Dutch one.
    * Does not support different conjugations per meaning of a term
    * Does not support different antonyms per meaning
    * Does not support stress homographs
"""
import re
from django.conf import settings
from content.thirdparty.wiki_api import MediaWikiAPI
from string import whitespace, punctuation
from django.utils.translation import pgettext

class Meaning(object):
    """Representation of a particular meaning of a term."""
    _definition = u''
    _example = u''
    _synonyms = None
    _antonyms = None

    def __init__(self, definition=u'', example=u'', synonyms=None,
            antonyms=None):
        """
        Keyword arguments:
        definition - The definition of this meaning. (Default u'')
        example - The example sentence of this meaning. (Default u'')
        synonyms - A list of synonyms of this meaning. (Default [])
        antonyms - A list of antonyms of this meaning. (Default [])
        """
        self._definition = definition
        self._example = example
        self._synonyms = [] if synonyms is None else synonyms
        self._antonyms = [] if antonyms is None else antonyms

    @property
    def definition(self):
        """Return the definition of this meaning."""
        return self._definition

    @definition.setter
    def definition(self, value):
        """Set the definition of this meaning."""
        self._definition = value

    @property
    def example(self):
        """Return an example sentence of this meaning."""
        return self._example

    @example.setter
    def example(self, value):
        """Set an example sentence of this meaning."""
        self._example = value

    @property
    def synonyms(self):
        """Return the list of synonyms for this meaning."""
        return self._synonyms

    @synonyms.setter
    def synonyms(self, value):
        """Set the list of synonyms for this meaning."""
        self._synonyms = value

    @property
    def antonyms(self):
        """Return the list of antonyms for this meaning."""
        return self._antonyms

    @antonyms.setter
    def antonyms(self, value):
        """Set the list of antonyms for this meaning."""
        self._antonyms = value

    def __repr__(self):
        return '%s("%s...")' % (self.__class__.__name__, self._definition[:20])


class Term(object):
    """Base class for a term, combining meanings per lexical category."""
    # Term entry
    _entry = u''
    # Meanings
    _meanings = None
    # Hyponyms
    _hyponyms = None

    def __init__(self):
        self._meanings = []
        self._hyponyms = []

    @property
    def entry(self):
        """Return the wiktionary entry of the word
        NOTE: This is probably always the same as the word.
        """
        return self._entry

    @entry.setter
    def entry(self, value):
        """Set the wiktionary entry of the word."""
        self._entry = value

    @property
    def meanings(self):
        """Return a list of the meanings of this word."""
        return self._meanings

    def add_meaning(self, meaning):
        """Add a meanings of this word."""
        self._meanings.append(meaning)

    @property
    def hyponyms(self):
        """Return a list of the hyponyms of this word."""
        return self._hyponyms

    def add_hyponym(self, hyponym):
        """Add a hyponym of this word."""
        self._hyponyms.append(hyponym)

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self._entry)


class TermForm(object):
    """Base class for terms that are a specific variant of a main term."""
    # The main term
    _main_term = None
    # The provided form type
    _form = None
    # A dictionary translating form codes to human-readable text
    _form_rewrites = None

    def __init__(self, main_term, form):
        """
        Keyword arguments:
        main_term - The word of which this is a form.
        form - The name of which form this is.
        """
        self._main_term = main_term
        self._form = form
        self._form_rewrites = {}

    @property
    def main_term(self):
        """Return the main term of which is a form."""
        return self._main_term

    @property
    def form(self):
        """Return which form of the main term this is."""
        return self._form

    def add_form_rewrite_rule(self, lang, form, rule):
        """Add a rewrite rule to create a human readable form description."""
        if lang not in self._form_rewrites:
            self._form_rewrites[lang] = {form: [rule]}
        elif form not in self._form_rewrites[lang]:
            self._form_rewrites[lang][form] = [rule]
        else:
            self._form_rewrites[lang][form].append(rule)

    def form2text(self, lang='nl'):
        """Return the human-readable text description(s) of the form.

        Keyword arguments:
        lang - The language of the text. (Default 'nl')
        """
        text = []
        # Check if we have a rewrite rule for this language and form.
        if (lang in self._form_rewrites and
            self.form in self._form_rewrites[lang]):
            for rule in self._form_rewrites[lang][self.form]:
                text.append(rule(self))
            return text
        else:
            return []

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self._main_term)

class NounTermForm(TermForm):
    """Class for forms of a noun."""

    def __init__(self, main_term, form):
        """
        Supported noun forms are:
          * noun-pl (plural)
          * noun-dim (dimunitive)
          * noun-dim-pl (dimunitive plural)

        Keyword arguments:
        main_term - The word of which this is a form.
        form - The name of which form this is.
        """
        if form not in ['noun-pl', 'noun-dim', 'noun-dim-pl']:
            raise ValueError("Unsupported form type")
        super(NounTermForm, self).__init__(main_term, form)
        self._init_rewrite_rules()

    @property
    def is_plural(self):
        """Return if this is the plural form."""
        return self.form == 'noun-pl'

    @property
    def is_diminutive(self):
        """Return if this is the diminutive form."""
        return self.form == "noun-dim"

    @property
    def is_diminutive_plural(self):
        """Return if this is the diminutive form."""
        return self.form == "noun-dim-pl"

    def _init_rewrite_rules(self):
        """Initialize rewrite rules for each form."""
        # Define template rule
        rule_template = lambda s: (lambda x: s % (x.main_term, ))
        #Add Dutch rewrite rules
        self.add_form_rewrite_rule('nl', 'noun-pl', rule_template(
            "meervoud van het zelfstandig naamwoord %s"))
        self.add_form_rewrite_rule('nl', 'noun-dim', rule_template(
            "verkleinwoord enkelvoud van het zelfstandig naamwoord %s"))
        self.add_form_rewrite_rule('nl', 'noun-dim-pl', rule_template(
            "verkleinwoord meervoud van het zelfstandig naamwoord %s"))


class VerbTermForm(TermForm):
    """Class for forms of a verb."""

    def __init__(self, main_term, form):
        """
        Supported verb forms are:
          * 1ps or 1ps-ij or 1ps-bijz (present 1st person single)
          * 2ps or 2ps-ij or 2ps-bijz (present 2st person single)
          * tps or tps-bijz (present 1st/2nd/3rd person single)
          * aanv-w or aanv-w-bijz (Subjunctive)
          * nl-prcp or volt-d (Past participle)
          * onv-d (Present participle)
          * ott-gij (Present 'Thou ..')
          * ott-mv (Present plural)
          * ott-onp (Present impersonal)
          * ovt-enk or ovt-enk-bijz (Past single)
          * ovt-gij or ovt-gij-bijz (Past 'Thou ..')
          * ovt-mv or ovt-mv-bijz (Past plural)
          * ovt-onp (Past impersonal)

        Keyword arguments:
        main_term - The word of which this is a form.
        form - The name of which form this is.
        """
        if form not in [
                '1ps', '1ps-ij', '1ps-bijz', '2ps', '2ps-ij', '2ps-bijz',
                'tps', 'tps-bijz', 'aanv-w', 'aanv-w-bijz', 'nl-prcp',
                'volt-d', 'onv-d', 'ott-gij', 'ott-mv', 'ott-onp', 'ovt-enk',
                'ovt-enk-bijz', 'ovt-gij', 'ovt-gij-bijz', 'ovt-mv',
                'ovt-mv-bijz', 'ovt-onp'
                ]:
            raise ValueError("Unsupported form type")
        super(VerbTermForm, self).__init__(main_term, form)
        self._init_rewrite_rules()

    @property
    def is_present_1ps(self):
        """Return if this is the present 1st person single form."""
        return self.form in ['1ps', '1ps-ij', '1ps-bijz']

    @property
    def is_present_2ps(self):
        """Return if this is the present 2nd person single form."""
        return self.form in ['2ps', '2ps-ij', '2ps-bijz']

    @property
    def is_present_tps(self):
        """Return if this is the present 1st/2nd/3rd person single form."""
        return self.form in ['tps', 'tps-bijz']

    @property
    def is_subjunctive(self):
        """Return if this is the subjunctive form."""
        return self.form in ['aanv-w', 'aanv-w-bijz']

    @property
    def is_past_participle(self):
        """Return if this is the past participle form."""
        return self.form in ['nl-prcp', 'volt-d']

    @property
    def is_present_participle(self):
        """Return if this is the present participle form."""
        return self.form == 'onv-d'

    @property
    def is_present_thou(self):
        """Return if this is the present 'Thou ..' form."""
        return self.form == 'ott-gij'

    @property
    def is_present_plural(self):
        """Return if this is the present plural form."""
        return self.form == 'ott-mv'

    @property
    def is_present_impersonal(self):
        """Return if this is the present impersonal form."""
        return self.form == 'ott-onp'

    @property
    def is_past_single(self):
        """Return if this is the past single form."""
        return self.form in ['ovt-enk', 'ovt-enk-bijz']

    @property
    def is_past_thou(self):
        """Return if this is the past 'Thou ..' form."""
        return self.form in ['ovt-gij', 'ovt-gij-bijz']

    @property
    def is_past_plural(self):
        """Return if this is the past plural form."""
        return self.form in ['ovt-mv', 'ovt-mv-bijz']

    @property
    def is_past_impersonal(self):
        """Return if this is the past impersonal form."""
        return self.form == 'ovt-onp'

    def _init_rewrite_rules(self):
        """Initialize rewrite rules for each form."""
        # Define template rule
        rule_template = lambda s: (lambda x: s % (x.main_term, ))
        ### Add Dutch rewrite rules
        # Present 1ps family
        for form in ['1ps', '1ps-ij', '1ps-bijz']:
            self.add_form_rewrite_rule('nl', form, rule_template(
                "eerste persoon enkelvoud tegenwoordige tijd van %s"))
            self.add_form_rewrite_rule('nl', form, rule_template(
                "gebiedende wijs van %s"))
            self.add_form_rewrite_rule('nl', form, rule_template(
                ("(bij inversie) tweede persoon enkelvoud "
                 "tegenwoordige tijd van %s")
                ))
        # Present 2ps family
        for form in ['2ps', '2ps-ij', '2ps-bijz']:
            self.add_form_rewrite_rule('nl', form, rule_template(
                "tweede persoon enkelvoud tegenwoordige tijd van %s"))
            self.add_form_rewrite_rule('nl', form, rule_template(
                "derde persoon enkelvoud tegenwoordige tijd van %s"))
            self.add_form_rewrite_rule('nl', form, rule_template(
                "verouderde gebiedende wijs meervoud van %s"))
        # Present tps family
        for form in ['tps', 'tps-bijz']:
            self.add_form_rewrite_rule('nl', form, rule_template(
                "enkelvoud tegenwoordige tijd van %s"))
            self.add_form_rewrite_rule('nl', form, rule_template(
                "gebiedende wijs van %s"))
        # Subjunctive family
        for form in ['aanv-w', 'aan-v-bijz']:
            self.add_form_rewrite_rule('nl', form, rule_template(
                "aanvoegende wijs van %s"))
        # Past participle family
        for form in ['nl-prcp', 'volt-d']:
            self.add_form_rewrite_rule('nl', form, rule_template(
                "voltooid deelwoord van %s"))
        # Present participle
        self.add_form_rewrite_rule('nl', 'onv-d', rule_template(
            "onvoltooid deelwoord van %s"))
        # Present thou
        self.add_form_rewrite_rule('nl', 'ott-gij', rule_template(
            "gij-vorm tegenwoordige tijd van %s"))
        # Present plural
        self.add_form_rewrite_rule('nl', 'ott-mv', rule_template(
            "meervoud tegenwoordige tijd van %s"))
        # Present impersonal
        self.add_form_rewrite_rule('nl', 'ott-onp', rule_template(
            "onpersoonlijke tegenwoordige tijd van %s"))
        # Past single family
        for form in ['ovt-enk', 'ovt-enk-bijz']:
            self.add_form_rewrite_rule('nl', form, rule_template(
                "enkelvoud verleden tijd van %s"))
        # Past thou family
        for form in ['ovt-gij', 'ovt-gij-bijz']:
            self.add_form_rewrite_rule('nl', form, rule_template(
                "gij-vorm verleden tijd van %s"))
        # Past plural family
        for form in ['ovt-mv', 'ovt-mv-bijz']:
            self.add_form_rewrite_rule('nl', form, rule_template(
                "meervoud verleden tijd van %s"))
        # Past impersonal
        self.add_form_rewrite_rule('nl', 'ovt-onp', rule_template(
            "onpersoonlijke verleden tijd van %s"))


class AdjectiveTermForm(TermForm):
    """Class for forms of an adjective."""

    def __init__(self, main_term, form):
        """
        Supported adjective forms are:
          * decl-pos (declined positive)
          * decl-com (declined comparitive)
          * decl-sup (declined superlative)
          * indecl-pos (indeclined positive)
          * indecl-com (indeclined comparitive)
          * indecl-sup (indeclined superlative)
          * part-pos (partitive positive)
          * part-com (partitive comparitive)
          * part-sup (partitive superlative)

        Keyword arguments:
        main_term - The word of which this is a form.
        form - The name of which form this is.
        """
        if form not in [
            'decl-pos', 'decl-com', 'decl-sup',
            'indecl-pos', 'indecl-com', 'indecl-sup',
            'part-pos', 'part-com', 'part-sup',
            ]:
            raise ValueError("Unsupported form type")
        super(AdjectiveTermForm, self).__init__(main_term, form)
        self._init_rewrite_rules()

    @property
    def is_declined(self):
        """Return if the adjective form is declined.
        In Dutch, 'beter' would be indeclined and 'betere' declined.
        """
        return bool(re.match('decl', self.form))

    @property
    def is_indeclined(self):
        """Return if the adjective form is indeclined.
        In Dutch, 'beter' would be indeclined and 'betere' declined.
        """
        return bool(re.match('indecl', self.form))

    @property
    def is_partitive(self):
        """Return if the adjective form is partitive.
        Indicating partialness or indeterminateness, such as "some water" or
        "something nice". In Dutch, it is a word form that is used when referring to
        undetermined things or amounts.
        """
        return bool(re.match('part', self.form))

    @property
    def is_positive(self):
        """ Return if the adjective form is positive.
        Positive is the 'normal' form of the degrees of comparison of an
        adjective or adverb. Thus big is the positive form of the trio big,
        bigger, biggest.
        """
        return bool(re.match('.*-pos', self.form))

    @property
    def is_comparitive(self):
        """Return if the adjective form is comparitive.
        An inflection, or different form, of a comparable adjective showing a
        relative quality, usually denoting 'to a greater extent' but not 'to
        the ultimate extent' (see also superlative and degrees of comparison).
        In English, the comparative form is usually formed by appending -er, or
        using the word more. For example, the comparative of hard is 'harder';
        of difficult, 'more difficult'.
        """
        return bool(re.match('.*-com', self.form))

    @property
    def is_superlative(self):
        """Return if the adjective form is superlative.
        An inflection, or different form, of a comparable adjective showing a
        relative quality, denoting 'to the ultimate extent' (see also
        comparative and degrees of comparison). In English, the superlative
        form is often formed by appending -est, or using the word most. For
        example, the superlative of big is 'biggest'; of confident, 'most
        confident'
        """
        return bool(re.match('.*-sup', self.form))

    def _init_rewrite_rules(self):
        """Initialize rewrite rules for each form."""
        # Define template rule
        rule_template = lambda s: (lambda x: s % (x.main_term, ))
        #Add Dutch rewrite rules
        self.add_form_rewrite_rule('nl', 'decl-pos', rule_template(
            "verbogen vorm van de stellende trap van %s"))
        self.add_form_rewrite_rule('nl', 'decl-com', rule_template(
            "verbogen vorm van de vergrotende trap van %s"))
        self.add_form_rewrite_rule('nl', 'decl-sup', rule_template(
            "verbogen vorm van de overtreffende trap van %s"))
        self.add_form_rewrite_rule('nl', 'indecl-pos', rule_template(
            "onverbogen vorm van de stellende trap van %s"))
        self.add_form_rewrite_rule('nl', 'indecl-com', rule_template(
            "onverbogen vorm van de vergrotende trap van %s"))
        self.add_form_rewrite_rule('nl', 'indecl-sup', rule_template(
            "onverbogen vorm van de overtreffende trap van %s"))
        self.add_form_rewrite_rule('nl', 'part-pos', rule_template(
            "partitief vorm van de stellende trap van %s"))
        self.add_form_rewrite_rule('nl', 'part-com', rule_template(
            "partitief vorm van de vergrotende trap van %s"))
        self.add_form_rewrite_rule('nl', 'part-sup', rule_template(
            "partitief vorm van de overtreffende trap van %s"))


class ConjunctiveTerm(Term):
    """The term class for conjunctives."""

    @property
    def category_description(self):
        """Return human-readable description of the term category."""
        return pgettext("word category","conjunctive")


class PrepositionTerm(Term):
    """The term class for prepositions."""

    @property
    def category_description(self):
        """Return human-readable description of the term category."""
        return pgettext("word category","preposition")


class AbbreviationTerm(Term):
    """The term class for abbreviations."""

    @property
    def category_description(self):
        """Return human-readable description of the term category."""
        return pgettext("word category","abbreviation")


class AdjectiveTerm(Term):
    """The term class for adjectives."""

    @property
    def category_description(self):
        """Return human-readable description of the term category."""
        return pgettext("word category","adjective")


class AdverbTerm(Term):
    """The term class for adverbs."""

    @property
    def category_description(self):
        """Return human-readable description of the term category."""
        return pgettext("word category","adverb")


class AdverbNumberTerm(Term):
    """The term class for adverbial numbers."""

    @property
    def category_description(self):
        """Return human-readable description of the term category."""
        return pgettext("word category","adverbial number")


class ArticleTerm(Term):
    """The term class for articles."""

    @property
    def category_description(self):
        """Return human-readable description of the term category."""
        return pgettext("word category","article")


class ProperNameTerm(Term):
    """The term class for proper names."""

    @property
    def category_description(self):
        """Return human-readable description of the term category."""
        return pgettext("word category","proper name")


class PronounTerm(Term):
    """The term class for pronouns."""

    @property
    def category_description(self):
        """Return human-readable description of the term category."""
        return pgettext("word category","pronoun")


class DemonstrativePronounTerm(PronounTerm):
    """The term class for demonstrative pronouns."""

    @property
    def category_description(self):
        """Return human-readable description of the term category."""
        return pgettext("word category","demonstrative pronoun")


class ExclaimingPronounTerm(PronounTerm):
    """The term class for exclaming pronouns."""

    @property
    def category_description(self):
        """Return human-readable description of the term category."""
        return pgettext("word category","exclaiming pronoun")


class IndefinitePronounTerm(PronounTerm):
    """The term class for indefinite pronouns."""

    @property
    def category_description(self):
        """Return human-readable description of the term category."""
        return pgettext("word category","indefinite pronoun")


class InterrogativePronounTerm(PronounTerm):
    """The term class for interrogative pronouns."""

    @property
    def category_description(self):
        """Return human-readable description of the term category."""
        return pgettext("word category","interrogative pronoun")


class PersonalPronounTerm(PronounTerm):
    """The term class for personal pronouns."""

    @property
    def category_description(self):
        """Return human-readable description of the term category."""
        return pgettext("word category","personal pronoun")


class PossesivePronounTerm(PronounTerm):
    """The term class for possesive pronouns."""

    @property
    def category_description(self):
        """Return human-readable description of the term category."""
        return pgettext("word category","possesive pronoun")


class ReciprocalPronounTerm(PronounTerm):
    """The term class for reciprocal pronouns."""

    @property
    def category_description(self):
        """Return human-readable description of the term category."""
        return pgettext("word category","reciprocal pronoun")


class ReflexivePronounTerm(PronounTerm):
    """The term class for reflexive pronouns."""

    @property
    def category_description(self):
        """Return human-readable description of the term category."""
        return pgettext("word category","reflexive pronoun")


class RelativePronounTerm(PronounTerm):
    """The term class for relative pronouns."""

    @property
    def category_description(self):
        """Return human-readable description of the term category."""
        return pgettext("word category","relative pronoun")


class NumberTerm(Term):
    """The term class for number."""

    @property
    def category_description(self):
        """Return human-readable description of the term category."""
        return pgettext("word category","number")


class IndefiniteNumeralTerm(Term):
    """The term class for indefinite numerals."""

    @property
    def category_description(self):
        """Return human-readable description of the term category."""
        return pgettext("word category","indefinite numeral")


class InterrogativeNumeralTerm(Term):
    """The term class for interrogative numerals."""

    @property
    def category_description(self):
        """Return human-readable description of the term category."""
        return pgettext("word category","interrogative numeral")


class OrdinalTerm(Term):
    """The term class for ordinals."""

    @property
    def category_description(self):
        """Return human-readable description of the term category."""
        return pgettext("word category","ordinal")


class IndefiniteOrdinalTerm(Term):
    """The term class for indefinite ordinals."""

    @property
    def category_description(self):
        """Return human-readable description of the term category."""
        return pgettext("word category","indefinite ordinal")


class NounTerm(Term):
    """The term class for nouns."""
    # Gender of the term
    _gender = ''
    # single form
    _single = u''
    # plural form
    _plural = u''
    # diminutive form
    _diminutive = u''
    # diminutive plural form
    _diminutive_plural = u''

    @property
    def category_description(self):
        """Return human-readable description of the term category."""
        return pgettext("word category","noun")

    @property
    def gender(self):
        """Return the gender of the noun."""
        return self._gender

    @gender.setter
    def gender(self, value):
        """Set the gender of the noun."""
        self._gender = value

    @property
    def single(self):
        """Return the single form of the noun."""
        return self._single

    @single.setter
    def single(self, value):
        """Set the single form of the noun."""
        self._single = value

    @property
    def plural(self):
        """Return the plural form of the noun."""
        return self._plural

    @plural.setter
    def plural(self, value):
        """Set the plural form of the noun."""
        self._plural = value

    @property
    def diminutive(self):
        """Return the diminutive form of the noun."""
        return self._diminutive

    @diminutive.setter
    def diminutive(self, value):
        """Set the diminutive form of the noun."""
        self._diminutive = value

    @property
    def diminutive_plural(self):
        """Return the diminutive plural form of the noun."""
        return self._diminutive_plural

    @diminutive_plural.setter
    def diminutive_plural(self, value):
        """Set the diminutive plural form of the noun."""
        self._diminutive_plural = value


class VerbTerm(Term):
    """The term class for verbs."""
    _1ps = u''
    _2ps = u''
    _plural = u''
    _past_single = u''
    _past_plural = u''
    _auxiliary = u''
    _past_participle = u''

    @property
    def category_description(self):
        """Return human-readable description of the term category."""
        return pgettext("word category","verb")

    @property
    def first_person_single(self):
        """Return the 1st person single form of the verb."""
        return self._1ps

    @first_person_single.setter
    def first_person_single(self, value):
        """Set the 1st person single form of the verb."""
        self._1ps = value

    @property
    def second_person_single(self):
        """Return the 2st person single form of the verb."""
        return self._2ps

    @second_person_single.setter
    def second_person_single(self, value):
        """Set the 2st person single form of the verb."""
        self._2ps = value

    @property
    def plural(self):
        """Return the plural form of the verb."""
        return self._plural

    @plural.setter
    def plural(self, value):
        """Set the plural form of the verb."""
        self._plural = value

    @property
    def past_single(self):
        """Return the past single form of the verb."""
        return self._past_single

    @past_single.setter
    def past_single(self, value):
        """Set the past single form of the verb."""
        self._past_single = value

    @property
    def past_plural(self):
        """Return the past plural form of the verb."""
        return self._past_plural

    @past_plural.setter
    def past_plural(self, value):
        """Set the past plural form of the verb."""
        self._past_plural = value

    @property
    def auxiliary(self):
        """Return the auxiliary form of the verb."""
        return self._auxiliary

    @auxiliary.setter
    def auxiliary(self, value):
        """Set the auxiliary form of the verb."""
        self._auxiliary = value

    @property
    def past_participle(self):
        """Return the past participle form of the verb."""
        return self._past_participle

    @past_participle.setter
    def past_participle(self, value):
        """Set the past participle form of the verb."""
        self._past_participle = value


class TermSet(object):
    """Collection of all terms within a language."""
    # Language of the terms in this set
    lang = None
    # Sound file containing the pronunciation
    _sound = ''
    # IPA string containing the pronunciation
    _ipa = u''
    # Syllables split up
    _syllables = u''
    # List of terms
    _terms = None

    def __init__(self, lang):
        """
        Supported language codes can be found here:
        https://nl.wiktionary.org/wiki/Categorie:Taalsjablonen

        Keyword arguments
        lang - The language code for this termset.
        """
        self.lang = lang.lower()
        self._terms = []

    @property
    def sound(self):
        """Return the link to the pronunciation sound file."""
        return self._sound

    @sound.setter
    def sound(self, value):
        """Set the link to the pronunciation sound file."""
        self._sound = value

    @property
    def ipa(self):
        """Return the IPA description of the pronunciation."""
        return self._ipa

    @ipa.setter
    def ipa(self, value):
        """Set the IPA description of the pronunciation."""
        self._ipa = value

    @property
    def syllables(self):
        """Return the description of the word in syllables."""
        return self._syllables

    @syllables.setter
    def syllables(self, value):
        """Set the description of the word in syllables."""
        self._syllables = value

    @property
    def terms(self):
        """Return the list of terms containing in this termset."""
        return self._terms

    def add_term(self, term):
        """Add a term to this termset."""
        self._terms.append(term)

    def __repr__(self):
        return '{%s::%s}(%s)' % (self.__class__.__name__, self.lang,
                repr(self._terms))


class WiktionaryParser(object):
    """Parser class that parses raw wikitext"""
    # The word the parsed document is about
    word = None
    # Reference to the WiktionaryAPI instance
    api = None
    # Temporary buffer of lines
    _buff = None
    # List of termsets
    _termsets = None
    # Current termset, if any
    _termset = None
    # Current language, if any
    _lang = None
    # Current term, if any
    _term = None
    # Current header, if any
    _header = None
    # Current header params, if any
    _header_params = None
    # List of parser warnings
    _warnings = None

    def __init__(self, api):
        self.api = api
        self._buff = []
        self._termsets = []
        self._warnings = []
        self._universal_langs = ['universeel', 'translingual']
        self._conjugations_identifier = lambda x: '%s/vervoeging' % (x,)
        self.re_ignore = re.compile(
            (r"^"
                r"(?:<!--.+-->)|"
                r"(?:{{rel-top[0-9]?}})|"
                r"(?:{{rel-mid[0-9]?}})|"
                r"(?:{{rel-bottom[0-9]?}})|"
                r"(?:{{top[0-9]?}})|"
                r"(?:{{mid[0-9]?}})|"
                r"(?:{{bottom}})|"
                r"(?:{{trans-top}})|"
                r"(?:{{trans-mid}})|"
                r"(?:{{trans-bottom}})|"
                r"(?:{{\(\(}})|"
                r"(?:{{\)\)}})|"
                r"(?:{{=}})"
            r"$"))
        self.re_lang = re.compile(r"^{{=(\w+)=}}$")
        self.re_template = re.compile(r"^{{([^|]+)(?:\|(.+))?}}$")
        self.re_pipelist = re.compile(r"((?:{{[^}]+\|[^}]+}})|[^|]+)")
        self.re_header = re.compile(r"^{{-([\w-]+)-(?:\|(.+))?}}$")
        self.re_pron_sound = re.compile(r"^\*{{sound}}: {{audio\|(.+)\|.+}}$")
        self.re_pron_ipa = re.compile(r"^\*{{WikiW\|IPA}}: {{IPA\|/(.+)/.*$")
        self.re_syll = re.compile(r"^\*(.+)$")
        self.re_nlnoun = re.compile(r"^([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)$")
        self.re_form = re.compile(r"^{{([^|]+)\|([^|]+).*}}$")
        self.re_meaning_entry = re.compile(
                r"^(?:\[[A-Z]\] )?'''(.+)''' ?(.+)?$")
        self.re_meaning_def = re.compile(r"^#(.+)$")
        self.re_meaning_eg = re.compile(r"^{{bijv-1\|(.+)}}$")
        self.re_syn_ref = re.compile(r"^\*\[([0-9]+)\]:? (.+)$")
        self.re_syn_list = re.compile(r"\[\[([^]]+)\]\]")
        self.re_ant_ref = re.compile(r"^\*\[([0-9]+)\]:? (.+)$")
        self.re_ant_list = re.compile(r"\[\[([^]]+)\]\]")
        self.re_hypo = re.compile(r"^\*\[\[(.+)\]\]$")
#        self.header_classes = {
#            'art': ArticleTerm,
#            'conj': ConjunctiveTerm,
#        }

    def _warn(self, warning, line=None):
        """Add a warning string to the list of warnings."""
        if line is None:
            self._warnings.append("%s" % (warning,))
        else:
            self._warnings.append("%s in \"%s\"" % (warning, line))

    @property
    def warnings(self):
        """Get the list of warnings."""
        return self._warnings

    def parse(self, lines, word=None, languages='*'):
        """Parse the provided wikitext.

        Keyword arguments:
        lines - The wikitext to parse, either one string or a list of lines.
        word - The word this wikitext is about. (Default None)
        languages - A list of languages it should return or '*'. (Default '*')
        """
        self.word = word
        self._termsets = []
        if isinstance(lines, str) or isinstance(lines, unicode):
            lines = lines.split("\n")
        for line in lines:
            if word is not None:
                line = line.strip().replace("{{pn}}", word)
            else:
                line = line.strip()
            # Test for an empty line, which should close a header
            if line == "":
                if self._header is not None:
                    # Finish parsing current header
                    self._trigger_header_parse()
                    # Clear buffer
                    self._buff = []
                    # Clear header and header params
                    self._header = self._header_params = None
                else:
                    self._warn("Unexpected empty line without a current header")
                continue
            # Test if line should be ignored
            if re.search(self.re_ignore, line):
                continue
            # Test for new language template
            lang_match = re.search(self.re_lang, line)
            if lang_match:
                # If there was a current termset
                if self._termset is not None:
                    # If there was a current header
                    if self._header is not None:
                        # Finish parsing current header
                        self._trigger_header_parse()
                        # Clear buffer
                        self._buff = []
                        # Clear header and header params
                        self._header = self._header_params = None
                    # Add current term to list of terms
                    self._termsets.append(self._termset)
                # Create new termset for found language
                self._termset = TermSet(lang_match.group(1))
                # Clear reference to current term
                self._term = None
                continue
            # If there is no current term either, skip line
            if self._termset is None:
                self._warn("Expecting language line", line)

            # Test for new header template
            header_match = re.search(self.re_header, line)
            if header_match:
                # If there is no current termset, assume universal language
                if self._termset is None:
                    self._termset = TermSet(self._universal_langs[0])
                # If there was a current header
                if self._header is not None:
                    # Finish parsing current header
                    self._trigger_header_parse()
                    # Clear buffer
                    self._buff = []
                # Set new current header and header params
                self._header, self._header_params = header_match.groups()
                continue

            # If not language or header line, but header exists: save to buffer
            if self._header:
                self._buff.append(line)

        # Finish pending termset
        if self._termset is not None:
            # Finish a pending header
            if self._header is not None:
                # Finish parsing current header
                self._trigger_header_parse()
                # Clear buffer
                self._buff = []
            # Add current term to list of terms
            self._termsets.append(self._termset)

        # Cleanup
        self._buff = []
        self._termset = self._term = None
        self._header = self._header_params = None
        # Return found terms
        if languages == '*':
            return self._termsets
        else:
            return [x for x in self._termsets if x.lang in languages or
                    x.lang in self._universal_langs]

    def _add_term(self, term):
        """Add term to the current termset."""
        self._term = term
        self._termset.add_term(self._term)
        return self._term

    def _ensure_term(self, cls):
        """Ensure the current term is of the right type."""
        if not isinstance(self._term, cls):
            self._term = cls()
            self._termset.add_term(self._term)
        return self._term

    def _trigger_header_parse(self):
        """Trigger the right header parse function."""
        if self._header == 'pron':
            self._parse_pronunciation()
        elif self._header == 'syll':
            self._parse_syllables()
        elif self._header == 'syn':
            self._parse_synonyms()
        elif self._header == 'ant':
            self._parse_antonyms()
        elif self._header == 'hypo':
            self._parse_hyponyms()
        elif self._header == 'nlnoun':
            self._parse_nlnoun()
        elif self._header == 'noun':
            if self._header_params == "0":
                self._parse_form(NounTermForm)
            else:
                self._parse_meaning(NounTerm)
        elif self._header == 'nlverb':
            self._parse_nlverb()
        elif self._header == 'nlstam':
            self._parse_nlstam()
        elif self._header == 'prcp':
            self._parse_form(VerbTermForm)
        elif self._header == 'verb':
            if self._header_params == "0":
                self._parse_form(VerbTermForm)
            else:
                self._parse_meaning(VerbTerm)
        elif self._header == 'abbr':
            self._parse_meaning(AbbreviationTerm)
        elif self._header == 'adverb':
            self._parse_meaning(AdverbTerm)
        elif self._header == 'adjc':
            if self._header_params == "0":
                self._parse_adjective_form()
            else:
                self._parse_meaning(AdjectiveTerm)
        elif self._header == 'art':
            self._parse_meaning(ArticleTerm)
        elif self._header == 'conj':
            self._parse_meaning(ConjunctiveTerm)
        elif self._header in ('cijfer', 'num'):
            self._parse_meaning(NumberTerm)
        elif self._header == 'name':
            self._parse_meaning(ProperNameTerm)
        elif self._header == 'num-indef':
            self._parse_meaning(IndefiniteNumeralTerm)
        elif self._header == 'num-int':
            self._parse_meaning(InterrogativeNumeralTerm)
        elif self._header == 'ordn':
            self._parse_meaning(OrdinalTerm)
        elif self._header == 'ordn_indef':
            self._parse_meaning(IndefiniteOrdinalTerm)
        elif self._header == 'prep':
            self._parse_meaning(PrepositionTerm)
        elif self._header == 'pronoun':
            self._parse_meaning(PronounTerm)
        elif self._header == 'pronom-dem':
            self._parse_meaning(DemonstrativePronounTerm)
        elif self._header == 'pronom-excl':
            self._parse_meaning(ExclaimingPronounTerm)
        elif self._header == 'pronom-indef':
            self._parse_meaning(IndefinitePronounTerm)
        elif self._header == 'pronom-int':
            self._parse_meaning(InterrogativePronounTerm)
        elif self._header == 'pronom-pers':
            self._parse_meaning(PersonalPronounTerm)
        elif self._header == 'pronom-pos':
            self._parse_meaning(PossesivePronounTerm)
        elif self._header == 'pronom-rec':
            self._parse_meaning(ReciprocalPronounTerm)
        elif self._header == 'pronom-refl':
            self._parse_meaning(ReflexivePronounTerm)
        elif self._header == 'pronom-rel':
            self._parse_meaning(RelativePronounTerm)
        else:
            self._warn("Unsupported header '%s'" % (self._header,))

    def _parse_pronunciation(self):
        """Parse info under the pronunciation header."""
        for line in self._buff:
            # Test for sound line
            sound_match = re.search(self.re_pron_sound, line)
            # Test for IPA line
            ipa_match = re.search(self.re_pron_ipa, line)
            if sound_match:
                # Store sound file in term
                self._termset.sound = sound_match.group(1)
            elif ipa_match:
                # Store IPA description in term
                self._termset.ipa = ipa_match.group(1)
            else:
                self._warn("Unexpected pronunciation line", line)

    def _parse_syllables(self):
        """Parse info under the syllables header."""
        for line in self._buff:
            match = re.search(self.re_syll, line)
            if match:
                self._termset.syllables = match.group(1)
                return
            else:
                self._warn("Unexpected syllable line", line)

    def _parse_form(self, termcls):
        """Parse info under the form of ... header."""
        # Check the size of the buffer
        if not self._buff:
            self._warn("No buffer found to parse form from", self._header)
            return
        elif len(self._buff) > 1:
            self._warn("Unexpected extra buffer content", self._buff[1])

        # Match the form line
        form_match = re.search(self.re_form, self._buff[0])
        if form_match:
            form, main_term = form_match.groups()
        else:
            self._warn("Unexpected form line", self._buff[0])
            return
        try:
            # Create term of the given class with the parsed form
            term = termcls(main_term=main_term, form=form)
        except ValueError as err:
            self._warn(err, form)
            return
        else:
            self._add_term(term)

    def _parse_adjective_form(self):
        """Parse info under the adjective form header."""
        # Check the size of the buffer
        if not self._buff:
            self._warn("No buffer found to parse adjective form from",
                    self._header)
            return
        elif len(self._buff) > 1:
            self._warn("Unexpected extra buffer content", self._buff[1])
            return
        # Match the form line
        template_match = re.search(self.re_template, self._buff[0])
        if template_match:
            template, params = template_match.groups()
            if template == "nl-adjc-form":
                adjc_forms = re.findall(self.re_pipelist, params)
                if adjc_forms:
                    self._add_term(AdjectiveTermForm(adjc_forms[0],
                        "%s-%s" % (adjc_forms[1], adjc_forms[2])))
                else:
                    self._warn("Unexpected adjective form line", self._buff[0])
            else:
                self._warn("Unexpected adjective form line", self._buff[0])
        else:
            self._warn("Unexpected adjective form line", self._buff[0])

    def _parse_nlnoun(self):
        """Parse info under the nlnoun header."""
        # Create new current term
        term = self._ensure_term(NounTerm)
        # Match different forms of the noun
        nlnoun_match = re.search(self.re_nlnoun, self._header_params)
        if nlnoun_match:
            term.single = nlnoun_match.group(1)
            term.plural = nlnoun_match.group(2)
            term.diminutive = nlnoun_match.group(3)
            term.diminutive_plural = nlnoun_match.group(4)
        else:
            self._warn("Unexpected nlnoun params", self._header_params)

        if self._buff:
            self._warn("Unexpected buffer content for nlnoun")

    def _parse_nlverb(self):
        """Parse info under the nlverb header."""
        # Create new current term
        term = self._ensure_term(VerbTerm)
        # Match different forms of the verb
        conj_list = re.findall(self.re_pipelist, self._header_params)
        if len(conj_list) > 7:
            term.first_person_single = conj_list[1]
            term.second_person_single = conj_list[2]
            term.plural = conj_list[3]
            term.past_single = conj_list[4]
            term.past_plural = conj_list[5]
            term.auxiliary = conj_list[6]
            term.past_participle = conj_list[7]
        else:
            self._warn("Unexpected nlverb line", self.header_params)

        if self._buff:
            self._warn("Unexpected buffer content for nlverb")

    def _parse_nlstam(self):
        """Parse info under the nlstam header."""
        # Create new current term
        term = self._ensure_term(VerbTerm)
        # Create separate parser
        inner_parser = self.api.create_parser()
        # Attempt to fetch extended conjugations list
        wiki_conjugations = self.api.get_info(
                self._conjugations_identifier(self.word), inner_parser)
        conj_terms = filter(lambda x: isinstance(x, VerbTerm), wiki_conjugations)
        if len(conj_terms) > 0:
            term.first_person_single = conj_terms[0].first_person_single
            term.second_person_single = conj_terms[0].second_person_single
            term.plural = conj_terms[0].plural
            term.past_single = conj_terms[0].past_single
            term.past_plural = conj_terms[0].past_plural
            term.auxiliary = conj_terms[0].auxiliary
            term.past_participle = conj_terms[0].past_participle
        else:
            self._warn("No extended conjugations available for %s" %
                    (self.word,))
            # Match different forms of the verb
            nlstam_list = re.findall(self.re_pipelist, self._header_params)
            if len(nlstam_list) > 2:
                term.past_single = nlstam_list[1]
                term.past_participle = nlstam_list[2]
            else:
                self._warn("Unexpected nlstam line", self._header_params)

        if self._buff:
            self._warn("Unexpected buffer content for nlstam")

    def _parse_meaning(self, termcls):
        """Parse info under the meaning header."""
        if isinstance(self._term, TermForm):
            self._warn("Meaning found for term form, which is not supported.")
            return
        meaning = None
        # Create new current term
        term = self._ensure_term(termcls)
        for line in self._buff:
            # Test for dictionary entry
            entry_match = re.search(self.re_meaning_entry, line)
            if entry_match:
                entry, gender = entry_match.groups()
                term.entry = entry
                if gender is not None:
                    term.gender = gender
            # Test for definition
            def_match = re.search(self.re_meaning_def, line)
            if def_match:
                if meaning is not None:
                    term.add_meaning(meaning)
                meaning = Meaning(definition=def_match.group(1))
            # Test for example sentences
            eg_match = re.search(self.re_meaning_eg, line)
            if eg_match:
                # If example is not linked to a meaning, skip.
                if meaning is None:
                    self._warn('Example sentence without a meaning', line)
                    continue
                else:
                    # At the example sentence to the current meaning
                    meaning.example = eg_match.group(1)
        if meaning is not None:
            term.add_meaning(meaning)

    def _parse_synonyms(self):
        """Parse info under the synonyms header."""
        if self._term is None:
            self._warn("Synonyms found without current term")
            return
        elif isinstance(self._term, TermForm):
            self._warn("Synonyms found for term form, which is not supported.")
            return

        for line in self._buff:
            ref_match = re.search(self.re_syn_ref, line)
            if ref_match:
                ref, syn_list = ref_match.groups()
                try:
                    meaning = self._term.meanings[int(ref)-1]
                except ValueError:
                    self._warn("Synonym reference is not a number", line)
                    continue
                except IndexError:
                    self._warn("Synonym reference does not match a definition",
                            line)
                    continue
                else:
                    meaning.synonyms = re.findall(self.re_syn_list, syn_list)
            else:
                self._warn('Unexpected synonym line', line)

    def _parse_antonyms(self):
        """Parse info under the antonyms header."""
        if self._term is None:
            self._warn("Antonyms found without current term")
            return
        elif isinstance(self._term, TermForm):
            self._warn("Antonyms found for term form, which is not supported.")
            return

        for line in self._buff:
            ref_match = re.search(self.re_ant_ref, line)
            if ref_match:
                ref, ant_list = ref_match.groups()
                try:
                    meaning = self._term.meanings[int(ref)-1]
                except ValueError:
                    self._warn("Antonym reference is not a number", line)
                    continue
                except IndexError:
                    self._warn("Antonym reference does not match a definition",
                            line)
                    continue
                else:
                    meaning.antonyms = re.findall(self.re_ant_list, ant_list)
            else:
                self._warn('Unexpected antonym line', line)

    def _parse_hyponyms(self):
        """Parse info under the hyponyms header."""
        if self._term is None:
            self._warn("Hyponyms found without current term")
            return
        elif isinstance(self._term, TermForm):
            self._warn("Hyponyms found for term form, which is not supported.")
            return

        for line in self._buff:
            hypo_match = re.search(self.re_hypo, line)
            if hypo_match:
                self._term.add_hyponym(hypo_match.group(1))
            else:
                self._warn("Unexpected hyponym line", line)
                continue

    @staticmethod
    def clean_wikitext(text, convert_template_fn=None,
            convert_link_fn=None):
        """Clean wikitext occurences from text.
        Templates and links are replaced from the provided text. If a function
        is provided for replacing template and/or link occurences, then that
        function will be called for each occurence. Default behavior is
        removing all templates entirely and replacing each link with the word
        in plain text.

        Keyword arguments:
        text - The text that should be cleaned.
        convert_template_fn - A function that returns the replacement for each
                              occurence of a wikitext template (Default None)
        convert_link_fn - A function that returns the replacement for each
                          occurence of a wikitext link (Default None)
        """
        # Convert template occurences
        if convert_template_fn is None:
            text = re.sub(r'{{[^}]+}}', '', text)
        else:
            text = re.sub(r'{{[^}]+}}', convert_template_fn, text)
        # Convert link occurences
        if convert_link_fn is None:
            text = re.sub(r'\[\[([^]]+)\]\]', '\g<1>', text)
        else:
            text = re.sub(r'\[\[[^]]+\]\]', convert_link_fn, text)
        # Remove any whitespace or interpunction at the beginning of the text
        text = text.lstrip(whitespace+"!#$%&*+,-./:;<=>?@\\^_`|})~")
        text = text.replace("()", "").replace("[]","").replace("{}","")
        return text


class WiktionaryAPI(MediaWikiAPI):
    """Main WiktionaryAPI entry point."""
    _termsets = None
    _languages = None
    _parser = None
    def __init__(self, lang=None, base_url=None, languages='*', parser=None,
            **kwargs):
        """
        Settings:
        The lang parameter can also be set by the CONTENT_WIKTIONARY_LANG
        setting. If this is not set and the parameter value is also not
        provided as keyword argument, then the default value of the
        MediaWikiAPI will be used. The base_url parameter can also be set by the
        CONTENT_WIKTIONARY_API_URL setting.

        A base_url should contain one string wildcard ("%s"), where the
        language code of the site can be inserted.

        Keyword arguments:
        lang - Which language of wiktionary to use. (Default: MediaWikiAPI)
        base_url - Which url to use. (Default '%s.wiktionary.org/w/api.php')
        languages - A list of languages it should return or '*'. (Default '*')
        parser - The parse to use. (Default WiktionaryParser())
        """
        if lang is None and hasattr(settings, "CONTENT_WIKTIONARY_LANG"):
            lang = settings.CONTENT_WIKTIONARY_LANG

        if base_url is None:
            if hasattr(settings, "CONTENT_WIKTIONARY_API_URL"):
                base_url = settings.CONTENT_WIKTIONARY_API_URL
            else:
                base_url = 'http://%s.wiktionary.org/w/api.php'
            if base_url[0] != 'h':
                base_url = 'http://%s' % (base_url,)

        super(WiktionaryAPI, self).__init__(lang, base_url, **kwargs)
        self._parser = self.create_parser() if parser is None else parser
        self._languages = languages
        self._termsets = {}

    def create_parser(self):
        return WiktionaryParser(api=self)

    def _load(self, word, parser):
        """Retrieve wikitext about the word or load from cache."""
        if word not in self._termsets:
            wikitext = self.get_page_wikitext(word)
            if wikitext is not None:
                self._termsets[word] = parser.parse(lines=wikitext,
                        word=word, languages=self._languages)
            else:
                return None
        return self._termsets[word]

    def get_info(self, word, parser=None):
        """Return termsets contained in the wikitext about the word.
        When the list of languages provided at initialization only covers one
        language, the terms of the only termset are directly returned. If no
        information about the word could be retrieved, the empty list is
        returned.

        Keyword arguments:
        word - The word about which you want the information.
        """
        parser = parser if parser is not None else self._parser
        termsets = self._load(word, parser)
        if not termsets:
            return []
        else:
            if isinstance(self._languages, list) and len(self._languages) == 1:
                return termsets[0].terms
            else:
                return termsets

    @property
    def parser_warnings(self):
        """Return the warnings collected during parsing."""
        return self._parser.warnings
