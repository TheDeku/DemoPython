import client as client


class SiteST:
    """SiteST class"""

    def __init__(self, client):
        """Constructor of SiteST"""
        # Minimo debe tener name y address para crearse en ST y un ID o myId
        self.myId = client.numeroCliente if hasattr(client, "numeroCliente") else ""
        self.name = client.direccion if hasattr(client, "direccion") else ""
        self.address = client.direccion if hasattr(client, "direccion") else ""
        self.adressComplement = client.direccionComplementaria if hasattr(client, "direccionComplementaria") else ""
        self.contactEmail = client.contactoEmail if hasattr(client, "contactoEmail") else ""
        self.contactFax = client.contactoFac if hasattr(client, "contactoFax") else ""
        self.contactMobile = client.contactoTelefono if hasattr(client, "contactoTelefono") else ""
        self.lat = client.latitud if hasattr(client, "latitud") else ""
        self.lon = client.longitud if hasattr(client, "longitud") else ""

    def createJsonSite(self, customer_id):
        """Create a json with the site data"""
        data = {
            "myId": self.myId,
            "name": self.name,
            "address": self.address,
            "addressComplement": self.adressComplement,
            "contactEmail": self.contactEmail,
            "contactFax": self.contactFax,
            "contactMobile": self.contactMobile,
            "customer": {
                "id": customer_id
            },
            "position": {
                "latitude": self.lat,
                "longitude": self.lon
            }
        }
        return data
