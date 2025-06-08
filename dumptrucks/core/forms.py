from django import forms

class CoordinateForm(forms.Form):
    coordinates = forms.CharField(required=False, label='Координаты разгрузки (x y)')
