


from django.forms.widgets import Textarea
from django.forms.widgets import PasswordInput
from django.forms.widgets import Select
from django.forms.widgets import SelectMultiple
from django.utils.translation import get_language

from django.contrib.admin.widgets import SELECT2_TRANSLATIONS

from django.contrib.auth import get_user_model

try:
    from django_middleware_global_request.middleware import get_request
except ImportError:
    def get_request():
        return None

User = get_user_model()

SELECT2_LANGUAGE_CODE = SELECT2_TRANSLATIONS.get(get_language())
SELECT2_I18N_FILES = []
if SELECT2_LANGUAGE_CODE:
    SELECT2_I18N_FILES += [
        "admin/js/vendor/select2/i18n/%s.js" % SELECT2_LANGUAGE_CODE
    ]

class Select2(Select):

    def __init__(self, attrs=None, choices=None):
        attrs = attrs or {}
        choices = choices or []
        if "class" in attrs:
            attrs["class"] += " django_power_admin_select2_widget"
        else:
            attrs["class"] = "django_power_admin_select2_widget"
        super().__init__(attrs=attrs, choices=choices)

    class Media:
        js=[
            "admin/js/vendor/jquery/jquery.js",
            "admin/js/vendor/select2/select2.full.js",
            "django_power_admin/widgets/Select2/js/Select2.js",
        ] + SELECT2_I18N_FILES + [
            "admin/js/jquery.init.js",
        ]
        css ={
            "all": [
                "admin/css/vendor/select2/select2.css",
            ]
        }

class SelectMultiple2(SelectMultiple):
    def __init__(self, attrs=None, choices=None):
        attrs = attrs or {}
        choices = choices or []
        if "class" in attrs:
            attrs["class"] += " django_power_admin_select2_multiple_widget"
        else:
            attrs["class"] = "django_power_admin_select2_multiple_widget"
        super().__init__(attrs=attrs, choices=choices)

    class Media:
        js=[
            "admin/js/vendor/jquery/jquery.js",
            "admin/js/vendor/select2/select2.full.js",
            "django_power_admin/widgets/SelectMultiple2/js/SelectMultiple2.js",
        ] + SELECT2_I18N_FILES + [
            "admin/js/jquery.init.js",
        ]
        css ={
            "all": [
                "admin/css/vendor/select2/select2.css",
            ]
        }

class PasswordResetableWidget(PasswordInput):
    pass

class ConfigTable(Textarea):
    template_name = "django_power_admin/widgets/ConfigTable.html"

    class Media:
        js=[
            "admin/js/vendor/jquery/jquery.js",
            "django_power_admin/widgets/ConfigTable/js/ConfigTable.js",
            "admin/js/jquery.init.js",
        ]
        css ={
            "all": [
                "fontawesome/css/all.min.css",
                "django_power_admin/widgets/ConfigTable/css/ConfigTable.css",
            ]
        }


class AllUsersSelect(Select2):
    def __init__(self,
            attrs=None,
            choices=None,
            user_info_template="{username} <{email}, {last_name}{first_name}>",
            empty_label="-"*10,
            get_users=None,
            get_user_info=None,
            ):
        super().__init__(attrs, choices)
        self.user_info_template = user_info_template
        self.get_user_info = get_user_info
        self.empty_label = empty_label
        self.get_users = get_users

    def get_all_users(self):
        request = get_request()
        cache_key = "DjangoPowerAdmin_Widgets_AllUsersSelect_AllUsers"
        if request:
            if hasattr(request, cache_key):
                return getattr(request, cache_key)
        if self.get_users:
            users = self.get_users()
        else:
            users = User.objects.filter(is_active=True, is_staff=True).all()
        if request:
            setattr(request, cache_key, users)
        return users
    
    def get_context(self, name, value, attrs):
        self.choices = [("", self.empty_label)]
        for user in self.get_all_users():
            if self.get_user_info:
                user_info = self.get_user_info(user)
            else:
                params = {
                    "username": user.username,
                    "email": user.email,
                    "last_name": user.last_name,
                    "first_name": user.first_name,
                }
                user_info = self.user_info_template.format(**params)
                user_info = user_info.replace(", >", ">")
                user_info = user_info.replace("<, ", "<")
                user_info = user_info.replace("<>", "")
            self.choices.append((user.pk, user_info))
        return super().get_context(name, value, attrs)
