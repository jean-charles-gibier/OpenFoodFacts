import sys


class SomeClass:
    def __init__(self, **some):
        for i in some.keys():
            print(" key:" + str(i) + " => " + str(some[i]))
        self.test = some["nb"]


json_list = [{"nb": 1, "list": [1, 2, 3], "dict": {"a": "b"}},
             {"nb": 2, "list": [4, 5, 6], "dict": {"b": "c"}},
             {"nb": 3, "list": [7, 8, 9], "dict": {"c": "d"}}]

for idx, some in enumerate(json_list):
    try:
        # get object type
        an_instance = SomeClass(**some)
        print(an_instance)

        if some.__eq__({"nb": 2, "list": [4, 5, 6], "dict": {"b": "c"}}):
            json_list.pop(idx)

    except:
        print('[%s] Ne peut enregistrer #%s', sys.exc_info()[0], an_instance)

print('2 eme passage :')

for some in json_list:
    print(some)
