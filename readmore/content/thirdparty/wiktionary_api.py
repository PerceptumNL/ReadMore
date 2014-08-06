"""Wiktionary API.
Known issues:
    * Does not support different conjugations per meaning of a term
    * Does not support different antonyms per meaning
    * Does not support stress homographs
"""
import re

class Meaning:
    """Representation of a particular meaning of a term."""
    _definition = u''
    _example = u''
    _synonyms = None

    def __init__(self, definition=u'', example=u'', synonyms=None):
        self._definition = definition
        self._example = example
        self._synonyms = [] if synonyms is None else synonyms

    def definition(self, value=None):
        if value is None:
            return self._definition
        else:
            self._definition = value

    def example(self, value=None):
        if value is None:
            return self._example
        else:
            self._example = value

    def synonyms(self, value=None):
        if value is None:
            return self._synonyms
        else:
            self._synonyms = value


class Term:
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

    def entry(self, value=None):
        if value is None:
            return self._entry
        else:
            self._entry = value

    def add_meaning(self, meaning):
        self._meanings.append(meaning)

    def meanings(self):
        return self._meanings

    def add_hyponym(self, hyponym):
        self._hyponyms.append(hyponym)

    def hyponyms(self):
        return self._hyponyms


class TermForm:
    """Base class for terms that are a specific variant of a main term"""
    # The main term
    _main_term = None

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

    def gender(self, value=None):
        if value is None:
            return self._gender
        else:
            self._gender = value

    def single_form(self, value=None):
        if value is None:
            return self._single
        else:
            self._single = value

    def plural_form(self, value=None):
        if value is None:
            return self._plural
        else:
            self._plural = value

    def diminutive_form(self, value=None):
        if value is None:
            return self._diminutive
        else:
            self._diminutive = value

    def diminutive_plural_form(self, value=None):
        if value is None:
            return self._diminutive_plural
        else:
            self._diminutive_plural = value

class VerbTerm(Term):
    _past_tense = u''
    _past_participle_tense = u''

    def past_tense(self, value=None):
        if value is None:
            return self._past_tense
        else:
            self._past_tense = value

    def past_participle_tense(self, value=None):
        if value is None:
            return self._past_participle_tense
        else:
            self._past_participle_tense = value

class TermSet:
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

    def sound(self, value=None):
        if value is None:
            return self._sound
        else:
            self._sound = value

    def ipa(self, value=None):
        if value is None:
            return self._ipa
        else:
            self._ipa = value

    def syllables(self, value=None):
        if value is None:
            return self._syllables
        else:
            self._syllables = value

    def add_term(self, term):
        self._terms.append(term)

    def terms(self):
        return self._terms


class WiktionaryParser:
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

    def __init__(self, word):
        self.word = word
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
        self.re_meaning_entry = re.compile("^'''(.+)''' ?(.+)?$")
        self.re_meaning_def = re.compile("^#(.+)$")
        # TODO: check if this is language dependent
        self.re_meaning_eg = re.compile("^{{bijv-1\|(.+)}}$")
        self.re_syn_ref = re.compile("^\*\[([0-9]+)\]: (.+)$")
        self.re_syn_list = re.compile("\[\[([^]]+)\]\]")
        self.re_hypo = re.compile("^\*\[\[(.+)\]\]$")

    def _warn(self, warning, line=None):
        if line is None:
            self._warnings.append("%s" % (warning,))
        else:
            self._warnings.append("%s in \"%s\"" % (warning, line))

    @property
    def warnings(self):
        return self._warnings

    def parse(self, lines):
        for line in lines:
            line = line.strip().replace("{{pn}}", self.word)
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
        return self._termsets

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
            self._parse_meaning(NounTerm)
        elif self._header == 'nlstam':
            self._parse_nlstam()
        elif self._header == 'verb':
            self._parse_meaning(VerbTerm)
        elif self._header == 'syn':
            self._parse_synonyms()
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
                self._termset.sound(sound_match.group(1))
            elif ipa_match:
                # Store IPA description in term
                self._termset.ipa(ipa_match.group(1))
            else:
                self._warn("Unexpected pronunciation line", line)

    def _parse_syllables(self):
        for line in self._buff:
            match = re.search(self.re_syll, line)
            if match:
                self._termset.syllables(match.group(1))
                return
            else:
                self._warn("Unexpected syllable line", line)

    def _parse_nlnoun(self):
        # Create new current term
        term = self._ensure_term(NounTerm)
        # Match different forms of the noun
        nlnoun_match = re.search(self.re_nlnoun, self._header_params)
        if nlnoun_match:
            term.single_form(nlnoun_match.group(1))
            term.plural_form(nlnoun_match.group(2))
            term.diminutive_form(nlnoun_match.group(3))
            term.diminutive_plural_form(nlnoun_match.group(4))
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
            term.past_tense(nlstam_list[1])
            term.past_participle_tense(nlstam_list[2])
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
                term.entry(entry)
                if gender is not None:
                    term.gender(gender)
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
                    meaning.example(eg_match.group(1))
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
                    meaning = self._term.meanings()[int(ref)-1]
                except ValueError:
                    self._warn("Synonym reference is not a number", line)
                    continue
                except IndexError:
                    self._warn("Synonym reference does not match a definition",
                            line)
                    continue
                else:
                    meaning.synonyms(re.findall(self.re_syn_list, line))

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

    def _parse_etymology(self):
        pass
