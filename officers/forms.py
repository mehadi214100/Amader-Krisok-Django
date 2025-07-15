from .models import OfficerBook
from django import forms

class officerBookForm(forms.ModelForm):
    class Meta:
        model = OfficerBook
        

