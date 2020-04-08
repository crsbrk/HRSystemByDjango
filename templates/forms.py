from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from crispy_forms.layout import Field
from scores.models import Attitude,Responsibility,Discipline


class AttitudeForm(forms.ModelForm):
    class Meta():
        model = Attitude
        exclude = ['worker_name','year_season']

class DisciplineForm(forms.ModelForm):
    class Meta():
        model = Discipline
        exclude = ['worker_name','year_season']
class ResponsibilityForm(forms.ModelForm):
    class Meta():
        model = Responsibility
        exclude = ['worker_name','year_season']

class CustomEmailbox(Field):
    template = 'accounts/custom_emailbox.html'

class NameForm(forms.Form):
	your_name = forms.CharField(label='Your name', max_length=100)
	your_phone = forms.CharField(max_length=100)
	message = forms.CharField(widget=forms.Textarea)
	sender = forms.EmailField()
	cc_myself = forms.BooleanField(required=False)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
            Row(
                Column('your_name', css_class='form-group col-md-6 mb-0'),
                Column('your_phone', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'message',

            Row(
				CustomEmailbox('sender'),
                css_class='form-row'
            ),
            'cc_myself',
            Submit('submit', 'Sign in')
        )	