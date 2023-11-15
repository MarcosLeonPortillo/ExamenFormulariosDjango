import calendar
from datetime import timedelta

class Month:
    '''
    Esta clase nos proporciona un envoltorio para mandar al template la información de un mes
    month = numero del mes
    year = numero del año
    weeks = Lista con 7 objetos de tipo datetime.date representando de Lunes a Domingo
    '''
    def __init__(self, month, year, weeks):
        self.month = month
        self.year = year
        self.weeks = weeks

class MonthsIterable:
    '''
    Clase que permite crear una lista de objetos Month entre dos fechas
    '''
    def __init__(self, date_from, date_to=None):
        '''
        Construye el objeto. Si no se pasa date_to o es vacío, se establece date_to a date_from + 30 días
        '''
        self.date_from = date_from
        self.date_to = date_to if date_to else date_from + timedelta(days=30)

    def months(self):
        '''
        Este método opera con las propiedades date_from y date_to del objeto para devolver
        una lista de objetos tipo Month
        '''

        #Creamos variables iniciales para operar
        months = []
        month_from = self.date_from.month
        year_from = self.date_from.year
        month_to = self.date_to.month
        year_to = self.date_to.year
        cal = calendar.Calendar()

        # Itera desde el mes de incicio al mes de fin creando un objeto Month en cada paso
        while year_from < year_to or (year_from == year_to and month_from <= month_to):
            weeks = cal.monthdatescalendar(year=year_from, month=month_from)
            month_wrapper = Month(month_from,year_from,weeks)
            months.append(month_wrapper)
            # Aumenta uno al mes controlando el cambio de año
            if month_from == 12:
                month_from = 0
                year_from += 1
            month_from += 1

        return months # Devuelve los meses creados
