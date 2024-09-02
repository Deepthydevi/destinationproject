from django import forms
from .models import Destination

class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = '__all__'
        widgets = {
            'place_name': forms.TextInput(attrs={'class': 'form-control'}),
            'weather': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'google_map_link': forms.URLInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
