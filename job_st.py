
from dotenv import load_dotenv
import os
from datetime import datetime

from syncroteam import SyncroTeam


class jobST:

    def __init__(self, jsonJob):
        # print(jsonJob['position'])
        if jsonJob['position'] is None:
            self.pLatitud = 0
            self.pLongitud = 0
        else:
            self.pLatitud = jsonJob['position']['latitude']
            self.pLongitud = jsonJob['position']['longitude']
        self.pFecha = jsonJob['actualEnd'][0:10] 
        self.pFechaCierre = jsonJob['actualEnd'][0:10] 
        self.pHorarioInicio = jsonJob['scheduledStart']+':00'[11:20]
        self.pCierreHoraInicio = jsonJob['scheduledEnd']+':00'[11:20]
        self.pCierreHoraFin = jsonJob['actualEnd']+':00'[11:20]
        if jsonJob['myId'] == "":
            self.pIdSynchroteam = jsonJob['num']
        else:
            self.pIdSynchroteam = ""
        self.pBrigada = jsonJob['technician']['login']
        self.pServicio = int(jsonJob['customer']['myId'])

        responseCustomer = SyncroTeam().getCustomer(jsonJob['customer']['id'])
        jsonCustomer = responseCustomer.json()
        for custom in jsonCustomer['customFieldValues']:
           

            if custom['label'] is not None and custom['label'] == 'Empresa':
            
                self.pEmpresa = custom['value']
            else:
                self.pEmpresa = 'No informado'
        if jsonJob['type']['id'] == int(os.getenv('NORMALIZACION')): 
            self.pCuenta = 1  # value designated by client
        elif jsonJob['type']['id'] == int(os.getenv('INS_MONOFASICA')): 
            self.pCuenta = 2
        elif jsonJob['type']['id'] == int(os.getenv('INS_TELEMEDIDA')): 
            self.pCuenta = 3
        elif jsonJob['type']['id'] == int(os.getenv('INS_TRIFASICA')): 
            self.pCuenta = 18
        elif jsonJob['type']['id'] == int(os.getenv('INS_CONTROL_INT')): 
            self.pCuenta = 22
        elif jsonJob['type']['id'] == int(os.getenv('INS_MANTEN')):
            self.pCuenta = 23
        else:
            self.pCuenta = 1000
            print('No se reconoce el tipo de trabajo')

        # Values from report
        if jsonJob['report'][0]['items'] is not None:
            self.pEstado = ''
            self.pActividad = ''
            self.pMotivo = ''
            self.pResponsabilidad = ''
            self.pTipoCNR = ''
            self.pFNIE = 0
            self.pObservacion = ''
            estadoInspeccion = ''
            if jsonJob['report'][0]['items'] != []:
                for report in jsonJob['report'][0]['items']:
                    if report['name'] == 'Estado Inspeccion':
                        estadoInspeccion = report['value']
                   
                    if report['name'] == 'Tipo de Visita':
                        self.pEstado = report['value']
                   

                    if report['name'] == 'Actividad Normalizacion Propuesta':
                        self.pActividad = report['value'].split('|')
                    elif report['name'] == 'Actividad Normalizacion Realizada':
                        self.pActividad = report['value'].split('|')

                    if report['name'] == 'Motivo Normalizacion':
                        self.pMotivo = report['value']

                    if report['name'] == 'Responsabilidad Normalizacion Propuesta':
                        self.pResponsabilidad = report['value']

                    if self.pEstado == 'Visita':

                        if report['name'] == 'Sub-tipo Visita':
                            self.pTipoCNR = report['value']
                    
                    if estadoInspeccion == 'Sub-Registro':

                        if report['name'] == 'Tipo de Sub-Registro':
                            self.pEstado = estadoInspeccion 
                            self.pTipoCNR = report['value']
                    if estadoInspeccion == 'Normal': 
                        self.pEstado = estadoInspeccion 

                    if report['name'] == 'N-FNIE':
                        self.pFNIE = int(report['value'])
                    if report['name'] == 'Observacion':
                        self.pObservacion = report['value']

        self.pFechaIngreso = jsonJob['scheduledStart']+':00'
        self.pIngresoEstado = 'Subida'

        if jsonJob['customFieldValues'] is not None:
            if jsonJob['customFieldValues'] == []:
                self.pIngresoProcedencia = 'Autogenerado'
            else:
                for customField in jsonJob['customFieldValues']:
                    if customField['label'] == 'Procedencia':
                        self.pIngresoProcedencia = customField['value']

        self.pInspeccionId = 0
        self.pNormalizacion = 0

        if jsonJob['equipment'] is not None :
            self.pMedidor = jsonJob['equipment']['myId']
        else:
            self.pMedidor = 0
        self.materiales = []

        for material in jsonJob['parts']:
            pCodigoMaterial = material['reference']
            pCantidadMaterial = material['quantity']
            self.materiales.append(
                {'pCodigoMaterial': pCodigoMaterial, 'pCantidadMaterial': pCantidadMaterial})


    def __json__(self):
        return {
            "pLatitud": self.pLatitud,
            "pLongitud": self.pLongitud,
            "pFecha": self.pFecha,
            "pFechaCierre": self.pFechaCierre,
            "pHorarioInicio": self.pHorarioInicio,
            "pCierreHoraInicio": self.pCierreHoraInicio,
            "pCierreHoraFin": self.pCierreHoraFin,
            "pBrigada": self.pBrigada,
            "pServicio": self.pServicio,
            "pEmpresa": self.pEmpresa,
            "pCuenta": self.pCuenta,
            "pEstado": self.pEstado,
            "pActividad": self.pActividad,
            "pFechaIngreso": self.pFechaIngreso,
            "pIngresoEstado": self.pIngresoEstado,
            "pIngresoProcedencia": self.pIngresoProcedencia,
            "pInspeccionId": self.pInspeccionId,
            "pNormalizacion": self.pNormalizacion,
            "pMedidor": self.pMedidor,
            "pMotivo": self.pMotivo,
            "pResponsabilidad": self.pResponsabilidad,
            "pTipoCNR": self.pTipoCNR,
            "pFNIE": self.pFNIE,
            "pObservacion": self.pObservacion,
            "pIdSynchroteam": self.pIdSynchroteam,
            "materiales": self.materiales

        }