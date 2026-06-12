"""动态员工名单工具。

员工名单不再写死在代码里，而是从注册用户（排除超级管理员）实时生成。
新员工注册后会自动出现在业务录入的下拉选项与 scores 排名中。
"""
from django import forms


def worker_display_name(user):
    name = '%s%s' % (user.last_name, user.first_name)
    return name or user.get_full_name() or user.username


def get_worker_names():
    """返回所有注册员工的展示姓名（排除超级管理员），按注册时间排序。"""
    from django.contrib.auth.models import User
    names = []
    for user in User.objects.filter(is_superuser=False).order_by('date_joined', 'id'):
        name = worker_display_name(user)
        if name and name not in names:
            names.append(name)
    return names


def worker_name_choices(blank=True):
    choices = [(name, name) for name in get_worker_names()]
    if blank:
        choices = [('', '---------')] + choices
    return choices


def make_worker_admin_form(model_cls, leader_fields=('pj_leader',), optional_fields=()):
    """生成一个 ModelForm，把指定的人员字段渲染成动态下拉（注册用户）。

    - leader_fields: 必填的人员字段
    - optional_fields: 可选的人员字段
    历史数据中已存在但当前未注册的姓名也会被补进选项，避免编辑旧记录时校验失败。
    """

    class _WorkerAdminForm(forms.ModelForm):
        class Meta:
            model = model_cls
            fields = '__all__'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            base = worker_name_choices(blank=False)
            existing = {value for value, _ in base}

            for field_name in tuple(leader_fields) + tuple(optional_fields):
                if field_name not in self.fields:
                    continue
                required = field_name in leader_fields
                current = getattr(self.instance, field_name, '') if self.instance else ''
                choices = list(base)
                if current and current not in existing:
                    choices = [(current, '%s（历史）' % current)] + choices
                if not required:
                    choices = [('', '---------')] + choices
                self.fields[field_name] = forms.ChoiceField(
                    choices=choices,
                    required=required,
                    label=self.fields[field_name].label,
                )

    return _WorkerAdminForm
