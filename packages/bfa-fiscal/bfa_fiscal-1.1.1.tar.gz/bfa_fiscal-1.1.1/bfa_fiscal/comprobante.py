
import warnings
import qrcode
import json
import base64

class Comprobante:

	
	def __init__(self, **kwargs):
		self.encabezado = dict (
			tipo_doc = 99,
			nro_doc = 0,
			cuit = 0,
			tipo_cbte = 6, 
			cbte_nro = None, 
			punto_vta = 4000, 
			fecha_cbte = None,
			imp_total = 0.00, 
			imp_tot_conc = 0.00, 
			imp_neto = 0.00,
			imp_trib = 0.00, 
			imp_op_ex = 0.00, 
			imp_iva = 0.00,
			moneda_id = 'PES', 
			moneda_ctz = 1.000,
			obs = None,
			concepto = 1, 
			fecha_serv_desde = None, 
			fecha_serv_hasta = None,
			fecha_venc_pago = None,
			nombre_cliente = '', 
			domicilio_cliente = '',
			localidad = '', 
			provincia = '',
			pais_dst_cmp = 200, 
			id_impositivo = 'Consumidor Final',
			forma_pago  =  'Efectivo',
			obs_generales = None,
			obs_comerciales = None,
			tipoDocRec = "",
            nroDocRec = "",
			motivo_obs = "",
			tipoCodAut = "E",
			cae = "", 
			archivo_qr = '/tmp/qr.png',
			logo_afip = '/tmp/afip.png',
			resultado = "", 
			fch_venc_cae = "",
			voucher_number = None,
			custom_remito = None,
			custom_pedido = None,
		)

		self.encabezado.update(kwargs)

		self.correccion_iva = {
			3: 0.,
			4: 0.,
			5: 0.,
			6: 0,
			8: 0,
			9: 0.
		}
		
		if self.encabezado['fecha_serv_desde'] or self.encabezado["fecha_serv_hasta"]:
			self.encabezado["concepto"] = 3
		
		self.cmp_asocs = []
		self.items = []
		self.ivas = {}


	def agregar_item (
		self, 
		ds = None,
		qty = 1, 
		precio = 0, 
		tasa_iva = 21., 
		umed = 7, 
		codigo = None,
		bonif = 0.0
	):
		item = dict (
			u_mtx = None, 
			cod_mtx = None, 
			codigo = codigo, 
			ds = ds,
			qty = qty, 
			umed = umed, 
			bonif = 0.00,
			despacho = None, 
			dato_a = None,
		)
		
		subtotal = precio * qty

		iva_id = {10.5: 4, 0: 3, 21: 5, 27: 6, 5: 8 ,2.5: 9}[tasa_iva]
		item["iva_id"] = iva_id
		item["bonif"] = bonif
		
		if self.encabezado["tipo_cbte"] in (1, 2, 3, 4, 5, 34, 39, 51, 52, 53, 54, 60, 64):
			precio_neto = round(precio / (1. + tasa_iva/100.), 2)
			importe_neto = precio_neto * qty

			iva_liq = importe_neto * tasa_iva / 100.
			iva_liq_redondeado = round(iva_liq, 2)

			self.agergar_iva(iva_id, round(importe_neto,2), iva_liq_redondeado)
			self.encabezado["imp_neto"] += round(importe_neto,2)
			self.encabezado["imp_iva"] += iva_liq_redondeado

			item["precio"] = round(precio / (1. + tasa_iva/100.), 2)
			precio_sin_iva = round(precio / (1. + tasa_iva/100.), 2)

			precio_iva = round(precio_sin_iva * (tasa_iva/100.), 2)
				
			item["imp_iva"] = precio_iva
			
		elif self.encabezado["tipo_cbte"] in (11, 12, 13):
			iva_liq = subtotal * tasa_iva / 100.
			iva_liq_redondeado = round(iva_liq, 2)

			self.agergar_iva(iva_id, subtotal, iva_liq_redondeado)
			self.encabezado["imp_neto"] += subtotal
			self.encabezado["imp_iva"] += iva_liq_redondeado

			item["precio"] = round(precio, 2)
			item["imp_iva"] = None
			iva_liq_redondeado = 0
		else:
			iva_liq = subtotal * tasa_iva / 100.
			iva_liq_redondeado = round(iva_liq, 2)

			self.agergar_iva(iva_id, subtotal, iva_liq_redondeado)
			self.encabezado["imp_neto"] += round(subtotal, 2)
			self.encabezado["imp_iva"] += iva_liq_redondeado

			item["precio"] = round(precio * (1. + tasa_iva/100.), 2)	
			item["imp_iva"] = None
			subtotal += iva_liq_redondeado

			iva_liq_redondeado = 0

		item["importe"] = round(subtotal, 2)
		self.encabezado["imp_total"] += round(subtotal, 2)
		self.encabezado["imp_neto"] = round(self.encabezado["imp_neto"] ,2)

		self.encabezado["imp_total"] = round(self.encabezado["imp_total"], 2)
		self.encabezado["imp_iva"] = round(self.encabezado["imp_iva"], 2)

		self.items.append(item)


	def agergar_iva(self, iva_id, base_imp, importe):
		iva = self.ivas.setdefault(iva_id, dict(iva_id=iva_id, base_imp=0., importe=0.))
		iva["base_imp"] += round(base_imp, 2)
		iva["importe"] += round(importe, 2)

		# funciones para corregir redondeo correctamentw:
		iva["base_imp"] = round(iva["base_imp"], 2)
		iva["importe"] = round(iva["importe"], 2)
		self.correccion_iva[iva_id] += importe - round(importe, 2)

	
	def corregir_iva(self):
		for iva_id, importe in self.correccion_iva.items():
			self.encabezado["imp_iva"] += round(importe, 2)
			self.encabezado["imp_neto"] -= round(importe, 2)
			# Aseguracion de redondeo imp_iva y imp_neto
			# self.encabezado["imp_iva"] = round(self.encabezado["imp_neto"] ,2)
			# self.encabezado["imp_neto"] = round(self.encabezado["imp_neto"] ,2)
		
			if iva_id in self.ivas:
				self.ivas[iva_id]["base_imp"] -= round(importe, 2)
				self.ivas[iva_id]["importe"] += round(importe, 2)
		
		del self.correccion_iva


	def configurar_factura_c(self):
		self.encabezado["imp_iva"] = 0.00
		self.encabezado["imp_op_ex"] = 0.00
		self.encabezado["imp_tot_onc"] = 0.00
		self.encabezado["imp_total"] = self.encabezado["imp_neto"] + self.encabezado["imp_trib"]
		self.encabezado.pop("imp_iva", None)


	def autorizar(self, wsfev1):
		if self.encabezado["tipo_cbte"] in (11, 12, 13):
			self.configurar_factura_c()
		else:
			self.corregir_iva()

		if not self.encabezado["cbte_nro"]:
			ult = wsfev1.CompUltimoAutorizado(self.encabezado["tipo_cbte"], self.encabezado["punto_vta"])
			self.encabezado["cbte_nro"] = int(ult) + 1

		self.encabezado["cbt_desde"] = self.encabezado["cbte_nro"]
		self.encabezado["cbt_hasta"] = self.encabezado["cbte_nro"]

		wsfev1.CrearFactura(**self.encabezado)

		for cmp_asoc in self.cmp_asocs:
			wsfev1.AgregarCmpAsoc(**cmp_asoc)

		if self.encabezado["tipo_cbte"] in (2, 3):
			wsfev1.AgregarCmpAsoc(1, self.encabezado["punto_vta"], self.encabezado["voucher_number"])

		if self.encabezado["tipo_cbte"] in (7, 8):
			wsfev1.AgregarCmpAsoc(6, self.encabezado["punto_vta"], self.encabezado["voucher_number"])

		if self.encabezado["tipo_cbte"] in (12, 13):
			wsfev1.AgregarCmpAsoc(11, self.encabezado["punto_vta"], self.encabezado["voucher_number"])

		if self.encabezado["tipo_cbte"] not in (11, 12, 13):
			for iva in self.ivas.values():
				wsfev1.AgregarIva(**iva)

		wsfev1.CAESolicitar()

		if wsfev1.ErrMsg:
			raise RuntimeError(wsfev1.ErrMsg)

		for obs in wsfev1.Observaciones:
			warnings.warn(obs)

		if wsfev1.Resultado == "R":
			raise Exception('items: {}, {}, {}'.format(self.encabezado, self.ivas, self.items))

		assert wsfev1.Resultado == "A"
		assert wsfev1.CAE
		assert wsfev1.Vencimiento

		self.encabezado["resultado"] = wsfev1.Resultado
		self.encabezado["cae"] = wsfev1.CAE
		self.encabezado["fch_venc_cae"] = wsfev1.Vencimiento

		return True


		
	def generar_qr(self):

		datosCmp = {
            "ver": 1,
            "fecha": self.encabezado["fecha_cbte"],
            "cuit": self.encabezado["cuit"],
            "ptoVta": self.encabezado["punto_vta"],
            "tipoCmp": self.encabezado["tipo_cbte"],
            "nroCmp": self.encabezado["cbte_nro"],
            "importe": self.encabezado["imp_total"],
            "moneda": self.encabezado["moneda_id"],
            "ctz": self.encabezado["moneda_ctz"],
            "tipoDocRec": self.encabezado["tipoDocRec"],
            "nroDocRec": self.encabezado["nroDocRec"],
            "tipoCodAut": self.encabezado["tipoCodAut"],
            "codAut": self.encabezado["cae"],
        }

		url = "https://www.afip.gob.ar/fe/qr/?p=%s"

		datosCmp_json = json.dumps(datosCmp)
		datosCmp64_bytes = base64.b64encode(datosCmp_json.encode('ascii'))
		datosCmp64 = datosCmp64_bytes.decode('ascii')
		url = url % datosCmp64

		qr = qrcode.QRCode(
			version=1,
			error_correction=qrcode.constants.ERROR_CORRECT_L,
			box_size=10,
			border=4,
		)

		qr.add_data(url)
		qr.make(fit=True)

		img = qr.make_image(fill_color="black", back_color="white")
		img.save('/tmp/qr.png')

		return url

	

	def generar_pdf(self, fepdf, salida="./factura.pdf"):
		fepdf.CrearFactura(**self.encabezado)

		ok = fepdf.EstablecerParametro("localidad_cliente", self.encabezado["localidad"])
		ok = fepdf.EstablecerParametro("provincia_cliente", self.encabezado["provincia"])
		ok = fepdf.AgregarDato("custom-pedido", self.encabezado["custom_pedido"])
		ok = fepdf.AgregarDato("custom-remito", self.encabezado["custom_remito"])
		ok = fepdf.AgregarDato("AFIP_QR", self.encabezado["archivo_qr"])
		ok = fepdf.AgregarDato("AFIP", self.encabezado["logo_afip"])


		ok = fepdf.EstablecerParametro("resultado", self.encabezado["resultado"])

		for item in self.items:
			fepdf.AgregarDetalleItem(**item)

		for cmp_asoc in self.cmp_asocs:
			fepdf.AgregarCmpAsoc(**cmp_asoc)

		for iva in self.ivas.values():
			fepdf.AgregarIva(**iva)

		fepdf.CrearPlantilla(papel="A4", orientacion="portrait")
		fepdf.ProcesarPlantilla(num_copias=3, lineas_max=24, qty_pos='izq')
		fepdf.GenerarPDF(archivo=salida)

		return salida
		