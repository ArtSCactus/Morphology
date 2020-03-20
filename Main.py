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


if __name__ == '__main__':
    vocabulary = Vocabulary([])
    vocabulary.add("word")
    vocabulary.print_all()
    vocabulary.delete("word")
    vocabulary.print_all()
    reader = FileReader('example.txt')
    print(reader.read())
    print(reader.read_in_list())
