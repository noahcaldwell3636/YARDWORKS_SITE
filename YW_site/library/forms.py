from django import forms


class EquipmentSheetGroup(forms.Form):
    name_of_submitter = forms.CharField(required=False)
    beginning_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)



class EquipmentSheetForm(forms.Form):
    equipment = forms.CharField(required=False)
    date_submitted = forms.DateTimeField(widget=forms.HiddenInput(), required=False)
    image = forms.ImageField(required=False)