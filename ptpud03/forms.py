from django import forms

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
    '''
    Formulario para el registro de actividades en en un calendario
    '''
