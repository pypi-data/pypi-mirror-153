
from django.forms.models import ModelChoiceField

from .widgets import Select2

class MPTTModelChoiceField(ModelChoiceField):

    def __init__(self, *args, **kwargs):
        self.label_property = kwargs.pop("label_property", None)
        kwargs["widget"] = Select2
        super().__init__(*args, **kwargs)

    def label_from_instance(self, obj):
        if self.label_property:
            value = getattr(obj, self.label_property)
            if callable(value):
                value = value()
            return value
        else:
            return " / ".join([x.name for x in obj.get_ancestors(include_self=True)])

class ModelChoiceFieldWithLabelProperty(ModelChoiceField):
    def __init__(self, *args, **kwargs):
        self.label_property = kwargs.pop("label_property", None)
        super().__init__(*args, **kwargs)

    def label_from_instance(self, obj):
        if self.label_property:
            value = getattr(obj, self.label_property)
            if callable(value):
                value = value()
            return value
        else:
            return str(obj)
