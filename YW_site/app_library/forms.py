from django import forms

class EquipmentSheetForm(forms.Form):
    name_of_submitter = forms.CharField(required=False)
    beginning_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)
    equipment = forms.CharField(required=False)
    date_submitted = forms.DateTimeField(widget=forms.HiddenInput(), required=False)
    image = forms.ImageField(required=False)