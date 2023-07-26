class Medidor:

    def __init__(self, direccion, marcaMedidor, serieMedidor, numeroCliente, ultimaLectura, ultimoConsumo, empresa, constante, modeloMedidor, propiedadMedidor):
        self.direccion = direccion if direccion else ""
        self.marcaMedidor = marcaMedidor if marcaMedidor else ""
        self.serieMedidor = serieMedidor if serieMedidor else ""
        self.numeroCliente = numeroCliente if numeroCliente else ""
        self.ultimaLectura = ultimaLectura if ultimaLectura else ""
        self.ultimoConsumo = ultimoConsumo if ultimoConsumo else ""
        self.empresa = empresa if empresa else ""
        self.constante = constante if constante else ""
        self.modeloMedidor = modeloMedidor if modeloMedidor else ""
        self.propiedadMedidor = propiedadMedidor if propiedadMedidor else ""

    def medidorArray(values):
        medidorArray = []
        for data in values:
            medidor = Medidor(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8],data[9])
            medidorArray.append(medidor)

        return medidorArray
    
    def medidorOut(values):
        medidorOutArray = []
        for data in values:
            medidorOut = {'marca_medidor': data[0],'serie_medidor':data[1],'numero_cliente':data[2],'empresa':data[3],'constante':data[4],'modelo_medidor':data[5],'fech_retiro':data[6]}
            medidorOutArray.append(medidorOut)

        return medidorOutArray