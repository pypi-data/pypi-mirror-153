import zeep
from zeep.helpers import serialize_object

class Padron:
	def __init__(self, authentication, CUIT):
		self.authentication = authentication
		self.CUIT = CUIT

	def consultarPadron(self, cuit):
		padron = {}

		try:
			soapClient = zeep.Client (
				wsdl="https://aws.afip.gov.ar/sr-padron/webservices/personaServiceA5?WSDL"
			)

			reporte = serialize_object (
				soapClient.service.getPersona (
					self.authentication["Token"], 
					self.authentication["Sign"], 
					self.CUIT, 
					cuit
				)
			)

			if reporte["datosGenerales"] is None:
				raise Exception(reporte["errorConstancia"]["error"][0])
			
			padron["surname"] = reporte["datosGenerales"]["apellido"]
			padron["name"] = reporte["datosGenerales"]["nombre"]
			padron["businessName"] = reporte["datosGenerales"]["razonSocial"]
			padron["cuit"] = reporte["datosGenerales"]["idPersona"]
			padron["address1"] = reporte["datosGenerales"]["domicilioFiscal"]["direccion"]
			padron["address2"] = "CP {}, {}, {}".format (
				reporte["datosGenerales"]["domicilioFiscal"]["codPostal"], 
				reporte["datosGenerales"]["domicilioFiscal"]["localidad"], 
				reporte["datosGenerales"]["domicilioFiscal"]["descripcionProvincia"] 
			)

			padron["IVACategory"] = None
			
			if reporte["datosMonotributo"] is not None:
				padron["IVACategory"] = "RESPONSABLE MONOTRIBUTO"
			else:
				for impuesto in reporte["datosRegimenGeneral"]["impuesto"]:
					if impuesto["idImpuesto"] == 30:
						padron["IVACategory"] = "RESPONSABLE INSCRIPTO"
					elif impuesto["idImpuesto"] == 32:
						padron["IVACategory"] = "EXENTO"
		except:
			raise

		return padron