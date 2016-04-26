import nltk.data
import nltk
import syllables
import math
from bs4 import BeautifulSoup
import nltk
from enchant.checker import SpellChecker
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from textblob import TextBlob


def create_and_generate_features(post):
    return StackOverflowTextAnalysis(post).generate_features()


class StackOverflowTextAnalysis(object):
    ENGINEERED_FEATURES_ON = True
    CHAR_NGRAMS_ON = True

    def __init__(self, post):
        self.body = post.get('body')
        assert self.body is not None
        self.title = post.get('title')
        self.body_length = None
        self.title_body_similarity = None
        self.title_length = None
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
        self.flesch_kincaid_grade = None
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
        self.lowercase_percentage = None
        self.uppercase_percentage = None
        self.spaces_count = None
        self.textblob = None
        self.sentiment = None
        self.subjectivity = None
        self.is_title_capitalized = None
        self.lines_of_code = None
        self.code_percentage = None
        self.num_code_tags = None
        self.num_p_tags = None

        # make a CountVectorizer-style tokenizer
        self.char_ngrammer = CountVectorizer(
            analyzer='char', ngram_range=(4, 4)
        ).build_analyzer()

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
        features = {}

        if self.ENGINEERED_FEATURES_ON:
            features = {
                "sota_body_length": self.get_body_length(),
                "sota_spelling_error_count": self.get_spelling_error_count(),
                "sota_email_count": self.get_email_count(),
                "sota_url_count": self.get_url_count(),
                "sota_ari": self.get_ari(),
                "sota_flesch_reading_ease": self.get_flesch_reading_ease(),
                "sota_flesch_kincaid_grade": self.get_flesch_kincaid_grade(),
                "sota_gunning_fog_index": self.get_gunning_fog_index(),
                "sota_smog_index": self.get_smog_index(),
                "sota_coleman_liau_index": self.get_coleman_liau_index(),
                "sota_lix": self.get_lix(),
                "sota_rix": self.get_rix(),
                "sota_uppercase_percentage": self.get_uppercase_percentage(),
                "sota_lowercase_percentage": self.get_lowercase_percentage(),
                "sota_spaces_count": self.get_spaces_count(),
                "sota_lines_of_code": self.get_lines_of_code(),
                "sota_code_percentage": self.get_code_percentage(),
                "sota_sentiment": self.get_sentiment(),
                "sota_subjectivity": self.get_subjectivity(),
                "sota_num_code_tags": self.get_num_code_tags(),
                "sota_num_p_tags": self.get_num_p_tags()
            }

            if self.get_title() is not None:
                title_features = {
                    "sota_title_length": self.get_title_length(),
                    "sota_title_body_similarity": self.get_title_body_similarity(),
                    "sota_is_title_capitalized": self.get_is_title_capitalized()
                }

                features = {**features, **title_features}

        if self.CHAR_NGRAMS_ON:
            for t in self.char_ngrammer(self.get_body()):
                features[t] = features.get(t, 0) + 1

        return features

    def get_body(self):
        return self.body

    def get_title(self):
        return self.title

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

    def get_title_length(self):
        if self.title_length is None:
            self.title_length = len(self.get_title())
        return self.title_length

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

    def get_flesch_kincaid_grade(self):
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

    def get_smog_grade(self):
        pass

    def get_coleman_liau_index(self):
        if self.coleman_liau_index is None:
            self.coleman_liau_index = (
                5.89 * self.get_character_count() / self.get_word_count()) - (
                30 * (self.get_sentence_count()/self.get_word_count())) - 15.8
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

    def get_lowercase_percentage(self):
        if self.lowercase_percentage is None:
            lowercase_count = 0
            for character in self.get_body_text():
                if character.islower():
                    lowercase_count += 1
            self.lowercase_percentage = (
                lowercase_count/len(self.get_body_text()))*100
        return self.lowercase_percentage

    def get_uppercase_percentage(self):
        if self.uppercase_percentage is None:
            uppercase_count = 0
            for character in self.get_body_text():
                if character.isupper():
                    uppercase_count += 1
            self.uppercase_percentage = (
                uppercase_count/len(self.get_body_text()))*100
        return self.uppercase_percentage

    def get_spaces_count(self):
        if self.spaces_count is None:
            self.spaces_count = 0
            for character in self.get_body_text():
                if character.isspace():
                    self.spaces_count += 1
        return self.spaces_count

    def get_textblob(self):
        if self.textblob is None:
            self.textblob = TextBlob(self.get_body_text())
        return self.textblob

    def get_sentiment(self):
        if self.sentiment is None:
            self.sentiment = self.get_textblob().sentiment.polarity
        return self.sentiment

    def get_subjectivity(self):
        if self.subjectivity is None:
            self.subjectivity = self.get_textblob().sentiment.subjectivity
        return self.subjectivity

    def get_title_body_similarity(self):
        if self.title_body_similarity is None:
            self.title_body_similarity = self.cosine_sim(
                self.get_title(), self.get_body_text()
            )
        return self.title_body_similarity

    def get_lines_of_code(self):
        if self.lines_of_code is None:
            # number of lines of code declared between tags <code>
            bs = BeautifulSoup(self.get_body(), "lxml")
            code = bs.find_all('code')
            self.lines_of_code = ' '.join([c.get_text() for c in code]).count('\n')+1
        return self.lines_of_code

    def get_code_percentage(self):
        if self.code_percentage is None:
            # percentage of lines of code declared between tags <code>
            lines_of_code = self.get_lines_of_code()
            lines_of_text = self.get_body().count('\n')+1
            self.code_percentage = (lines_of_code/lines_of_text)*100
        return self.code_percentage

    def get_num_code_tags(self):
        if self.num_code_tags is None:
            bs = BeautifulSoup(self.get_body(), "lxml")
            self.num_code_tags = len(bs.find_all('code'))
        return self.num_code_tags

    def get_num_p_tags(self):
        if self.num_p_tags is None:
            bs = BeautifulSoup(self.get_body(), "lxml")
            self.num_p_tags = len(bs.find_all('p'))
        return self.num_p_tags

    def get_is_title_capitalized(self):
        if self.is_title_capitalized is None:
            self.is_title_capitalized = self.get_title()[0].isupper()
        return self.is_title_capitalized

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

    def stem_tokens(self, tokens):
        stemmer = nltk.stem.porter.PorterStemmer()
        return [stemmer.stem(item) for item in tokens]

    '''remove punctuation, lowercase, stem'''
    def normalize(self, text):
        remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
        return self.stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

    def cosine_sim(self, text1, text2):
        vectorizer = TfidfVectorizer(tokenizer=self.normalize, stop_words='english')
        tfidf = vectorizer.fit_transform([text1, text2])
        return ((tfidf * tfidf.T).A)[0, 1]
