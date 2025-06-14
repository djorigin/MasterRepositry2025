from django import forms
from .models import RJ45Pinout, RJ45Pin, Supplier

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

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            'name', 'legal_name', 'website', 'email', 'phone', 'street_address',
            'city', 'state', 'postal_code', 'country', 'tax_id',
            'is_manufacturer', 'is_active', 'notes'
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if getattr(field.widget, 'input_type', None) == 'checkbox':
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        name = self.cleaned_data['name']
        # Example business logic: enforce capitalization
        return name.title()
    
    # Add more clean_<field> methods or clean() for business logic as needed