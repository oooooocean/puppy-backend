from rest_framework.fields import ChoiceField, ListField, CharField
from api.models.support import IdAndName


class IdAndNameField(ChoiceField):
    def to_representation(self, value):
        if value in ('', None):
            return value
        return IdAndName(value, self.choices[value])._asdict()


class StringListField(ListField):
    child = CharField

    def to_representation(self, data):
        return data.split(',')

    def to_internal_value(self, data):
        return ','.join(super(StringListField, self).to_internal_value(data))
