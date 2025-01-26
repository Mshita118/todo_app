from django import forms
from .models import Task, Category, Comment


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed',
                  'category', 'priority', 'deadline']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'deadline': forms.NumberInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Category Description', 'rows': 3}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'title': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Add a comment...'}),
        }


class SortForm(forms.Form):
    SORT_CHOICES = [
        ('created_at', 'Created Date'),
        ('updated_at', 'Updated Date'),
        ('completed', 'Completed'),
        ('priority', 'Priority'),
        ('category', 'Category'),
        ('deadline', 'Deadline'),
    ]
    sort_by = forms.ChoiceField(choices=SORT_CHOICES, required=False, widget=forms.Select(
        attrs={'onchange': 'this.form.submit();'}))
