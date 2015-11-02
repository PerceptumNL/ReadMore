from django import forms
from main.models import Institute, TeacherCode

class StudentForm(forms.Form):
    students = forms.CharField(widget=forms.Textarea,
        label='Student data (id, first_name, last_name, group)')

class TeacherForm(forms.Form):
    institute = forms.ModelChoiceField(queryset=Institute.objects.all(),
        empty_label=None)
    teacher_code = forms.ModelChoiceField(queryset=TeacherCode.objects.all(),
        empty_label=None)
    teachers = forms.CharField(widget=forms.Textarea,
        label='Teacher data (id, first_name, last_name, group1; group2; ...)')
