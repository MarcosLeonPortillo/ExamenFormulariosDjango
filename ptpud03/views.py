from django.shortcuts import render
from .forms import CalendarForm

# Create your views here.

def index(request):
        if request.method == 'GET':
            tablero_form = CalendarForm(request.GET)
        # Ejecutamos la validación
            if tablero_form.is_valid():
                # Los datos se obtienen del diccionario cleaned_data
                date_from = tablero_form.cleaned_data["Fecha Desde"]
                date_to = tablero_form.cleaned_data["Fecha Hasta"]
                weekdays = tablero_form.cleaned_data["Días  de la semana"]
                activity = tablero_form.cleaned_data["Actividad"]

                return render(request, 'ptpud03/index.html',
                              {"Fecha Desde": date_from, "Fecha Hasta": date_to,
                               "Días  de la semana": weekdays, "Actividad": activity, 'form':tablero_form})

        else:
            tablero_form = CalendarForm()
        return render(request,'ptpud03/index.html', {'form':tablero_form})

def calendar(request):
    if request.method == 'GET':
        tablero_form = CalendarForm(request.GET)
        # Ejecutamos la validación
        if tablero_form.is_valid():
            # Los datos se obtienen del diccionario cleaned_data
            date_from = tablero_form.cleaned_data["Fecha Desde"]
            date_to = tablero_form.cleaned_data["Fecha Hasta"]
            weekdays = tablero_form.cleaned_data["Días  de la semana"]
            activity = tablero_form.cleaned_data["Actividad"]

            return render(request, 'ptpud03/index.html',
                          {"Fecha Desde": date_from, "Fecha Hasta": date_to,
                           "Días  de la semana": weekdays, "Actividad": activity, 'form': tablero_form})

    else:
        tablero_form = CalendarForm()

    return render(request, 'ptpud03/calendar.html', {'form':tablero_form})
