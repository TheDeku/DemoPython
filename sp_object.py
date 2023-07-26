from bcolors import bcolors


class spObject:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def registroActividad(self, data):
        values = ['latitud',
                     'longitud',
                     'fecha',
                     'horarioInicio',
                     'brigada',
                     'servicio',
                     'empresa',
                     'cuenta',
                     'estado',
                     'fechaIngreso',
                     'ingresoEstado',
                     'ingresoProcedencia',
                     'tipoCNR',
                     'FNIE',
                     'observacion',
                     'idSyncroteam',
                     'status', 
                     'id']
        data_dict = {value: data for value, data in zip(values, data)}
        return data_dict
        print(f"{bcolors.HEADER}***resultado transformacion***{bcolors.ENDC}")
        print(f"{bcolors.OKBLUE}{data_dict}{bcolors.ENDC}")
