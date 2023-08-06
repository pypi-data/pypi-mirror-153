import django.db.models


class TableFilter:
    def __init__(self, key, label):
        self.key = key
        self.label = label


class TableButton:
    def __init__(self, label, action):
        self.label = label
        self.action = action


class TableButtonGroup:
    def __init__(self, label, items):
        self.label = label
        self.items = items


class TableButtonDivider:
    def __init__(self):
        None


class TableColumn:
    def __init__(self, key, name, type=None, value=None, method=None, link=None, sortable=False):
        self.key = key
        self.name = name
        self.type = type
        self.value = value
        self.method = method
        self.link = link
        self.sortable = sortable


class Table:
    def __init__(self, rows, columns, heading=None, create=None, update=None, search=False, filters=None, buttons=None, placeholder=None):
        self.rows = rows
        if isinstance(rows, django.db.models.QuerySet):
            self.count = rows.count()
        self.columns = columns
        self.heading = heading
        self.create = create
        self.update = update
        self.search = search
        self.filters = filters
        self.buttons = buttons
        self.placeholder = placeholder

    def sort(self, rows):
        pass

    def formatter(self, row):
        return ''

