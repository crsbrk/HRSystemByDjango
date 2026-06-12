from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfileInfo, WorkApplication
from accounts.workers import worker_name_choices
from templates.constant_files import ORDER_TYPES, FAULTY_TYPES, MANUFA_TYPES


class UserForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ('password', 'email')


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('profile_phone', 'profile_pic', 'profile_site', 'profile_descption')


class WorkApplicationForm(forms.ModelForm):
    reviewer = forms.ModelChoiceField(
        queryset=User.objects.none(),
        label="审批人",
        required=True,
        empty_label="-- 请选择审批人 --",
    )

    class Meta():
        model = WorkApplication
        fields = (
            'work_type', 'reviewer',
            'title', 'score',
            'work_num', 'work_subtype', 'work_manufacturer',
            'work_date', 'work_progress',
            'workload_allot',
            'pj_participant1', 'workload_allot1',
            'pj_participant2', 'workload_allot2',
            'pj_participant3', 'workload_allot3',
            'description', 'evidence',
        )
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'work_date': forms.DateInput(attrs={'type': 'date'}),
            'workload_allot': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '1'}),
            'workload_allot1': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '1'}),
            'workload_allot2': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '1'}),
            'workload_allot3': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '1'}),
        }
        labels = {
            'work_num': '编号',
            'work_subtype': '子类型',
            'work_manufacturer': '厂家',
            'work_date': '相关日期',
            'work_progress': '当前进度(0~1)',
            'workload_allot': '比例1',
            'pj_participant1': '完成人员2',
            'workload_allot1': '比例2',
            'pj_participant2': '完成人员3',
            'workload_allot2': '比例3',
            'pj_participant3': '完成人员4',
            'workload_allot3': '比例4',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 审批人只能是管理员/审批人角色，且不能是超级管理员
        self.fields['reviewer'].queryset = User.objects.filter(
            userprofileinfo__role__in=['manager', 'approver'],
            is_superuser=False,
        ).distinct()
        # 显示姓名
        self.fields['reviewer'].label_from_instance = lambda u: '%s%s（%s）' % (
            u.last_name, u.first_name, u.username
        ) if (u.last_name or u.first_name) else u.username
        # 这些字段都是可选的（JS控制显示）
        for f in ('work_num', 'work_subtype', 'work_manufacturer', 'work_date', 'work_progress'):
            self.fields[f].required = False
        for f in ('pj_participant1', 'pj_participant2', 'pj_participant3'):
            self.fields[f] = forms.ChoiceField(
                choices=worker_name_choices(blank=True),
                required=False,
                label=self.fields[f].label,
            )
        for f in ('workload_allot', 'workload_allot1', 'workload_allot2', 'workload_allot3'):
            self.fields[f].required = False

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['workload_allot'] = cleaned_data.get('workload_allot') or 1

        for participant_field, ratio_field in (
            ('pj_participant1', 'workload_allot1'),
            ('pj_participant2', 'workload_allot2'),
            ('pj_participant3', 'workload_allot3'),
        ):
            if not cleaned_data.get(participant_field):
                cleaned_data[ratio_field] = 0
            elif not cleaned_data.get(ratio_field):
                raise ValidationError('已选择完成人员时，对应完成比例必须大于 0。')

        ratio_total = sum(cleaned_data.get(field) or 0 for field in (
            'workload_allot', 'workload_allot1', 'workload_allot2', 'workload_allot3'
        ))
        if ratio_total > 1:
            raise ValidationError('完成人员完成比例合计不能超过 1。')
        return cleaned_data
