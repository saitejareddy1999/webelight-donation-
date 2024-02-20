from django import forms

from number.models import Number


class NumberForm(forms.ModelForm):
    class Meta:
        model = Number
        exclude = ['created_at']

    def __init__(self, *args, **kwargs):
        super(NumberForm, self).__init__(*args, **kwargs)
        self.fields['receiver_phone_number'].widget.attrs['placeholder'] = 'enter receiver phone number'
        self.fields['amount'].widget.attrs['placeholder'] = 'enter amount to donate'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
