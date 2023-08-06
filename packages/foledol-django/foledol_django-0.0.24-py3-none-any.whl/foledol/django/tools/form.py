from foledol.django.logger import log


class Form:
    def __init__(self, context, fields, namespace=None):
        self.context = context
        self.fields = fields
        self.namespace = namespace
        self.old_values = None
        self.new_values = None

    def field(self, key):
        try:
            return next(field for field in self.fields if field.key == key)
        except StopIteration:
            raise Exception("Invalid field '" + key + "'")

    def read(self, values, sibling=None, defaults=None):
        self.old_values = {}
        for field in self.fields:
            default_value = None
            if defaults and field.key in defaults:
                default_value = defaults[field.key]
            elif sibling and field.key in sibling.__dict__:
                default_value = sibling.__dict__[field.key]
            self.old_values[field.key] = default_value
            self.context[field.key] = field.value #if field.value else default_value
            # TODO: move this before the self.context
            field.read(values, default_value)
        self.context['form'] = self

    def validate(self):
        self.context['error'] = False
        for field in self.fields:
            field.validate()
            self.context[field.key] = field.value
            self.context['errors_on_' + field.key] = None
            if len(field.errors) > 0:
                self.context['errors_on_' + field.key] = field.errors
            self.context['error'] |= field.has_error()

    def save(self, sibling):
        self.new_values = {}
        for field in self.fields:
            if field.key in sibling.__dict__:
                sibling.__dict__[field.key] = field.value
            self.new_values[field.key] = field.value

    def save_and_log(self, sibling, model, action, request):
        self.save(sibling)
        sibling.save()
        log(sibling.id, model, action, request.user, self.old_values, self.new_values)
