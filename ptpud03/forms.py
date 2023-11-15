from django import forms
from datetime import date
from django.utils import timezone
import datetime
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
