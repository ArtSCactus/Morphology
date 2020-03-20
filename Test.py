# ~~~~~~~~~~~ Artsiom's examples ~~~~~~~~~~~~~~~~
def print_biggest(a, b):
    print("Doing if else(choosing the biggest one from {0} and {1}):".format(a, b))
    if a >= b:
        print(a)
    else:
        print(b)


def do_cycle(iterations):
    print("Doing cycle: ")
    iteration = 0;
    while iteration < iterations:
        print(iteration)
        iteration = iteration + 1


def do_exception_handling():
    print("Doing exception handling")
    print("Throwing Exception with args: Test, exception and handling it")
    try:
        raise Exception("Exception", "not handled")
    except Exception as e:
        print("Exception successfully handled! Args:", str(e.args))


def show_array():
    print("Showing array")
    str_array = ["one", "two", "three", "four"];
    counter = 0;
    for _ in str_array:
        print("Element[{0}]:{1}".format(counter, str_array[counter]))
        counter = counter + 1;


def show_dict():
    print("Showing dict")
    # instead of key1, keyN can be any variable/object
    map = {"key1": "value1", "key2": "value2"}
    print("By keys:")
    for key in map.keys():
        print("Value by {0}".format(map.get(key)))
    print("By values:")
    for value in map.values():
        print("Value from values(): ".format(map.get(value)))
    print("All pairs")
    for key, value in map.items():
        print("Key: {0} -> Value: {1}".format(key, value))


def show_list(list):
    print("Showing list:")
    print(str(list))
    print("Length {0}".format(len(list)))
    print("Is number 3 in list? {0}".format(3 in list))
    list_for_concat = [5, 6, 7]
    print("Concat {0} with {1} -> {2}".format(list, list_for_concat, list + list_for_concat))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    print_biggest(2, 3)
    do_cycle(5)
    do_exception_handling()
    show_array()
    show_dict()
    show_list([1, 2, 3, 4])


if __name__ == "__main__":
    main()
