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
    * Does not support other lexical categories than nouns and verbs
    * Does not support different conjugations per meaning of a term
    * Does not support different antonyms per meaning
    * Does not support stress homographs
"""
import re
from django.conf import settings
from readmore.content.thirdparty.wiki_api import MediaWikiAPI

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

    def __init__(self, main_term, form):
        """
        Keyword arguments:
        main_term - The word of which this is a form.
        form - The name of which form this is.
        """
        self._main_term = main_term
        self._form = form

    @property
    def main_term(self):
        """Return the main term of which is a form."""
        return self._main_term

    @property
    def form(self):
        """Return which form of the main term this is."""
        return self._form

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self._main_term)

class NounTermForm(TermForm):
    _plural = False
    _diminutive = False
    _diminutive_plural = False

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
        super(NounTermForm, self).__init__(main_term, form)
        if form == 'noun-pl':
            self._plural = True
        elif form == "noun-dim":
            self._diminutive = True
        elif form == "noun-dim-pl":
            self._diminutive_plural = True
        else:
            raise ValueError("Unsupported form type")

    @property
    def is_plural(self):
        return self._plural

    @property
    def is_diminutive(self):
        return self._diminutive

    @property
    def is_diminutive_plural(self):
        return self._diminutive_plural

class VerbTermForm(TermForm):
    # Present 1st person single
    _present_1ps = False
    # Present 2nd person single
    _present_2ps = False
    # Present 1st/2nd/3rd person single
    _present_tps = False
    # Subjunctive
    _subjunctive = False
    # Present participle
    _present_participle = False
    # Past participle
    _past_participle = False
    # Present 'Thou ..'
    _present_thou = False
    # Present plural
    _present_plural = False
    # Present impersonal
    _present_impersonal = False
    # Past single
    _past_single = False
    # Past 'Thou ...'
    _past_thou = False
    # Past plural
    _past_plural = False
    # Past impersonal
    _past_impersonal = False

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
        super(VerbTermForm, self).__init__(main_term, form)
        if form in ['1ps', '1ps-ij', '1ps-bijz']:
            self._present_1ps = True
        elif form in ['2ps', '2ps-ij', '2ps-bijz']:
            self._present_2ps = True
        elif form in ['tps', 'tps-bijz']:
            self._present_tps = True
        elif form == 'aanv-w' or form == 'aanv-w-bijz':
            self._subjunctive = True
        elif form in ['nl-prcp', 'volt-d']:
            self._past_participle = True
        elif form == 'onv-d':
            self._present_participle = True
        elif form == 'ott-gij':
            self._present_thou = True
        elif form == 'ott-mv':
            self._present_plural = True
        elif form == 'ott-onp':
            self._present_impersonal = True
        elif form in ['ovt-enk', 'ovt-enk-bijz']:
            self._past_single = True
        elif form in ['ovt-gij', 'ovt-gij-bijz']:
            self._past_thou = True
        elif form in ['ovt-mv', 'ovt-mv-bijz']:
            self._past_plural = True
        elif form == 'ovt-onp':
            self._past_impersonal = True
        else:
            raise ValueError("Unsupported form type")

    @property
    def is_present_1ps(self):
        return self._present_1ps

    @property
    def is_present_2ps(self):
        return self._present_2ps

    @property
    def is_present_tps(self):
        return self._present_tps

    @property
    def is_subjunctive(self):
        return self._subjunctive

    @property
    def is_past_participle(self):
        return self._past_participle

    @property
    def is_present_participle(self):
        return self._present_participle

    @property
    def is_present_thou(self):
        return self._present_thou

    @property
    def is_present_plural(self):
        return self._present_plural

    @property
    def is_present_impersonal(self):
        return self._present_impersonal

    @property
    def is_past_single(self):
        return self._past_single

    @property
    def is_past_thou(self):
        return self._past_thou

    @property
    def is_past_plural(self):
        return self._past_plural

    @property
    def is_past_impersonal(self):
        return self._past_impersonal



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
    _past_tense = u''
    _past_participle_tense = u''

    @property
    def past_tense(self):
        """Return the past tense form of the noun."""
        return self._past_tense

    @past_tense.setter
    def past_tense(self, value):
        """Set the past tense form of the noun."""
        self._past_tense = value

    @property
    def past_participle_tense(self):
        """Return the past participle tense form of the noun."""
        return self._past_participle_tense

    @past_participle_tense.setter
    def past_participle_tense(self, value):
        """Set the past participle tense form of the noun."""
        self._past_participle_tense = value


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
        self.lang = lang
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

    def __init__(self):
        self._buff = []
        self._termsets = []
        self._warnings = []
        self.re_ignore = re.compile(
            ("^"
                "(?:<!--.+-->)|"
                "(?:{{rel-top[0-9]?}})|"
                "(?:{{rel-mid[0-9]?}})|"
                "(?:{{rel-bottom[0-9]?}})|"
                "(?:{{top[0-9]?}})|"
                "(?:{{mid[0-9]?}})|"
                "(?:{{bottom}})|"
                "(?:{{trans-top}})|"
                "(?:{{trans-mid}})|"
                "(?:{{trans-bottom}})|"
                "(?:{{\(\(}})|"
                "(?:{{\)\)}})|"
                "(?:{{=}})"
            "$"))
        self.re_lang = re.compile("^{{=(\w+)=}}$")
        self.re_header = re.compile("^{{-(\w+)-\|?(.+)?}}$")
        self.re_pron_sound = re.compile("^\*{{sound}}: {{audio\|(.+)\|.+}}$")
        self.re_pron_ipa = re.compile("^\*{{WikiW\|IPA}}: {{IPA\|/(.+)/.*$")
        self.re_syll = re.compile("^\*(.+)$")
        self.re_nlnoun = re.compile("^([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)$")
        self.re_nlstam = re.compile("([^|]+)")
        self.re_form = re.compile("^{{([^|]+)\|(.+)}}$")
        self.re_meaning_entry = re.compile("^(?:\[[A-Z]\] )?'''(.+)''' ?(.+)?$")
        self.re_meaning_def = re.compile("^#(.+)$")
        self.re_meaning_eg = re.compile("^{{bijv-1\|(.+)}}$")
        self.re_syn_ref = re.compile("^\*\[([0-9]+)\]:? (.+)$")
        self.re_syn_list = re.compile("\[\[([^]]+)\]\]")
        self.re_ant_ref = re.compile("^\*\[([0-9]+)\]:? (.+)$")
        self.re_ant_list = re.compile("\[\[([^]]+)\]\]")
        self.re_hypo = re.compile("^\*\[\[(.+)\]\]$")

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
                continue

            # Test for new header template
            header_match = re.search(self.re_header, line)
            if header_match:
                # If there was a current header
                if self._header is not None:
                    # Finish parsing current header
                    self._trigger_header_parse()
                    # Clear buffer
                    self._buff = []
                # Set new current header and header params
                self._header, self._header_params = header_match.groups()
                continue

            # If not language or header line, save to buffer.
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
            return filter(lambda x: x.lang in languages, self._termsets)

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
        elif self._header == 'nlnoun':
            self._parse_nlnoun()
        elif self._header == 'noun':
            if self._header_params == "0":
                self._parse_form(NounTermForm)
            else:
                self._parse_meaning(NounTerm)
        elif self._header == 'nlstam':
            self._parse_nlstam()
        elif self._header == 'verb':
            if self._header_params == "0":
                self._parse_form(VerbTermForm)
            else:
                self._parse_meaning(VerbTerm)
        elif self._header == 'syn':
            self._parse_synonyms()
        elif self._header == 'ant':
            self._parse_antonyms()
        elif self._header == 'hypo':
            self._parse_hyponyms()
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
        except ValueError as e:
            self._warn(e, form)
            return
        else:
            self._add_term(term)

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

    def _parse_nlstam(self):
        """Parse info under the nlstam header."""
        # Create new current term
        term = self._ensure_term(VerbTerm)
        # Match different forms of the verb
        nlstam_list = re.findall(self.re_nlstam, self._header_params)
        if len(nlstam_list) > 2:
            term.past_tense = nlstam_list[1]
            term.past_participle_tense = nlstam_list[2]
        else:
            self._warn("Unexpected nlstam line", self._header_params)

        if self._buff:
            self._warn("Unexpected buffer content for nlstam")

    def _parse_meaning(self, termcls):
        """Parse info under the meaning header."""
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
                    meaning.synonyms = re.findall(self.re_syn_list, line)
            else:
                self._warn('Unexpected synonym line', line)

    def _parse_antonyms(self):
        """Parse info under the antonyms header."""
        if self._term is None:
            self._warn("Antonyms found without current term")
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
                    meaning.antonyms = re.findall(self.re_ant_list, line)
            else:
                self._warn('Unexpected antonym line', line)

    def _parse_hyponyms(self):
        """Parse info under the hyponyms header."""
        if self._term is None:
            self._warn("Hyponyms found without current term")
            return

        for line in self._buff:
            hypo_match = re.search(self.re_hypo, line)
            if hypo_match:
                self._term.add_hyponym(hypo_match.group(1))
            else:
                self._warn("Unexpected hyponym line", line)
                continue


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

        self._parser = WiktionaryParser() if parser is None else parser
        self._languages = languages
        self._termsets = {}

    def _load(self, word):
        """Retrieve wikitext about the word or load from cache."""
        if word not in self._termsets:
            wikitext = self.get_page_wikitext(word)
            self._termsets[word] = self._parser.parse(lines=wikitext,
                    word=word, languages=self._languages)
        return self._termsets[word]

    def get_info(self, word):
        """Return termsets contained in the wikitext about the word.
        When the list of languages provided at initialization only covers one
        language, the terms of the only termset are directly returned.

        Keyword arguments:
        word - The word about which you want the information.
        """
        termsets = self._load(word)
        if isinstance(self._languages, list) and len(self._languages) == 1:
            return termsets[0].terms
        else:
            return termsets

    @property
    def parser_warnings(self):
        """Return the warnings collected during parsing."""
        return self._parser.warnings
