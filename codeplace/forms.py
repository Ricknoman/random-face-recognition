from django import forms
from .models import uploadedimage

class imageform(forms.ModelForm):
    class Meta:
        model = uploadedimage
        fields = ['image']