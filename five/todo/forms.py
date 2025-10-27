from django import forms
from .models import ToDo

class ToDoForm(forms.ModelForm):
    due_date = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class' :'form-control'}),
                                   input_formats=['%Y-%m-%dT%H:%M'])
    completed = forms.BooleanField(required=False)
    
    class Meta:
        model = ToDo
        fields = ['name', 'description', 'due_date', 'completed']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.due_date:
            self.fields['due_date'].initial = self.instance.due_date.strftime('%Y-%m-%dT%H:%M')