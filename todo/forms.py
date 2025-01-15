from django import forms
from .models import Task, Category


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed', 'category']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
