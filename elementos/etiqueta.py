from elementos.diccionario import traduccion
class Etiqueta():
	def __init__(self, nombre):
		self.nombre = nombre    # el nombre por el que voy a identificar mi diccionario
		self.atributos = {}       # el diccionario que voy a llenar con los valores que me lleguen

	def crearEtiquetahtml(self) -> str:
		etiqueta = ""
		contenido = ""
		if self.nombre == "Titulo":
			etiqueta = "<ht "
			for i in self.atributos:
				if i == "tamaÃ±o":
					etiquetafinal = etiqueta[3:]
					etiqueta = f'<h{self.atributos.get(i,None)[1]}' + etiquetafinal
				elif i == "texto":
					contenido = self.atributos[i]
				else:
					valor = traduccion.get(self.atributos[i].upper(),None)
					atr = traduccion.get(i.upper(),None)
					if valor != None:
						etiqueta += atr + '="' + valor + '" '
					else:
						etiqueta += atr + '="' + self.atributos[i] + '" '
			etiqueta += ">" + contenido + "</" + etiqueta[1:3] + ">"
		elif self.nombre == "Negrita":
			etiqueta = "<b>"
			contenido = self.atributos["texto"]
			etiqueta += contenido + "</b>"
		elif self.nombre == "Cursiva":
			etiqueta = "<u>"
			contenido = self.atributos["texto"]
			etiqueta += contenido + "</u>"
		elif self.nombre == "Subrayado":
			etiqueta = "<u>"
			contenido = self.atributos["texto"]
			etiqueta += contenido + "</u>"
		elif self.nombre == "Tachado":
			etiqueta = "<del>"
			contenido = self.atributos["texto"]
			etiqueta += contenido + "</del>"
		elif self.nombre == "Codigo":
			etiqueta = f'<code class="codigo" '
			for i in self.atributos:
				if i == "texto":
					contenido = self.atributos[i]
				else:
					valor = traduccion.get(self.atributos[i].upper(),None)
					atr = traduccion.get(i.upper(),None)
					if valor != None:
						etiqueta += atr + '="' + valor + '" '
					else:
						etiqueta += atr + '="' + self.atributos[i] + '" '
			etiqueta += ">" + '<font color="white" face="Hurmit Nerd font light">' + contenido + "</font>" +"</code>"
		elif self.nombre == "Texto":
			etiqueta = "<" + traduccion.get(self.nombre.upper(),None) + "> "
			contador = 0
			for atributo in self.atributos:
				if contador == 0:	
					etiqueta += "<font" + ' '
					contador += 1
     
				if atributo == "texto":
					contenido = self.atributos[atributo]
				elif atributo == "fuente":
					etiqueta += 'face'+ '="' + self.atributos[atributo] + '" '
				elif atributo == "color":
					etiqueta += 'color'+ '="' + self.atributos[atributo] + '" '
				else:
					lista = list(self.atributos.keys())
					value = traduccion.get(self.atributos[atributo].upper(),None)
					if value != None:
						etiqueta +=  atributo + '="' + value + '" '
					else:
						atr = traduccion.get(atributo.upper(),None)
						etiqueta += atr + '="' + self.atributos[atributo] + '" '
			etiqueta += ">" + contenido + "</font></p>"
		else:
			etiqueta = traduccion.get(self.nombre.upper(),None)
			if etiqueta != "table":
					etiqueta = "<" + etiqueta + " "
					if self.nombre == "Fondo":
						return f'background-color: {self.atributos["color"]};'
					else:
						for atributo in self.atributos:
							if atributo == "texto":
								contenido = self.atributos[atributo]
							else:
								lista = list(self.atributos.keys())
								value = traduccion.get(self.atributos[atributo].upper(),None)
								if value != None:
									etiqueta +=  atributo + '="' + value + '" '
								else:
									atr = traduccion.get(atributo.upper(),None)
									etiqueta += atr + '="' + self.atributos[atributo] + '" '
								if atributo == lista[-1]:
									etiqueta += ">" + contenido + "</" + traduccion.get(self.nombre.upper(),None) + ">"
									break
			else:
				# codigo para crear la tabla
				print("tabla")
		return etiqueta