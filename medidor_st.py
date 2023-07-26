

class MedidorCustomerST:
    def __init__(self, myID, name):
        """Constructor of MedidorCustomerST"""
        self.myID = myID
        self.name = name

class MedidorST:

    def __init__(self, medidor):
        """Constructor of MedidorST"""
        self.myID = medidor.serieMedidor if medidor.serieMedidor else ""
        self.name = medidor.marcaMedidor if medidor.marcaMedidor else ""
        self.medidorCustomerST = MedidorCustomerST(medidor.numeroCliente if hasattr(medidor, 'numeroCliente') else ""
                                                   ,medidor.nombreCliente if hasattr(medidor, 'nombreCliente') else "no informado")
        ##Custom Fields
        self.lastLeture = medidor.ultimaLectura if medidor.ultimaLectura else ""
        self.lastConsumption = medidor.ultimoConsumo if medidor.ultimoConsumo else ""
        self.property = medidor.propiedadMedidor if medidor.propiedadMedidor else ""
        self.constant = medidor.constante if medidor.constante else ""
        self.model = medidor.modeloMedidor if medidor.modeloMedidor else ""


    def createJsonMedidor(self):
        """Create a json with the medidor data"""
        data = {
            "myId": self.myID,
            "name": self.name,
            "customer":{
                "myId": self.medidorCustomerST.myID,
                "name": self.medidorCustomerST.name
            },
            "customFieldValues": [{
                "label": "Última Lectura",
                "value": self.lastLeture
            },
                {
                "label": "Último Consumo",
                "value": self.lastConsumption

            }, {
                "label": "Propiedad",
                "value": self.property

            }, {
                "label": "Constante",
                "value": self.constant

            }, {
                "label": "Modelo",
                "value": self.model

            }]
        }
        return data

