
import json
from dotenv import load_dotenv
import os
from bcolors import bcolors
from client import Client

from db_conection import DBConnection
from job_st import jobST
from medidor import Medidor
from sp_object import spObject
from syncroteam import SyncroTeam

load_dotenv()


class ProcessData:

    _host = os.getenv('HOST_ACP')
    _user = os.getenv('USER_BD_ACP')
    _password = os.getenv('PASSWORD_ACP')
    _db_dest = os.getenv('BD_ACP')

    def processCustomers(self):
        db = DBConnection(self._host, self._user,
                          self._password, self._db_dest)
        db.connect()
        data_bd = db.execute_query("SELECT * FROM acp.v_clientes")
        client = Client.clientArray(data_bd)
        for client in client:
            data = SyncroTeam().clientToCustomer(client)
            # print(f"{bcolors.OKBLUE}JSON del cliente{bcolors.ENDC}")
            # print(f"{bcolors.OKCYAN}{data}{bcolors.ENDC}")
            # se ejecuta n veces segun la cantidad de clientes
            stClient = SyncroTeam().createCustomer(data)
            stClientJson = json.loads(stClient.content)
            # print("Cliente creado en SyncroTeam")
            # print(stClientJson['id'])
            dataSite = SyncroTeam().clientToSite(client, stClientJson['id'])
            # print(f"{bcolors.OKBLUE}JSON del sitio{bcolors.ENDC}")
            # print(f"{bcolors.OKGREEN}{dataSite}{bcolors.ENDC}")
            siteST = SyncroTeam().createSite(dataSite)

        db.disconnect()

    def processCustomerOut(self):
        db = DBConnection(self._host, self._user,
                          self._password, self._db_dest)
        db.connect()
        data_bd = db.execute_query("SELECT * FROM acp.v_clientes_baja")
        print(data_bd)
        clientOut = Client.clientOut(data_bd)
        for client in clientOut:
            SyncroTeam().deleteCustomer(client['id'])
            SyncroTeam().deleteSite(client['id'])

    def processEquipmentOut(self):
        db = DBConnection(self._host, self._user,
                          self._password, self._db_dest)
        db.connect()
        data_bd = db.execute_query("SELECT * FROM acp.v_medidores_baja")
        medidorOut = Medidor.medidorOut(data_bd)

        for medidor in medidorOut:
            SyncroTeam().deleteEquipment(medidor['serie_medidor'])

    def processEquipment(self):
        db = DBConnection(self._host, self._user,
                          self._password, self._db_dest)
        db.connect()
        data_bd = db.execute_query("SELECT * FROM acp.v_medidores")
        medidores = Medidor.medidorArray(data_bd)
        for equipment in medidores:
            data = SyncroTeam().medidorToEquipment(equipment)

            SyncroTeam().createEquipment(data)
        db.disconnect()

    def processJobs(self, status):
        print(
            f"{bcolors.HEADER}{bcolors.BOLD}***Inicio Traspaso Informacion ST a ACP***{bcolors.ENDC}")
        db = DBConnection(self._host, self._user,
                          self._password, self._db_dest)
        statusDb = False
        while statusDb == False:
            statusDb = db.connect()

        listResponse = SyncroTeam().getJobs(status)  # se ejecuta una vez
        # print(listResponse.content)
        jsonJobs = listResponse.json()
        for job in jsonJobs['data']:
            jobResponse = SyncroTeam().getJob(job['id'])
            # print(jobResponse.content)
            print(jobResponse.json()['reportTemplate'])
            newJob = jobST(jobResponse.json())
            if newJob.pMedidor == 0:
                print(
                    f"{bcolors.FAIL}No se encontro medidor en el trabajo: {newJob.pIdSynchroteam}{bcolors.ENDC}")
                newJob.pCuenta = 1000
            json_string = json.dumps(newJob, default=lambda o: o.__json__())
            print(f"{bcolors.HEADER}***Objeto creado***{bcolors.ENDC}")
            print(f"{bcolors.OKCYAN}{json_string}{bcolors.ENDC}")
            if (newJob.pCuenta == 1000):
                print(
                    f"{bcolors.FAIL}No se pudo procesar {newJob.pServicio}{bcolors.ENDC}")
                continue

            cursor = db.conexion.cursor()
            result = cursor.callproc('sp_registro_inspeccion', (newJob.pLatitud,
                                                                newJob.pLongitud,
                                                                newJob.pFecha,
                                                                newJob.pHorarioInicio,
                                                                newJob.pBrigada,
                                                                newJob.pServicio,
                                                                newJob.pEmpresa,
                                                                newJob.pCuenta,
                                                                newJob.pEstado,
                                                                newJob.pFechaIngreso,
                                                                newJob.pIngresoEstado,
                                                                newJob.pIngresoProcedencia,
                                                                newJob.pTipoCNR,
                                                                newJob.pFNIE,
                                                                newJob.pObservacion,
                                                                newJob.pIdSynchroteam,
                                                                '',  # respuesta
                                                                0,))
            # print(result)
            data = spObject().registroActividad(result)
            value = spObject(**data)
            print(f"{bcolors.HEADER}***resultado registro***{bcolors.ENDC}")
            print(f"{bcolors.OKBLUE}{data}{bcolors.ENDC}")
            id_inspeccion = value.id
            if id_inspeccion == "None":
                id_inspeccion = "error"
            else:
                newJob.pInspeccionId = int(id_inspeccion)
                result_normalizacion = cursor.callproc('sp_normalizacion', (newJob.pBrigada,
                                                                            newJob.pFechaIngreso,
                                                                            newJob.pFecha,
                                                                            newJob.pServicio,
                                                                            newJob.pEmpresa,
                                                                            newJob.pIngresoProcedencia,
                                                                            newJob.pInspeccionId,
                                                                            newJob.pMedidor,
                                                                            newJob.pIngresoEstado,
                                                                            newJob.pLatitud,
                                                                            newJob.pLongitud,
                                                                            '0',  # respuesta
                                                                            0))
                print(f"{bcolors.HEADER}***resultado normalizacion***{bcolors.ENDC}")
                print(f"{bcolors.OKBLUE}{result_normalizacion}{bcolors.ENDC}")
                newJob.pNormalizacion = result_normalizacion[12]

                for i, actividad in enumerate(newJob.pActividad):

                    if actividad != "":
                        result_act_normalizacion = cursor.callproc('sp_actividad_normalizacion', (newJob.pNormalizacion,
                                                                                                  actividad,
                                                                                                  newJob.pFecha,
                                                                                                  newJob.pCuenta,
                                                                                                  newJob.pIngresoEstado,
                                                                                                  newJob.pBrigada,
                                                                                                  newJob.pFechaCierre,  
                                                                                                  newJob.pCierreHoraInicio,  
                                                                                                  newJob.pCierreHoraFin, 
                                                                                                  newJob.pMotivo, 
                                                                                                  newJob.pResponsabilidad, 
                                                                                                  '',
                                                                                                  ))
                        print(
                            f"{bcolors.HEADER}***resultado actividad normalizacion***{bcolors.ENDC}")
                        print(
                            f"{bcolors.OKBLUE}{result_act_normalizacion}{bcolors.ENDC}")


                        if i == 0:
                            for material in newJob.materiales:
                                result_mat_norma = cursor.callproc('sp_material_normalizacion', (material['pCodigoMaterial'],
                                                                                                 newJob.pInspeccionId,
                                                                                                 actividad,
                                                                                                 int(
                                                                                                     material['pCantidadMaterial']),
                                                                                                 ''
                                                                                                 ))
                                print(
                                    f"{bcolors.HEADER}***resultado material normalizacion***{bcolors.ENDC}")
                                print(
                                    f"{bcolors.OKBLUE}{result_mat_norma}{bcolors.ENDC}")
                        result_act_inspeccion = cursor.callproc('sp_actividad_inspeccion', (newJob.pInspeccionId,
                                                                                            actividad,
                                                                                            newJob.pBrigada,
                                                                                            newJob.pFecha,
                                                                                            ''
                                                                                            ))
                        print(
                            f"{bcolors.HEADER}***resultado actividad inspeccion***{bcolors.ENDC}")
                        print(
                            f"{bcolors.OKBLUE}{result_act_inspeccion}{bcolors.ENDC}")

                print(
                    f"{bcolors.WARNING}----------------------------------------------------{bcolors.ENDC}")
                SyncroTeam().validateJob(job['id'])
