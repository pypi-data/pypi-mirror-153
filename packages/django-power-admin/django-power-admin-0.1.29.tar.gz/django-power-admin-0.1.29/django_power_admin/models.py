import datetime

from fastutils import strutils
from fastutils import dictutils

from django.core.exceptions import FieldDoesNotExist
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from django_middleware_global_request.middleware import get_request

# -----------------------------------------------------------------------------
# simple share model related
# -----------------------------------------------------------------------------
class SimpleShareModel(models.Model):
    _is_simple_share_model = True
    _simple_share_model_owner_field_name = "owner"
    _member_class = None
    _member_class_fk_name = None

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="+", verbose_name=_("Owner"))

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        request = get_request()
        if not self.owner:
            self.owner = request.user
        result = super().save(*args, **kwargs)
        return result

    @classmethod
    def get_user_related_filters(cls, user):
        filters = Q(**{cls._simple_share_model_owner_field_name: user})
        if cls._member_class:
            member_instances = cls._member_class.objects.filter(user=user).values(cls._member_class_fk_name)
            pkids = set([member_instance[cls._member_class_fk_name] for member_instance in member_instances])
            filters |= Q(**{"pk__in": pkids})
        return filters

    @classmethod
    def get_user_related_objects(cls, user, queryset=None):
        queryset = queryset or cls.objects
        filters = cls.get_user_related_filters(user)
        return queryset.filter(filters)

class SimpleMemberModelBase(models.Model):
    OWNER = 10
    MANAGER = 20
    DEVELOPER = 30
    VISITOR = 40
    ROLES = [
        (OWNER, _("Owner")),
        (MANAGER, _("Manager")),
        (DEVELOPER, _("Developer")),
        (VISITOR, _("Visitor")),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+", verbose_name=_("User"))
    role = models.IntegerField(choices=ROLES, verbose_name=_("Role"))

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.pk)

def create_simple_member_model(MainModelClass, SimpleMemberModel=SimpleMemberModelBase, memberModelVerboseName=None, memberModelVerboseNamePlural=None):
    memberModelName = MainModelClass.__name__ + "Member"
    mainModelClassForeignKeyName = MainModelClass._meta.model_name

    class Meta:
        app_label = MainModelClass._meta.app_label
        verbose_name = memberModelVerboseName or memberModelName
        verbose_name_plural = memberModelVerboseNamePlural or memberModelName+"s"

    SimpleMemberModel = type(memberModelName, (SimpleMemberModel, ), {
        "__module__": MainModelClass._meta.__module__,
        "Meta": Meta,
        mainModelClassForeignKeyName: models.ForeignKey(MainModelClass, on_delete=models.CASCADE, related_name="+", verbose_name=MainModelClass._meta.verbose_name)
    })
    setattr(MainModelClass, "_member_class", SimpleMemberModel)
    setattr(MainModelClass, "_member_class_fk_name", mainModelClassForeignKeyName)
    return SimpleMemberModel

# -----------------------------------------------------------------------------
# simple export related
# -----------------------------------------------------------------------------
XLSX_CELL_SIZE_MAX = 32*1024

class DateRender(object):
    def __init__(self, format="%Y/%m/%d %H:%M:%S", empty_value="-"):
        self.format = format
        self.empty_value = empty_value

    def __call__(self, value):
        if not value:
            return self.empty_value
        else:
            return value.strftime(self.format)

class NoneRender(object):
    def __init__(self, display=_("NULL")):
        self.display = display

    def __call__(self, value):
        if value is None:
            return self.display
        else:
            return value

class BooleanRender(object):
    def __init__(self, true_display=_("TRUE"), false_display=_("FALSE")):
        self.true_display = true_display
        self.false_display = false_display
    
    def __call__(self, value):
        if value:
            return self.true_display
        else:
            return self.false_display

class NullBooleanRender(object):
    def __init__(self, null_display=_("NULL"), true_display=_("TRUE"), false_display=_("FALSE")):
        self.null_display = null_display
        self.true_display = true_display
        self.false_display = false_display
    
    def __call__(self, value):
        if value is None:
            return self.null_display
        if value:
            return self.true_display
        else:
            return self.false_display

SIMPLE_EXPORT_DEFAULT_RENDERS = {
    bool: NullBooleanRender(),
    datetime.datetime: DateRender(),
}

def lookup_model_value(obj, field):
    def lookup_model_value_simple(obj, field):
        value = getattr(obj, field)
        if callable(value):
            value = value()
        return value
    value = obj
    for fname in field.split("__"):
        value = lookup_model_value_simple(value, fname)
    return value

def split_field_value(value, size):
    """
    如果字符串长度超过单元格式的最大长度限制，则需要使用多列来存储。

    value: 字符串
    size: 列数

    返回值总是为size长度的字符串数组，如果有效数据不需要size个列，则使用None填充空余的列表
    """
    if value is None:
        return [None] * size
    if not isinstance(value, str):
        return [value] + [None] * (size - 1)
    values = strutils.chunk(value, XLSX_CELL_SIZE_MAX)
    if len(values) < size:
        values += [None] * (size - len(values))
    else:
        values = values[:size]
    return values

def get_simple_export_header(field_settings, model):
    """Get simple export header
    """
    header = []
    col = 0
    for field_setting in field_settings:
        col += 1
        label = field_setting.get("label", None)
        if label:
            header.append(str(label))
            continue
        header_name = field_setting.get("header", None)
        if header_name:
            header.append(str(header_name))
            continue
        field = field_setting.get("field", None)
        if not field:
            header.append(str(_("COLUMN#{}").format(col)))
            continue
        try:
            field_instance = model._meta.get_field(field)
        except FieldDoesNotExist:
            field_instance = None
        if field_instance:
            header.append(str(field_instance.verbose_name))
            continue
        field_instance = getattr(model, field, None)
        if field_instance:
            header_name = getattr(field_instance, "short_description", None)
            if header_name:
                header.append(str(header_name))
                continue
            header_name = getattr(field_instance, "label", None)
            if header_name:
                header.append(str(header_name))
                continue
            header.append(str(_("COLUMN#{}").format(col)))
            continue
    return header

def get_simple_export_data(queryset, field_settings):
    """Get queryset's export data, without header.
    """
    data = []
    idx0 = -1
    total = 0
    for item in queryset:
        total += 1
    for item in queryset:
        idx0 += 1
        idx1 = idx0 + 1
        row = []
        col = -1
        for field_setting in field_settings:
            col += 1
            field = field_setting.get("field", "")
            if field.lower() in ["loop.counter0", "loop.index0", "forloop.counter0", "forloop.index0"]: # 序号，从0开始
                field_value = idx0
            elif field.lower() in ["loop.counter1", "loop.index1", "forloop.counter1", "forloop.index1"]: # 序号，从1开始
                field_value = idx1
            elif field.lower() in ["", "_empty", "_empty_", "_blank", "_blank_", "空", "空列", "空白列", "保留", "保留列"]: # 空列
                field_value = None
            elif field.lower() in ["_constant", "_constant_", "_value", "_value_", "常数", "常数列", "常量", "常量列", "预置", "预置数据", "预置数据列表"]: # 常数列表
                field_value = field_setting.get("value", "")
            else: # 数据模型字段
                field_value = lookup_model_value(item, field)
            # 使用自定义渲染
            render = field_setting.get("render", None)
            if render and callable(render):
                field_value = render(field_value)
            # 如果未指定自定义渲染，对非（bool，datetime）等类型的数据使用默认渲染
            field_value_type = type(field_value)
            render = SIMPLE_EXPORT_DEFAULT_RENDERS.get(field_value_type, None)
            if render:
                field_value = render(field_value)
            # 如果值不为（str, int, float）等类型，强制转化为字符串
            if not isinstance(field_value, (type(None), str, int, float)):
                field_value = str(field_value)
            # 将数据保存到指定列表
            columns = field_setting.get("columns", col)
            if not isinstance(columns, (list, tuple, str)):
                columns = [columns]
            if len(columns) == 1: # 保存至1列表
                dictutils.update(row, str(columns[0]), field_value)
            else: # 分割保存到多个列表
                values = split_field_value(field_value, len(columns))
                for c, value in zip(columns, values):
                    dictutils.update(row, str(c), value)
        data.append(row)
    return data

def get_simple_export_default_field_settings(model, exclude_fields=None):
    """Get simple export default field settings
    """
    exclude_fields = exclude_fields or []
    field_settings = [{
        "field": "forloop.index1",
        "header": str(_("Index")),
    }]
    for field in model._meta.fields:
        if field.name in exclude_fields:
            continue
        if field.primary_key:
            header = str(_("Primary Key Field Name"))
        else:
            header = None
        if header:
            field_settings.append({
                "field": field.name,
                "header": header,
            })
        else:
            field_settings.append({
                "field": field.name,
            })
    return field_settings
