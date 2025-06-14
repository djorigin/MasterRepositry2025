from django import forms
from .models import RJ45Pinout, RJ45Pin

class RJ45PinoutForm(forms.ModelForm):
    class Meta:
        model = RJ45Pinout
        fields = '__all__'  # or list the fields you want

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if getattr(field.widget, 'input_type', None) == 'checkbox':
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

class RJ45PinForm(forms.ModelForm):
    class Meta:
        model = RJ45Pin
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if getattr(field.widget, 'input_type', None) == 'checkbox':
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'