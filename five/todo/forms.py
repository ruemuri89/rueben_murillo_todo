from django import forms
from .models import ToDo

class ToDoForm(forms.ModelForm):
    completed = forms.BooleanField(required=False)
    class Meta:
        model = ToDo
        fields = ['name', 'description', 'due_date', 'completed']