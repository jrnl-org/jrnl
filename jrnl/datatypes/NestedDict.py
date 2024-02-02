"""https://stackoverflow.com/a/74873621/8740440"""


class NestedDict(dict):
    def __missing__(self, x):
        self[x] = NestedDict()
        return self[x]
