import client as client


class CustomerST:
    """Class to create a customer in ST"""

    def __init__(self, client):
        """Constructor of CustomerST"""
        self.myId = client.numeroCliente if hasattr(client, "numeroCliente") else ""
        self.name = client.nombreCliente if hasattr(client, "nombreCliente") else "Sin Información"
        self.address = client.direccion if hasattr(client, "direccion") else ""
        self.adressComplement = client.direccionComplementaria if hasattr(client, "direccionComplementaria") else ""
        self.contactEmail = client.contactoEmail if hasattr(client, "contactoEmail") else ""
        self.contactFirstName = client.contactoNombre if hasattr(client, "contactoNombre") else ""
        self.contactFax = client.contactoFac if hasattr(client, "contactoFax") else ""
        self.contactPhone = client.contactoTelefono if hasattr(client, "contactoTelefono") else ""
        self.contactLastName = client.contactoApellido if hasattr(client, "contactoApellido") else ""
        ##Custom Fields
        self.cusomTarifa = client.tarifa if hasattr(client, "tarifa") else ""
        self.customComuna = client.comuna if hasattr(client, "comuna") else ""
        self.customSe = client.subestacion if hasattr(client, "subestacion") else ""
        self.customPoste = client.poste if hasattr(client, "poste") else ""
        self.customModeloMedidor = client.modeloMedidor if hasattr(client, "modeloMedidor") else ""
        self.empresa = client.empresa if hasattr(client, "empresa") else ""
        ##Position
        self.lat = client.latitud if hasattr(client, "latitud") else ""
        self.lon = client.longitud if hasattr(client, "longitud") else ""

    def createJsonCustomer(self):
        """Create a json with the customer data"""
        data = {
            "myId": self.myId,
            "name": self.name,
            "address": self.address,
            "addressComplement": self.adressComplement,
            "contactEmail": self.contactEmail,
            "contactFirstName": self.contactFirstName,
            "contactFax": self.contactFax,
            "contactPhone": self.contactPhone,
            "contactLastName": self.contactLastName,
            "customFieldValues": [{
                # "id": int(os.getenv('ST_TARIFA')),
                "label": "Tarifa",
                "value": self.cusomTarifa
            },
                {
                # "id": int(os.getenv('ST_COMUNA')),
                "label": "Comuna",
                "value": self.customComuna

            }, {
                # "id": int(os.getenv('ST_SE')),
                "label": "S/E",
                "value": self.customSe

            }, {
                # "id": int(os.getenv('ST_POSTE')),
                "label": "Poste",
                "value": self.customPoste

            }, {
                # "id": int(os.getenv('ST_MEDIDOR')),
                "label": "Modelo Medidor",
                "value": self.customModeloMedidor

            }, {
                # "id": int(os.getenv('ST_EMPRESA')),
                "label": "Empresa",
                "value": self.empresa

            }],
            "position" : {
                "latitude": self.lat,
                "longitude": self.lon
            }
        }
        return data
