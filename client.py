class Client:
    

        def basicClient(self,data):
            """Constructor of Client basic data"""
            print(data)
            self.numeroCliente = data['customer']['myId']
            self.nombreCliente = data['customer']['name']
            return self

        
        def __init__(self,empresa, nombreCliente, contacto, direccion, grupoFacturacion, numeroCliente, latitud, longitud, tarifa, comuna, subestacion, poste, modeloMedidor, marcaMedidor):
            """Constructor of Client with full data"""
            self.empresa = empresa if empresa else ""
            self.nombreCliente = nombreCliente if nombreCliente else ""
            self.contacto = contacto if contacto else ""
            self.direccion = direccion if direccion else ""
            self.grupoFacturacion = grupoFacturacion if grupoFacturacion else ""
            self.numeroCliente = numeroCliente if numeroCliente else ""
            self.latitud = latitud if latitud else ""
            self.longitud = longitud if longitud else ""
            self.tarifa = tarifa if tarifa else ""
            self.comuna = comuna if comuna else ""
            self.subestacion = subestacion if subestacion else ""
            self.poste = poste if poste else ""
            self.modeloMedidor = modeloMedidor if modeloMedidor else ""
            self.marcaMedidor = marcaMedidor if marcaMedidor else ""


        def clientArray(values):
            clientArray = []
            for data in values:
                client = Client(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13])
                clientArray.append(client)

            return clientArray
        
        def clientOut(values):
            clientOutArray = []
            for data in values:
                clientOut = {'company': data[0],'id':data[1],'date':data[2]}
                clientOutArray.append(clientOut)

            return clientOutArray