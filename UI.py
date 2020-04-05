from Main import MorphologySystem, NoSuchWordError, NoSuchWordEndingError
import sys

system = MorphologySystem()


def add_to_dict_menu():
    print("~~~~~~~~~~~~~~ Dictionary filling ~~~~~~~~~~~~~~")
    while True:
        option = input("Choose input type:\n[1] From file\n[2] From console\n[0] Exit\n->")
        if (option is '0'):
            break
        if option is '1':
            file_path = input("File path ->")
            try:
                system.analyse_text_from_file(file_path)
            except FileNotFoundError as e:
                print("File not found: ", e.filename)
                break
            system.get_vocabulary().print_all_cyr_repr()
        if option is '2':
            text = input("Input text -> ")
            system.analyse_manual_text(text)
            system.get_vocabulary().print_all_cyr_repr()
            break
        else:
            print("Wrong option. Try again")


def generate_word_option_menu():
    word_base = input('Please, enter word base: ')
    word_ending = input('Please, enter word ending: ')
    try:
        options = system.generate_word(word_base, word_ending)
    except NoSuchWordError as e:
        print(e.get_message())
        return
    except NoSuchWordEndingError as e:
        print(e.get_message())
        return
    print("Possible options:")
    for option in options:
        print(option)


def find_word_option_menu():
    word = input('Please, input word -> ')
    print(system.get_word_ending(word))


if __name__ == '__main__':
    while True:
        print('~~~~~~~~~~~~~~ Main menu ~~~~~~~~~~~~~~')
        option = input("Choose option: \n[1] Add to dictionary\n[2] Print dictionary\n[3] Word endings\n[4] Find Word "
                       "ending\n[5] Generate word\n[0] Exit\n->")
        if option is '1':
            add_to_dict_menu()
            continue
        if option is '2':
            system.print_vocabulary()
            continue
        if option is '3':
            system.vocabulary.print_all_words_endings();
            continue
        if option is '4':
            find_word_option_menu()
            continue
        if option is '5':
            generate_word_option_menu()
            continue
        if option is '0':
            sys.exit(0)
        else:
            print("Wrong option")
