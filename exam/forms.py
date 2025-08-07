# exam/forms.py

from django import forms

class UploadExamForm(forms.Form):
    exam_name = forms.CharField(label='Exam Name', max_length=100)  # <- changed here
    duration = forms.IntegerField(label='Duration (minutes)')
    json_file = forms.FileField(label='Upload JSON File')
