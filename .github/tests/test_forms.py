import datetime
import pytest
from django import forms
from django.urls import resolve, reverse
from hypothesis import given, strategies as st, settings
from hypothesis.extra.django import from_form
from pytest_django.asserts import assertFormError, assertContains, assertTemplateUsed
from django.test import Client

from ptpud03 import views
from ptpud03.forms import CalendarForm, WEEKDAYS
from ptpud03.urls import urlpatterns
from ptpud03.utils import MonthsIterable

TEMPLATE_CALENDAR = 'ptpud03/calendar.html'

TEMPLATE_INDEX = 'ptpud03/index.html'

CALENDAR_PATH = '/calendar/'

LABEL_SUFFIX = ':'

INPUT_FORMAT = '%d/%m/%Y'

HELP_TEXT = 'dd/mm/YYYY'


# Arrange
@pytest.fixture
def form():
    return CalendarForm()


def test_form_date_from_field(form):
    field = form.declared_fields['date_from']
    # Comprueba que el atributo date_from es un DateField
    assert isinstance(field, forms.DateField)
    # Comprueba que el atributo date_from tiene el label correcto
    assert field.label == "Fecha Desde"
    # Comprueba que el atributo date_from tiene el label correcto
    assert field.label_suffix == LABEL_SUFFIX
    # Comprueba que el atributo date_from tiene atirbuto help_text='dd/mm/YYYY'
    assert field.help_text == HELP_TEXT
    # Comprueba que el atributo date_from es requerido
    assert field.required == True
    # Comprueba que el formato de entrada es correcto
    assert field.input_formats == [INPUT_FORMAT]
    # Comprueba que el atributo date_from tiene el valor por defecto del día actual
    assert field.initial == datetime.date.today


def test_form_date_to_field(form):
    field = form.declared_fields['date_to']
    # Comprueba que el atributo date_from es un DateField
    assert isinstance(field, forms.DateField)
    # Comprueba que el atributo date_from tiene el label correcto
    assert field.label == "Fecha Hasta"
    # Comprueba que el atributo date_from tiene el label correcto
    assert field.label_suffix == LABEL_SUFFIX
    # Comprueba que el atributo date_from tiene atirbuto help_text='dd/mm/YYYY'
    assert field.help_text == HELP_TEXT
    # Comprueba que el atributo date_from es requerido
    assert field.required == False
    # Comprueba que el formato de entrada es correcto
    assert field.input_formats == [INPUT_FORMAT]
    # Comprueba que el atributo date_from tiene el valor por defecto del día actual
    assert field.initial == None


def test_form_weekdays_field(form):
    field = form.declared_fields['weekdays']
    # Comprueba que el atributo date_from es un DateField
    assert isinstance(field, forms.MultipleChoiceField)
    # Comprueba que el atributo date_from tiene el label correcto
    assert field.label == "Días de la semana"
    # Comprueba que el atributo date_from tiene el label correcto
    assert field.label_suffix == LABEL_SUFFIX
    # Comprueba que el atributo date_from tiene atirbuto help_text='dd/mm/YYYY'
    assert field.help_text == "Elige al menos un día"
    # Comprueba que el atributo date_from es requerido
    assert field.required == True
    # Comprueba que el formato de entrada es correcto
    assert field.choices == WEEKDAYS
    # Comprueba que el atributo date_from tiene el valor por defecto del día actual
    assert field.initial == None
    # Comprueba que usa el widget CheckboxSelectMultiple
    assert isinstance(field.widget, forms.CheckboxSelectMultiple)


def test_form_activity_field(form):
    field = form.declared_fields['activity']
    # Comprueba que el atributo date_from es un DateField
    assert isinstance(field, forms.CharField)
    # Comprueba que el atributo date_from tiene el label correcto
    assert field.label == "Actividad"
    # Comprueba que el atributo date_from tiene el label correcto
    assert field.label_suffix == LABEL_SUFFIX
    # Comprueba que el atributo date_from tiene atirbuto help_text='dd/mm/YYYY'
    assert field.help_text == "Introduce el título de la actividad"
    # Comprueba que el atributo date_from es requerido
    assert field.required == True
    # Comprueba que el formato de entrada es correcto
    assert field.max_length == 20
    # Comprueba que el atributo date_from tiene el valor por defecto del día actual
    assert field.initial == None


@pytest.fixture
def form_no_week():
    data = {
        'date_from': '01/01/2021',
        'date_to': '06/01/2021',
        'weekdays': ['0', '1', '2', '3', '4', '5', '6'],
        'activity': 'Actividad 1'
    }
    return CalendarForm(data)


@pytest.fixture
def form_week():
    data = {
        'date_from': '01/01/2021',
        'date_to': '07/01/2021',
        'weekdays': ['0', '1', '2', '3', '4', '5', '6'],
        'activity': 'Actividad 1'
    }
    return CalendarForm(data)


def test_form_is_valid(form_no_week, form_week):
    assertFormError(form_no_week, field=None,
                    errors='La fecha hasta debe contemplar al menos 7 días de diferencia')
    assert form_week.is_valid()


@pytest.fixture
def index_needle(form):
    return (
        f'<form method="get" action="/calendar/"> \
          {form.as_div()}\
          <div>\
               <input type="submit" value="Enviar">')


def test_view_index_form(client, index_needle):
    response = client.get('/')
    assertContains(response, index_needle, html=True)
    assertTemplateUsed(response, TEMPLATE_INDEX)


def test_url_calendar():
    # comprueba si hay una url para calendar/ en urlpatterns
    resolver = resolve(CALENDAR_PATH, urlconf='ptpud03.urls')
    assert resolver.func == views.calendar


def test_view_calendar(client, form_no_week, form_week):
    view_calendar_form_no_valid(client, form_no_week)
    view_calendar_form_valid(client, form_week)


def view_calendar_form_no_valid(client, form_no_week):
    test_url_calendar()
    response = client.get(CALENDAR_PATH, form_no_week.data)
    assert response.status_code == 200
    assertTemplateUsed(response, TEMPLATE_INDEX)
    form = response.context['form']
    assertFormError(form, field=None,
                    errors='La fecha hasta debe contemplar al menos 7 días de diferencia')


def view_calendar_form_valid(client, form_week):
    test_url_calendar()
    response = client.get(CALENDAR_PATH, form_week.data)
    assert response.status_code == 200
    assertTemplateUsed(response, TEMPLATE_CALENDAR)


@pytest.fixture
def random_dates():
    return [(st.dates(min_value=datetime.date(2022, 6, 1),
                      max_value=datetime.date(2023, 2, 1)).example(),
             st.dates(min_value=datetime.date(2023, 2, 7),
                      max_value=datetime.date(2023, 12, 31)).example()) for x in range(5)]


def test_template_calendar_h1(random_dates):
    for date in random_dates:
        date_from = date[0]
        date_to = date[1]
        data = {
            'date_from': date_from.strftime(INPUT_FORMAT),
            'date_to': date_to.strftime(INPUT_FORMAT),
            'weekdays': ['0', '1'],
            'activity': 'Actividad 1'
        }
        client = Client()
        response = client.get(CALENDAR_PATH, data)
        assert response.status_code == 200
        assertTemplateUsed(response, TEMPLATE_CALENDAR)
        cadena = (f'Calendarios del\
                  {date_from.strftime(INPUT_FORMAT)}\
                  al\
                  {date_to.strftime(INPUT_FORMAT)}')
        assertContains(response, cadena, html=True)


def test_template_calendar_month_tittles(random_dates):
    for date in random_dates:
        date_from = date[0]
        date_to = date[1]
        data = {
            'date_from': date_from.strftime(INPUT_FORMAT),
            'date_to': date_to.strftime(INPUT_FORMAT),
            'weekdays': ['0', '1'],
            'activity': 'Actividad 1'
        }
        client = Client()
        response = client.get(CALENDAR_PATH, data)
        assert response.status_code == 200
        assertTemplateUsed(response, TEMPLATE_CALENDAR)

        months = MonthsIterable(date_from, date_to)
        date_to = months.date_to

        for month in months.months():
            cadena = (f'<h2>{month.month} / {month.year}')
            assertContains(response, cadena, html=True)


def test_template_calendar_monthly_tables(random_dates):
    for date in random_dates:
        date_from = date[0]
        date_to = date[1]
        data = {
            'date_from': date_from.strftime(INPUT_FORMAT),
            'date_to': date_to.strftime(INPUT_FORMAT),
            'weekdays': ['0', '1'],
            'activity': 'Actividad 1'
        }
        client = Client()
        response = client.get(CALENDAR_PATH, data)
        assert response.status_code == 200
        assertTemplateUsed(response, TEMPLATE_CALENDAR)

        months = MonthsIterable(date_from, date_to)
        date_to = months.date_to

        for month in months.months():
            html_tabla = cabecera_tabla_HTML()
            filas_html = filas_dias_tabla_HTML(month, data, date_from, date_to)
            html_tabla += filas_html

            assertContains(response, html_tabla, html=True)

def cabecera_tabla_HTML():
    return (f'<table>\
                        <thead>\
                        <th>Lunes</th>\
                        <th>Martes</th>\
                        <th>Miércoles</th>\
                        <th>Jueves</th>\
                        <th>Viernes</th>\
                        <th>Sábado</th>\
                        <th>Domingo</th>\
                        </thead>')

def filas_dias_tabla_HTML(month, data, date_from, date_to):
    cadena = ''
    for week in month.weeks:
        cadena += (f'<tr>')
        for day in week:
            cadena += (f'<td class="day">')
            if day.month == month.month:
                cadena += (f'{day.day}')
            cadena += (f'</td>')
        cadena += (f'</tr><tr>')
        for day in week:
            cadena += (f'<td class="content">')
            if day.month == month.month and day >= date_from and day <= date_to:
                if str(day.weekday()) in data['weekdays']:
                    cadena += (f'{data["activity"]}')
            cadena += (f'</td>')
        cadena += (f'</tr>')
    return cadena
