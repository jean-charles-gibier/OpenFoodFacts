#!/usr/bin/python3
# coding: utf-8

class Bidon:
    _params_dict = {}

    def __init__(self, **content):
        for a in content:
            self._params_dict[a] = content[a]

    @property
    def params_dict(self):
        return self._params_dict


def main():
    # test
    obj1 = Bidon(**{'test': 1, 'name': 'BIDON1'})
    obj2 = Bidon(**{'test': 2, 'name': 'BIDON2'})
    print(" obj1: " + str(obj1.params_dict))
    print(" obj2: " + str(obj2.params_dict))


# principal
if __name__ == "__main__":
    main()
