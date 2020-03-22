import collections

import pymorphy2
from pymorphy2 import MorphAnalyzer


class Vocabulary:
    def __init__(self):
        # contains words and their analysis
        self.words_map = {}
        # contains words and their endings
        self.words_endings = {}

    def update_word_endings(self, dict):
        self.words_endings.update(dict)

    def add_word_ending(self, word, ending):
        self.words_endings.update(word, ending)

    def delete_word_ending(self, word):
        self.words_endings.pop(word)

    def get_word_ending(self, word):
        return self.words_endings.get(word)

    def get_word_endings_dict(self):
        return self.words_endings

    def print_word_ending(self, word):
        print(self.words_endings.get(word))

    def print_all_words_endings(self):
        if not self.words_endings:
            print("empty")
        else:
            for current_word, ending in self.words_endings.items():
                print(current_word, " -> ", ending)

    # adds word and it's analysis to vocabulary
    def add_manual(self, word, morph_analysis):
        self.words_map.update(word, morph_analysis)
        self.words_map = collections.OrderedDict(sorted(self.words_map.items()))

    # adds all pairs word -> analysis to vocabulary
    def update(self, dict):
        self.words_map.update(dict)
        self.words_map = collections.OrderedDict(sorted(self.words_map.items()))

    # removes pair word -> analysis from vocabulary
    def delete(self, word):
        self.words_map.pop(word)

    # prints all pairs word -> analysis to console
    def print_all(self):
        if not self.words_map:
            print("empty")
        else:
            for current_word, morph_analysis in self.words_map.items():
                print(current_word, " -> ", morph_analysis)

    # prints all pairs word -> analysis to console in cyrillic representation
    def print_all_cyr_repr(self):
        if not self.words_map:
            print("empty")
        else:
            for current_word, morph_analysis in self.words_map.items():
                print(current_word, " -> ", morph_analysis.tag.cyr_repr)

    # prints analysis of the word  from vocabulary
    def print_analysis(self, word):
        for current_word, morph_analysis in self.words_map.keys():
            if current_word is word:
                print(word, " -> ", morph_analysis)
                break

    # returns word analysis dict
    def get_dict(self):
        return self.words_map


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
        pass

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
        self.vocabulary.print_all()

    # Returns word ending (окончание in russian)
    def get_word_ending(self, word):
        normal_form = self.morphology.parse(word)[0].normal_form
        words_intersection = ''.join(sorted(set(word) & set(normal_form), key=word.index))
        ending = word.split(words_intersection)
        try:
            return ending[1]
        except IndexError as e:
            return ending[0]

    def get_normal_form(self, word):
        print(self.morphology.parse(word)[0].normal_form)

    def get_analysis(self, word):
        return self.vocabulary.get_dict().get(word)

    def print_word_endings(self):
        self.vocabulary.p


if __name__ == '__main__':
    system = MorphologySystem()
    system.analyse_manual_text('машиной')
    print(system.get_word_ending('машиной'))
    print(system.get_analysis('машина'))
    system.vocabulary.print_all_words_endings()
