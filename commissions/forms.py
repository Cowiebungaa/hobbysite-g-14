from django import forms
from django.utils.translation import gettext_lazy as
from .models import Commission, JobCommission, JobCommissionApplication


class JobCommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = ['title', 'description', 'author', 'status']
        widgets = {
            'author': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    created_at = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), initial='Current Time')
    updated_at = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), initial='Current Time')


class JobCommissionApplicationForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['role', 'personnelRequired', 'status']