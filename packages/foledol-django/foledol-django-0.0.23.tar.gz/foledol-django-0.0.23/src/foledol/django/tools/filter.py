class Filter:
    code = 'default'
    name = "default"
    title = None

    def __str__(self):
        return self.name

    def filter(self, source):
        return source

    def all(self):
        pass


class NoneFilter(Filter):
    code = '(none)'
    name = '(aucun)'


def filters_dictionary(filters):
    return {item.code: item for item in filters}

