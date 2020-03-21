import pymorphy2
from pymorphy2 import MorphAnalyzer


class Vocabulary:
    def __init__(self, word_list):
        self.words_list = word_list

    def add(self, word):
        self.words_list.append(word)

    def delete(self, word):
        for current_word in self.words_list:
            if current_word is word:
                self.words_list.remove(current_word)
                break

    def print_all(self):
        if not self.words_list:
            print("empty")
        else:
            for current_word in self.words_list:
                print(str(current_word))

    def print(self, word):
        for current_word in self.words_list:
            if current_word is word:
                print(str(current_word))
                break

    def get_as_array(self):
        return self.words_list


class FileReader:
    def __init__(self, path):
        self.path = path

    def read(self):
        import codecs
        file = codecs.open(self.path, "r", "utf_8_sig")
        text = file.read()
        file.close()
        return text

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
# Returns map word -> analysis of given words
    def get_analyzed_lexemes(self, words_list):
        morphology = pymorphy2.MorphAnalyzer()
        analyzed_lexemes = {}
        for word in words_list:
            analyzed_lexemes.update({word:morphology.parse(word)[0]})
        return analyzed_lexemes


if __name__ == '__main__':
    reader = FileReader('example.txt')
    text_handler = TextHandler()
    text = reader.read()
    words = TextHandler().get_words_from_text(text)
    morpher = LexemeAnalyzer()
    lexemes = morpher.get_analyzed_lexemes(words)
    for word, analysis in lexemes.items():
        print(word, analysis.tag.cyr_repr)