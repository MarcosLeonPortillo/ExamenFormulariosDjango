from django import forms
from datetime import date
from django.utils import timezone
import datetime
from django.core.exceptions import ValidationError
# Lista de opciones
WEEKDAYS = [
    ('0','Lunes'),
    ('1','Martes'),
    ('2','Miércoles'),
    ('3','Jueves'),
    ('4','Viernes'),
    ('5','Sábado'),
    ('6','Domingo'),
]

class CalendarForm(forms.Form):
    date_from = forms.DateField(
        label='Fecha Desde',
        required=True,
        input_formats=['%d/%m/%Y'],
        initial= datetime.date.today,
        label_suffix = ":",
        help_text="dd/mm/YYYY",
    )

    date_to = forms.DateField(
        label='Fecha Hasta',
        required=False,
        input_formats=['%d/%m/%Y'],
        initial=None,
        label_suffix=":",
        help_text="dd/mm/YYYY"
    )

    weekdays = forms.MultipleChoiceField(
        label='Días de la semana',
        choices=WEEKDAYS,
        widget=forms.CheckboxSelectMultiple,
        initial=None,
        required=True,
        label_suffix=":",
        help_text="Elige al menos un día"
    )

    activity = forms.CharField(
        label='Actividad',
        required=True,
        max_length=20,
        label_suffix=":",
        initial=None,
        help_text="Introduce el título de la actividad",

    )

    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get("Fecha Desde")
        date_to = cleaned_data.get("Fecha Hasta")

        if date_to and (date_to - date_from).days < 6:
             raise ValidationError("La fecha hasta debe contemplar al menos 7 días de diferencia")

        return cleaned_data
