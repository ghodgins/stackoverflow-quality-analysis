import nltk.data
import nltk
import syllables
import math
from bs4 import BeautifulSoup
import nltk
from enchant.checker import SpellChecker
import re


class StackOverflowTextAnalysis(object):
    def __init__(self, body):
        self.body = body
        self.body_length = None
        self.body_text = None
        self.words = None
        self.sentences = None
        self.character_count = None
        self.avg_characters_per_word = None
        self.avg_words_per_sentence = None
        self.word_count = None
        self.sentence_count = None
        self.total_syllable_count = None
        self.complex_word_count = None
        self.long_word_count = None
        self.avg_words_per_sentence = None
        self.ari = None
        self.flesch_reading_ease = None
        self.flesch_kincaid_grade_level = None
        self.gunning_fog_index = None
        self.smog_index = None
        self.coleman_liau_index = None
        self.lix = None
        self.rix = None
        self.spelling_errors = None
        self.spelling_error_count = None
        self.urls = None
        self.url_count = None
        self.emails = None
        self.email_count = None

        # regex to find strings of the form example@mail.com
        # unfortunately also matches urls such as //ex@mple.com
        self.email_regex_string = ''.join((
            # example (can't start with .)
            "([A-Za-z0-9!#$%&'*+\/=?^_`{|}~-]+",
            # example (allowing . after start)
            "(?:\.[A-Za-z0-9!#$%&'*+\/=?^_`{|}~-]+)*",
            # @ OR at
            "(@|\sat\s)",
            # mail
            "(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?",
            # . OR dot
            "(\.|\sdot\s))+",
            # com
            "[A-Za-z0-9](?:[a-z0-9-]*[A-Za-z0-9])?)"
        ))

        self.email_regex = re.compile(self.email_regex_string)

        self.url_regex_string = ''.join((
            'http[s]?://',
            '(?:[a-zA-Z]|[0-9]|',
            '[$-_@.&+]|[!*\(\),]',
            '|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        ))

        self.url_regex = re.compile(''.join(self.url_regex_string))

    # prepend sota (abbreviation of StackOverflowTextAnalysis) to each key to
    # ensure that they are unique when combined with other feature sets
    def generate_features(self):
        return {
            "sota_body_length": self.get_body_length(),
            "sota_spelling_error_count": self.get_spelling_error_count(),
            "sota_email_count": self.get_email_count(),
            "sota_url_count": self.get_url_count(),
            "sota_ari": self.get_ari(),
            "sota_flesch_reading_ease": self.get_flesch_reading_ease(),
            "sota_flesch_kincaid_grade_level": self.get_flesch_kincaid_grade_level(),
            "sota_gunning_fog_index": self.get_gunning_fog_index(),
            "sota_smog_index": self.get_smog_index(),
            "sota_coleman_liau_index": self.get_coleman_liau_index(),
            "sota_lix": self.get_lix(),
            "sota_rix": self.get_rix()
        }

    def get_body(self):
        return self.body

    def get_body_text(self):
        if self.body_text is None:
            self.body_text = BeautifulSoup(self.get_body(), "lxml").get_text()
        return self.body_text

    def get_words(self):
        if self.words is None:
            self.words = nltk.word_tokenize(self.get_body_text())
        return self.words

    def get_sentences(self):
        if self.sentences is None:
            self.sentences = nltk.sent_tokenize(self.get_body_text())
        return self.sentences

    def get_character_count(self):
        if self.character_count is None:
            self.character_count = len(self.get_body_text())
        return self.character_count

    def get_word_count(self):
        if self.word_count is None:
            self.word_count = len(self.get_words())
        return self.word_count

    def get_sentence_count(self):
        if self.sentence_count is None:
            self.sentence_count = len(self.get_sentences())
        return self.sentence_count

    def get_body_length(self):
        if self.body_length is None:
            self.body_length = len(self.get_body_text())
        return self.body_length

    def get_long_word_count(self):
        if self.long_word_count is None:
            self.long_word_count = 0
            for word in self.get_words():
                if len(word) >= 7:
                    self.long_word_count += 1
        return self.long_word_count

    def get_avg_words_per_sentence(self):
        if self.avg_words_per_sentence is None:
            self.avg_words_per_sentence = self.get_word_count(
                ) / self.get_sentence_count()
        return self.avg_words_per_sentence

    def get_avg_characters_per_word(self):
        if self.avg_characters_per_word is None:
            self.avg_characters_per_word = (
                self.get_character_count() / self.get_word_count()
            )
        return self.avg_characters_per_word

    def get_total_syllable_count(self):
        if self.total_syllable_count is None:
            self.total_syllable_count = 0
            for word in self.get_words():
                self.total_syllable_count += syllables.count(word)
        return self.total_syllable_count

    # This method only considers the number of syllables in a word.
    # This often results in that too many complex words are detected.
    def get_complex_word_count(self):
        if self.complex_word_count is None:
            self.complex_word_count = 0
            for word in self.get_words():
                if syllables.count(word) >= 3:
                    self.complex_word_count += 1
        return self.complex_word_count

    # calculate the Automated Readability Index which estimates
    # the US High School grade reading level of text
    def get_ari(self):
        if self.ari is None:
            self.ari = (4.71 * self.get_avg_characters_per_word()) + \
                (0.5 * self.get_avg_words_per_sentence()) - 21.43
        return self.ari

    def get_flesch_reading_ease(self):
        if self.flesch_reading_ease is None:
            self.flesch_reading_ease = (
                206.835 - (
                    1.015 * self.get_avg_words_per_sentence()
                ) - (
                    84.6 * (
                        self.get_total_syllable_count() / self.get_word_count()
                    )
                )
            )
        return self.flesch_reading_ease

    def get_flesch_kincaid_grade_level(self):
        if self.flesch_reading_ease is None:
            self.flesch_reading_ease = 0.39 * self.get_avg_words_per_sentence() + 11.8 * \
                (self.get_total_syllable_count() / self.get_word_count()) - 15.59
        return self.flesch_reading_ease

    def get_gunning_fog_index(self):
        if self.gunning_fog_index is None:
            self.gunning_fog_index = 0.4 * (
                (self.get_avg_words_per_sentence()) + (
                    100 * (
                        self.get_complex_word_count() / self.get_word_count()
                    ))
            )
        return self.gunning_fog_index

    def get_smog_index(self):
        if self.smog_index is None:
            self.smog_index = math.sqrt(
                self.get_complex_word_count() * (
                    30 / self.get_sentence_count()
                )
            ) + 3
        return self.smog_index

    def smog_grade():
        pass

    def get_coleman_liau_index(self):
        if self.coleman_liau_index is None:
            self.coleman_liau_index = (
                5.89 * self.get_character_count() / self.get_word_count()) - (
                30 * (self.get_sentence_count() / self.get_word_count())) - 15.8
        return self.coleman_liau_index

    def get_lix(self):
        if self.lix is None:
            self.lix = self.get_word_count() / self.get_sentence_count() + \
                float(100 * self.get_long_word_count()) / self.get_word_count()
        return self.lix

    def get_rix(self):
        if self.rix is None:
            self.rix = self.get_long_word_count() / self.get_sentence_count()
        return self.rix

    def lowercase_percentage():
        pass

    def uppercase_percentage():
        pass

    def spaces_count():
        pass

    def text_speak_count():
        # this or spellcheck errors count???
        pass

    def title_body_similarity():
        pass

    def title_length():
        pass

    def is_title_capitalized():
        pass

    def avg_term_entropy():
        # avg entropy of terms in a question,
        # according to the SO entropy index we devised.
        # Each term’s entropy is calculated on the SO dataset.
        pass

    def lines_of_code():
        pass

    def lines_of_code_percentage():
        # percentage of lines of code declared between tags <code>
        pass

    def metric_entropy():
        pass

    def get_email_count(self):
        if self.email_count is None:
            self.email_count = len(self.find_emails())
        return self.email_count

    def find_emails(self):
        if self.emails is None:
            # Removing lines that start with '//' because the regular expression
            # mistakenly matches patterns like 'http://foo@bar.com' as
            # '//foo@bar.com'.
            self.emails = [
                email[0] for email in re.findall(self.email_regex, self.get_body())
                if not email[0].startswith('//')
            ]
        return self.emails

    def get_url_count(self):
        if self.url_count is None:
            self.url_count = len(self.find_urls())
        return self.url_count

    def find_urls(self):
        if self.urls is None:
            self.urls = re.findall(self.url_regex, self.get_body())
        return self.urls

    def find_spelling_errors(self):
        if self.spelling_errors is None:
            spellchecker = SpellChecker("en_US", self.get_body_text())
            self.spelling_errors = list(spellchecker)
        return self.spelling_errors

    def get_spelling_error_count(self):
        if self.spelling_error_count is None:
            self.spelling_error_count = len(self.find_spelling_errors())
        return self.spelling_error_count
