
import datetime
import json
import requests
import base64
from dotenv import load_dotenv
import os
from bcolors import bcolors
from client import Client

from customer_st import CustomerST
from medidor_st import MedidorST
from site_st import SiteST
from static_config import staticConfig


load_dotenv()


class SyncroTeam:
    """Class to interact with SyncroTeam API"""

    _st_url = os.getenv('ST_URL')
    _valueToken = f"{os.getenv('ST_CONFIG')}:{os.getenv('ST_KEY')}"
    _token = base64.b64encode(_valueToken.encode('utf-8')).decode('utf-8')
    _headers = {
        "Authorization": f"Basic {_token}",
        "Content-Type": "application/json"
    }

    def clientToCustomer(self, client):
        """Method to convert client to customer"""
        data = CustomerST(client).createJsonCustomer()
        json_data = json.dumps(data)
        return json_data

    def clientToSite(self, client, customer_id):
        """Method to convert client to site"""
        data = SiteST(client).createJsonSite(customer_id)
        json_data = json.dumps(data)
        return json_data

    def medidorToEquipment(self, medidor):
        """Method to convert medidor to equipment"""
        data = MedidorST(medidor).createJsonMedidor()
        json_data = json.dumps(data)
        return json_data

    def createCustomer(self, data):
        """Method to create a customer in ST"""
        urlToSend = f"{self._st_url}/customer/send"
        response = requests.post(url=urlToSend, headers=self._headers, data=data)
        self.printResponse(urlToSend,response)
        return response
    
    def getCustomer(self,idCustomer):
        """Method to get customer from ST"""
        urlToSend = f"{self._st_url}/customer/details?id={idCustomer}"
        response = requests.get(url=urlToSend,headers=self._headers)
        self.printResponse(urlToSend,response)
        return response
    
    def deleteCustomer(self,idCustomer):
        """Method to delete customer from ST"""
        # print(idCustomer)
        urlToSend = f"{self._st_url}/customer/delete?myId={idCustomer}"
        response = requests.delete(url=urlToSend,headers=self._headers)
        self.printResponse(urlToSend,response)
        return response

    def createEquipment(self, data):
        """Method to create a equipment in ST"""
        # print(data)
        urlToSend = f"{self._st_url}/equipment/send"
        response = requests.post(url=urlToSend, headers=self._headers, data=data)
        self.printResponse(urlToSend,response)
        if response.status_code == 200:
            return response
        else:
            dataLoad = json.loads(data)
            client = Client.basicClient(Client,dataLoad)
            customerSt = self.clientToCustomer(client)
            response = self.createCustomer(customerSt)
            if response.status_code == 200:
                response = requests.post(url=urlToSend, headers=self._headers, data=data)
                self.printResponse(urlToSend,response)
                return response
            else:
                return response

    def deleteEquipment(self, idEquipment):
        """Method to delete a equipment in ST"""
        urlToSend = f"{self._st_url}/equipment/delete?myId={idEquipment}"
        response = requests.delete(url=urlToSend, headers=self._headers)
        self.printResponse(urlToSend,response)
        return response
    
    def getEquipment(self,idEquipment):
        """Method to get equipment from ST"""
        urlToSend = f"{self._st_url}/equipment/details?id={idEquipment}"
        response = requests.get(url=urlToSend,headers=self._headers)
        self.printResponse(urlToSend,response)
        return response

    def getJobs(self,status):
        """Method to get jobs from ST"""
        nowDate = datetime.datetime.now()-datetime.timedelta(days=1)
        nowDateFormated = nowDate.strftime("%Y-%m-%d %H:%M:%S")
        # print(nowDateFormated)
        urlToSend = f"{self._st_url}/job/list?changedSince={nowDateFormated}&status={status}&pageSize=100"
        response = requests.get(url=urlToSend,headers=self._headers)
        self.printResponse(urlToSend,response)
        return response
    
    def getJob(self,idJob):
        """Method to get job from ST"""
        urlToSend = f"{self._st_url}/job/details?id={idJob}"
        response = requests.get(url=urlToSend,headers=self._headers)
        self.printResponse(urlToSend,response)
        return response
    
    def getSite(self,idSite):
        """Method to get site from ST"""
       
        urlToSend = f"{self._st_url}/site/details?id={idSite}"
        response = requests.get(url=urlToSend,headers=self._headers)
        self.printResponse(urlToSend,response)
        return response
    
    def deleteSite(self,idSite):
        """Method to delete site from ST"""
        urlToSend = f"{self._st_url}/site/delete?myId={idSite}"
        response = requests.delete(url=urlToSend,headers=self._headers)
        self.printResponse(urlToSend,response)
        return response
    
    def createSite(self,data):
        """Method to create site from ST"""
        urlToSend = f"{self._st_url}/site/send"
        response = requests.post(url=urlToSend,headers=self._headers,data=data)
        self.printResponse(urlToSend,response)
        return response
    
    def validateJob(self,idJob):
        """Method to update job from ST"""
        job = json.dumps({"id":idJob})
        urlToSend = f"{self._st_url}/job/validate"
        response = requests.post(url=urlToSend,data=job,headers=self._headers)
        self.printResponse(urlToSend,response)
        return response
    
    def printResponse(self,url,response):
        """Method to print response"""
        print(f"{bcolors.HEADER}{url}{bcolors.ENDC}")
        print(f"{bcolors.OKGREEN}{response.content}{bcolors.ENDC}")
        print(f"{bcolors.WARNING}----------------------------------------------------{bcolors.ENDC}")
        staticConfig.APICALLED = staticConfig.APICALLED + 1