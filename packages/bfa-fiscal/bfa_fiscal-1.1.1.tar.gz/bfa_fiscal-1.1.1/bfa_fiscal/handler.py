
import os
import time
import sys
from decimal import Decimal
import datetime

from pyafipws.wsaa import WSAA
from pyafipws.wsfev1 import WSFEv1
from pyafipws.pyfepdf import FEPDF

from .comprobante import Comprobante
from .padron import Padron

class Handler:
	def __init__(self, *initialization, **kwargs):
		self.URL_WSAA = "https://wsaahomo.afip.gov.ar/ws/services/LoginCms?wsdl"
		self.URL_WS = "https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL"
		self.CUIT = 20259692432
		self.CERT = "./gbasisty.crt"
		self.PRIVATEKEY = "./gbasisty.key"
		self.CACHE = "./cache"
		self.FORMATO = "./factura.csv"
		self.CONF_PDF = dict (
			LOGO = "./logo.png",
			EMPRESA = "Basisty, Fuentes & Assoc.",
			MEMBRETE1 = "Maipu 239 1er Piso Of. 19",
			MEMBRETE2 = "Banfield",
			CUIT = "CUIT 20-25969243-2",
			IIBB = "IIBB 20259692432",
			IVA = "IVA Responsable Monotributo",
			INICIO = "Inicio de Actividad: 01/04/2006"
		)

		self.CREDENCIALES = dict (
			expirationTimestamp = None,
			Token = None,
			Sign = None
		)

		for dictionary in initialization:
			for key in dictionary:
				setattr(self, key, dictionary[key])
				
		for key in kwargs:
			setattr(self, key, kwargs[key])


	def facturar(self, reg):
		wsfev1 = WSFEv1()

		if self.CREDENCIALES["Sign"] is None or self.CREDENCIALES["Token"] is None:
			self.CREDENCIALES = self.generar_credenciales('wsfe')
	
		wsfev1.Token = self.CREDENCIALES["Token"]
		wsfev1.Sign = self.CREDENCIALES["Sign"]
		wsfev1.Cuit = self.CUIT
		wsfev1.Conectar(self.CACHE, self.URL_WS)

		fepdf = FEPDF()
		fepdf.CargarFormato(self.FORMATO)
		fepdf.FmtCantidad = "0.2"
		fepdf.FmtPrecio = "0.2"
		fepdf.CUIT = self.CUIT

		for k, v in self.CONF_PDF.items():
			fepdf.AgregarDato(k, v)

		if "homo" in self.URL_WSAA:
			fepdf.AgregarDato("motivos_obs", "Ejemplo Sin validez fiscal")

		hoy = datetime.date.today().strftime("%Y%m%d")
		
		cbte_id = {
			"FACTURA A": 1,
			"NOTA DEBITO A": 2,
			"NOTA CREDITO A": 3, 
			"FACTURA B": 6,
			"NOTA DEBITO B": 7,
			"NOTA CREDITO B": 8, 
			"FACTURA C": 11,
			"NOTA DEBITO C": 12,
			"NOTA CREDITO C": 13, 

		} [reg.get("tipo_comprobante", "FACTURA B")]

		doc_id = {
			"DNI": 96,
			"CUIT": 80,
			"CUIL": 86,
			"": 99
		} [reg.get("tipo_documento", "")]

		cbte = Comprobante (
			tipo_cbte = cbte_id, 
			punto_vta = reg.get("point_of_sale", 3), 
			fecha_cbte = hoy,
			cbte_nro = reg.get("nro"),
			tipo_doc = doc_id, 
			nro_doc = reg["documento_nro"],
			nombre_cliente = reg["nombre"],
			domicilio_cliente = reg["domicilio"],
			fecha_serv_desde = reg.get("periodo_desde"),
			fecha_serv_hasta = reg.get("periodo_hasta"),
			fecha_venc_pago = reg.get("venc_pago", None),
			voucher_number = reg.get("voucher_number", None),
			id_impositivo = reg.get("iva_category", 'Consumidor Final'),
			forma_pago = reg.get("forma_pago", None),
			concepto = reg.get("concepto", 1),
			custom_remito = reg.get("custom_pedido", 0),
			custom_pedido = reg.get("custom_pedido", 0),
		)
		
		for item in reg["items"]:
			cbte.agregar_item (
				ds = item["descripcion"],
				qty = item.get("cantidad", 1),
				precio = item.get("precio", 0),
				tasa_iva = item.get("tasa_iva", 21.),
				bonif = item.get("bonif", 0.00),
				umed = item.get("umed", 7),
			)

		ok = cbte.autorizar(wsfev1)
		
		nro = cbte.encabezado["cbte_nro"]
		print("Factura autorizada", nro, cbte.encabezado["cae"])
		
		if "homo" in self.URL_WS:
			cbte.encabezado["motivos_obs"] = "Ejemplo Sin validez fiscal"
		
		nombreArchivo = {
			1: "factura",
			2: "nota_debito",
			3: "nota_credito", 
			6: "factura",
			7: "nota_debito",
			8: "nota_credito", 
			11: "factura",
			12: "nota_debito",
			13: "nota_credito", 

		} [cbte_id]

		if cbte.encabezado["resultado"] == "A":
			ok = cbte.generar_qr()
			ok = cbte.generar_pdf(fepdf, f"/tmp/{nombreArchivo}_{nro}.pdf")
			print("PDF generado", ok)
		else:
			print("Comprobante no autorizado")

		resultado = dict (
			numero = nro,
			pdf = f"/tmp/{nombreArchivo}_{nro}.pdf"
		)

		return resultado


	def consultarPadron(self, cuit):
		if self.CREDENCIALES["Sign"] is None or self.CREDENCIALES["Token"] is None:
			self.CREDENCIALES = self.generar_credenciales("ws_sr_padron_a5")
		
		padron = Padron(self.CREDENCIALES, self.CUIT)

		return padron.consultarPadron(cuit)


	def generar_credenciales(self, servicio = "wsfe"):
		wsaa = WSAA()
		wsaa.CreateTRA(servicio, 36000)

		wsaa.Autenticar (
			service = servicio, 
			crt=self.CERT, 
			key=self.PRIVATEKEY,
			wsdl=self.URL_WSAA, 
			cache=self.CACHE, 
			debug=True
		)

		credenciales = dict (
			expirationTimestamp =  wsaa.ObtenerTagXml("expirationTime"),
			Token = wsaa.Token,
			Sign = wsaa.Sign
		)

		return credenciales
