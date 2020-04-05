import collections

import pymorphy2
from pymorphy2 import MorphAnalyzer


class Vocabulary:
    def __init__(self):
        # contains words and their analysis
        self.__words_map = {}
        # contains words and their endings
        self.__words_endings = {}

    def update_word_endings(self, map):
        self.__words_endings.update(map)

    def add_word_ending(self, word, ending):
        if word in self.__words_endings.keys():
            return
        self.__words_endings.update(word, ending)

    def delete_word_ending(self, word):
        self.__words_endings.pop(word)

    def get_word_ending(self, word):
        return self.__words_endings.get(word)

    def get_word_endings_dict(self):
        return self.__words_endings

    def print_word_ending(self, word):
        print(self.__words_endings.get(word))

    def print_all_words_endings(self):
        if not self.__words_endings:
            print("empty")
        else:
            for current_word, ending in self.__words_endings.items():
                print(current_word, " -> ", ending)

    # adds word and it's analysis to vocabulary
    def add_manual(self, word, morph_analysis):
        if word in self.__words_map.keys():
            return
        self.__words_map.update(word, morph_analysis)
        self.__words_map = collections.OrderedDict(sorted(self.__words_map.items()))

    # adds all pairs word -> analysis to vocabulary
    def update(self, dict):
        self.__words_map.update(dict)
        self.__words_map = collections.OrderedDict(sorted(self.__words_map.items()))

    # removes pair word -> analysis from vocabulary
    def delete(self, word):
        self.__words_map.pop(word)

    # prints all pairs word -> analysis to console
    def print_all(self):
        if not self.__words_map:
            print("empty")
        else:
            for current_word, morph_analysis in self.__words_map.items():
                print(current_word, " -> ", morph_analysis, " ending: ", self.__words_endings.get(current_word))

    # prints all pairs word -> analysis to console in cyrillic representation
    def print_all_cyr_repr(self):
        if not self.__words_map:
            print("empty")
        else:
            for current_word, morph_analysis in self.__words_map.items():
                print(current_word, " -> ", morph_analysis.tag.cyr_repr, " ending: ",
                      self.__words_endings.get(current_word))

    # prints analysis of the word  from vocabulary
    def print_analysis(self, word):
        for current_word, morph_analysis in self.__words_map.keys():
            if current_word is word:
                print(word, " -> ", morph_analysis, " ending: ", self.__words_endings.get(current_word))
                break

    # returns word analysis dict
    def get_dict(self):
        return self.__words_map

    def get_word_meta(self, word):
        return self.__words_map.get(word)


class FileReader:
    def __init__(self, path):
        self.path = path

    """ Reads file and returns as single string row """

    def read(self):
        import codecs
        file = codecs.open(self.path, "r", "utf_8_sig")
        text = file.read()
        file.close()
        return text

    """ Reads file and returns as rows list """

    def read_in_list(self):
        import codecs
        file = codecs.open(self.path, "r", "utf_8_sig")
        list = []
        for line in file:
            list.append(line)
        file.close()
        return list


class TextHandler:
    def __init__(self):
        pass

    def get_sentences(self, text):
        import re
        sentence_regexp = re.compile('[.!?…]')
        sentences = sentence_regexp.split(text)
        return sentences

    def get_words(self, sentence):
        import re
        word_regexp = re.compile('\s+')
        words = word_regexp.split(sentence)
        for word in words:
            if word is '':
                words.remove(word)

        return words

    def get_words_from_text(self, text):
        words = []
        all_sentences = self.get_sentences(text)
        for sentence in all_sentences:
            current_sentence_words = self.get_words(sentence)
            words = words + current_sentence_words
        return words


class LexemeAnalyzer:
    def __init__(self):
        pass

    """ Returns map word -> analysis of given words"""

    @staticmethod
    def analyze_words(words_list):
        morphology = pymorphy2.MorphAnalyzer()
        analyzed_lexemes = {}
        for word in words_list:
            analyzed_lexemes.update({word: morphology.parse(word)[0]})
        return analyzed_lexemes


class MorphologySystem:
    def __init__(self):
        self.vocabulary = Vocabulary()
        self.text_handler = TextHandler()
        self.morphology = MorphAnalyzer()

    # Returns map of type word -> analysis
    def __analyze_words(self, words_list):
        analyzed_lexemes = {}
        for word in words_list:
            analyzed_lexemes.update({self.morphology.parse(word)[0].normal_form: self.morphology.parse(word)[0]})
        return analyzed_lexemes

    def __get_words_endings(self, words_list):
        endings = {}
        for word in words_list:
            endings.update({self.morphology.parse(word)[0].normal_form: self.get_word_ending(word)})
        return endings

    def analyse_text_from_file(self, path):
        temp = FileReader(path)
        text = temp.read()
        temp = TextHandler()
        words = temp.get_words_from_text(text)
        self.vocabulary.update(self.__analyze_words(words))
        self.vocabulary.update_word_endings(self.__get_words_endings(words))
        list(self.vocabulary.get_word_endings_dict()).sort()
        list(self.vocabulary.get_dict().items()).sort()

    def analyse_manual_text(self, text):
        words = self.text_handler.get_words_from_text(text)
        analysis = self.__analyze_words(words)
        self.vocabulary.update(analysis)
        self.vocabulary.update_word_endings(self.__get_words_endings(words))
        list(self.vocabulary.get_word_endings_dict()).sort()
        list(self.vocabulary.get_dict().items()).sort()

    def get_vocabulary(self):
        return self.vocabulary

    def print_vocabulary(self):
        self.vocabulary.print_all_cyr_repr()

    # generates a words with ending
    def generate_word(self, base, ending):
        word = self.vocabulary.get_word_meta(base)
        voc_ending = self.vocabulary.get_word_ending(base)

        if word is None:
            raise NoSuchWordError('No such word in the vocabulary')
        if voc_ending is None:
            raise NoSuchWordEndingError('No such word in the vocabulary')
            print("Normal form", word.normal_form)
        lexeme = word.lexeme
        options = []
        for form in lexeme:
            form = form.word
            if ending in form:
                if form not in options:
                    options.append(form)
        return options

    # Returns word ending (окончание in russian)
    def get_word_ending(self, word):
        import re
        if len(word) is 1 or re.match('([0-9]+|[-&|!?+$#@()^:%])', word):
            return 'none'
        normal_form = self.morphology.parse(word)[0].normal_form
        if word == normal_form:
            return "none"
        words_intersection = ''.join(sorted(set(word) & set(normal_form), key=word.index))
        ending = word.split(words_intersection)
        try:
            ending = ending[1]
        except IndexError as e:
            ending = ending[0]
            # there's no word ending longer than 3 symbols in russian language
        if len(ending) > 3:
            return "none"
        else:
            return ending


def get_normal_form(self, word):
    print(self.morphology.parse(word)[0].normal_form)


def get_analysis(self, word):
    return self.vocabulary.get_dict().get(word)


def print_word_endings(self):
    self.vocabulary.p


class NoSuchWordError(RuntimeError):
    def __init__(self, message):
        self.__message = message

    def get_message(self):
        return self.__message


class NoSuchWordEndingError(RuntimeError):
    def __init__(self, message):
        self.__message = message

    def get_message(self):
        return self.__message


if __name__ == '__main__':
    system = MorphologySystem()
    system.analyse_text_from_file("example.txt")
    print(system.generate_word('современный', 'ого'))
