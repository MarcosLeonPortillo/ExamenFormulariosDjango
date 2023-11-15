from django.shortcuts import render


# Create your views here.

def index(request):
    '''
    Este view se debe ocupar de alojar la inicialización del formulario de registro de actividad
    '''
    return render(request,'ptpud03/index.html', {})

def calendar(request):
    '''
    Este view se debe encargar de procesar el envío del formulario de registro de actividad
    '''
    '''
        Este view se debe encargar de procesar el envío del formulario de registro de actividad
        '''
    return render(request, 'ptpud03/calendar.html', {})
