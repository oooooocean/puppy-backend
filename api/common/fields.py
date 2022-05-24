from rest_framework.fields import ChoiceField
from api.models.support import IdAndName


class IdAndNameField(ChoiceField):
    def to_representation(self, value):
        if value in ('', None):
            return value
        return IdAndName(value, self.choices[value])._asdict()
