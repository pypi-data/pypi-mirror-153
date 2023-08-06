

from django.contrib.admin import FieldListFilter
from django.utils.translation import gettext_lazy as _

class MultipleSelectFieldFilter(FieldListFilter):

    def expected_parameters(self):
        return ["{field_path}__in".format(field_path=self.field_path)]
    
    def choices(self, changelist):
        return []

class TextInputFieldFilter(FieldListFilter):
    template = 'django_power_admin/filters/TextInputFieldFilter.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.input_name = "{field_path}__icontains".format(field_path=self.field_path)
        self.input_value = self.used_parameters.get(self.input_name, "")

    def expected_parameters(self):
        return ["{field_path}__icontains".format(field_path=self.field_path)]
    
    def choices(self, changelist):
        return []

    class Media:
        css = {
            "all": [
                "django_power_admin/filters/TextInputFieldFilter/css/TextInputFieldFilter.css",
            ]
        }
        js = [
            "django_power_admin/assets/js/parseParam.js",
            "admin/js/vendor/jquery/jquery.js",
            "django_power_admin/filters/TextInputFieldFilter/js/TextInputFieldFilter.js",
            "admin/js/jquery.init.js",
        ]


class DateRangeFilter(FieldListFilter):
    template = 'django_power_admin/filters/DateRangeFilter.html'

    def __init__(self, field, request, params, model, model_admin, field_path,
            input_start_placeholder=_("Date Start"),
            input_end_placeholder=_("Date End"),
            ):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.input_start_placeholder = input_start_placeholder
        self.input_end_placeholder = input_end_placeholder
        
        self.input_start_name = "{field_path}__gte".format(field_path=self.field_path)
        self.input_end_name = "{field_path}__lte"

        if self.input_start_name in self.used_parameters:
            if not self.used_parameters[self.input_start_name]:
                del self.used_parameters[self.input_start_name]
        if self.input_end_name in self.used_parameters:
            if not self.used_parameters[self.input_end_name]:
                del self.used_parameters[self.input_end_name]
            
        self.input_start_value = self.used_parameters.get(self.input_start_name, "")
        self.input_end_value = self.used_parameters.get(self.input_end_name, "")

    def expected_parameters(self):
        return [
            "{field_path}__gte".format(field_path=self.field_path),
            "{field_path}__lte".format(field_path=self.field_path),
        ]
    
    def choices(self, changelist):
        return []

    class Media:
        css = {
            "all": [
                "jquery-ui/jquery-ui.min.css",
                "django_power_admin/filters/DateRangeFilter/css/DateRangeFilter.css",
            ]
        }
        js = [
            "django_power_admin/assets/js/parseParam.js",
            "admin/js/vendor/jquery/jquery.js",
            "jquery-ui/jquery-ui.min.js",
            "jquery-ui/i18n/datepicker-zh-Hans.js",
            "django_power_admin/filters/DateRangeFilter/js/DateRangeFilter.js",
            "admin/js/jquery.init.js",
        ]
