"""Wiktionary API.
Known issues:
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
        self._definition = definition
        self._example = example
        self._synonyms = [] if synonyms is None else synonyms
        self._antonyms = [] if antonyms is None else antonyms

    @property
    def definition(self):
        return self._definition

    @definition.setter
    def definition(self, value):
        self._definition = value

    @property
    def example(self):
        return self._example

    @example.setter
    def example(self, value):
        self._example = value

    @property
    def synonyms(self):
        return self._synonyms

    @synonyms.setter
    def synonyms(self, value):
        self._synonyms = value

    @property
    def antonyms(self):
        return self._antonyms

    @antonyms.setter
    def antonyms(self, value):
        self._antonyms = value

    def __repr__(self):
        return '%s("%s...")' % (self.__class__.__name__, self._definition[:20])


class Term(object):
    """Base class for a term.
    In a language a word may exist in multiple categories, e.g. verb and noun.
    For each of these, a separate term is used. Within a category, e.g. noun, a
    word can still have multiple meanings (e.g. bank). These meanings are
    are represented by a Meaning object and linked to this term.
    """
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
        return self._entry

    @entry.setter
    def entry(self, value):
        self._entry = value

    @property
    def meanings(self):
        return self._meanings

    def add_meaning(self, meaning):
        self._meanings.append(meaning)

    @property
    def hyponyms(self):
        return self._hyponyms

    def add_hyponym(self, hyponym):
        self._hyponyms.append(hyponym)

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self._entry)


class TermForm(object):
    """Base class for terms that are a specific variant of a main term"""
    # The main term
    _main_term = None
    # The provided form type
    _form = None

    def __init__(self, main_term, form):
        self._main_term = main_term
        self._form = form

    @property
    def main_term(self):
        return self._main_term

    @property
    def form(self):
        return self._form

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self._main_term)

class NounTermForm(TermForm):
    _plural = False
    _diminutive = False
    _diminutive_plural = False

    def __init__(self, main_term, form):
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
    """The term class for nouns"""
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
        return self._gender

    @gender.setter
    def gender(self, value):
        self._gender = value

    @property
    def single(self):
        return self._single

    @single.setter
    def single(self, value):
        self._single = value

    @property
    def plural(self):
        return self._plural

    @plural.setter
    def plural(self, value):
        self._plural = value

    @property
    def diminutive(self):
        return self._diminutive

    @diminutive.setter
    def diminutive(self, value):
        self._diminutive = value

    @property
    def diminutive_plural(self):
        return self._diminutive_plural

    @diminutive_plural.setter
    def diminutive_plural(self, value):
        self._diminutive_plural = value


class VerbTerm(Term):
    _past_tense = u''
    _past_participle_tense = u''

    @property
    def past_tense(self):
        return self._past_tense

    @past_tense.setter
    def past_tense(self, value):
        self._past_tense = value

    @property
    def past_participle_tense(self):
        return self._past_participle_tense

    @past_participle_tense.setter
    def past_participle_tense(self, value):
        self._past_participle_tense = value


class TermSet(object):
    """Collection of all terms within a language"""
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
        self.lang = lang
        self._terms = []

    @property
    def sound(self):
        return self._sound

    @sound.setter
    def sound(self, value):
        self._sound = value

    @property
    def ipa(self):
        return self._ipa

    @ipa.setter
    def ipa(self, value):
        self._ipa = value

    @property
    def syllables(self):
        return self._syllables

    @syllables.setter
    def syllables(self, value):
        self._syllables = value

    @property
    def terms(self):
        return self._terms

    def add_term(self, term):
        self._terms.append(term)

    def __repr__(self):
        return '{%s::%s}(%s)' % (self.__class__.__name__, self.lang,
                repr(self._terms))


class WiktionaryParser(object):
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
        if line is None:
            self._warnings.append("%s" % (warning,))
        else:
            self._warnings.append("%s in \"%s\"" % (warning, line))

    @property
    def warnings(self):
        return self._warnings

    def parse(self, lines, word=None, languages='*'):
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
        self._term = term
        self._termset.add_term(self._term)
        return self._term

    def _ensure_term(self, cls):
        """Ensure the current term is of the right type"""
        if not isinstance(self._term, cls):
            self._term = cls()
            self._termset.add_term(self._term)
        return self._term

    def _trigger_header_parse(self):
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
        for line in self._buff:
            match = re.search(self.re_syll, line)
            if match:
                self._termset.syllables = match.group(1)
                return
            else:
                self._warn("Unexpected syllable line", line)

    def _parse_form(self, termcls):
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
    _termsets = None
    _languages = None
    _parser = None

    def __init__(self, lang=None, base_url=None, languages='*', parser=None,
            **kwargs):
        if lang is None and hasattr(settings, "CONTENT_WIKTIONARY_LANG"):
            lang = settings.CONTENT_WIKTIONARY_LANG

        if base_url is None:
            if hasattr(settings, "CONTENT_WIKTIONARY_API_URL"):
                base_url = settings.CONTENT_WIKTIONARY_API_URL
            else:
                base_url = 'http://%s.wiktionary.org/w/api.php'

        super(WiktionaryAPI, self).__init__(lang, base_url, **kwargs)

        self._parser = WiktionaryParser() if parser is None else parser
        self._languages = languages
        self._termsets = {}

    def _load(self, word):
        if word not in self._termsets:
            wikitext = self.get_page_wikitext(word)
            self._termsets[word] = self._parser.parse(lines=wikitext,
                    word=word, languages=self._languages)
        return self._termsets[word]

    def get_terms(self, word):
        termsets = self._load(word)
        if isinstance(self._languages, list) and len(self._languages) == 1:
            return termsets[0].terms
        else:
            return termsets

    @property
    def parser_warnings(self):
        return self._parser.warnings
