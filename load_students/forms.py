from django import forms
from django.utils.safestring import mark_safe

class StudentForm(forms.Form):
    students = forms.CharField(widget=forms.Textarea,
        label='Student data (id, first_name, last_name, group)')

