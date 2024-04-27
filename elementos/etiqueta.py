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
				elif i == "color":
					if len(self.atributos[i]) == 7:
						etiqueta += '><font color'+ '="' + self.atributos[i] + '"> '
					else:
						etiqueta += '><font color'+ '="' + traduccion.get(self.atributos[i].upper(),None) + '"> '
				else:
					valor = traduccion.get(self.atributos[i].upper(),None)
					atr = traduccion.get(i.upper(),None)
					if valor != None:
						etiqueta += atr + '="' + valor + '" '
					else:
						etiqueta += atr + '="' + self.atributos[i] + '" '
			etiqueta += contenido + "</font>" + "</" + etiqueta[1:3] + ">"
		elif self.nombre == "Negrita":
			etiqueta = "<b>"
			contenido = self.atributos["texto"]
			etiqueta += contenido + "</b>"
		elif self.nombre == "Cursiva":
			etiqueta = "<i>"
			contenido = self.atributos["texto"]
			etiqueta += contenido + "</i>"
		elif self.nombre == "Subrayado":
			etiqueta = "<u>"
			contenido = self.atributos["texto"]
			etiqueta += contenido + "</u>"
		elif self.nombre == "Tachado":
			etiqueta = "<del>"
			contenido = self.atributos["texto"]
			etiqueta += contenido + "</del>"
		elif self.nombre == "Codigo":
			alineacion = ""
			etiqueta = f'<code class="codigo" '
			for i in self.atributos:
				if i == "texto":
					contenido = self.atributos[i]
				elif i == "posicion":
					alineacion = traduccion.get(self.atributos[i].upper(),None)
				else:
					valor = traduccion.get(self.atributos[i].upper(),None)
					atr = traduccion.get(i.upper(),None)
					if valor != None:
						etiqueta += atr + '="' + valor + '" '
					else:
						etiqueta += atr + '="' + traduccion.get(self.atributos[i],None) + '" '
			etiqueta += f'><font align="{alineacion}">' + contenido + "</font></code>"
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
					if len(self.atributos[atributo]) == 7:
						etiqueta += 'color'+ '="' + self.atributos[atributo] + '" '
					else:
						etiqueta += 'color'+ '="' + traduccion.get(self.atributos[atributo].upper(),None) + '" '
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
				# Leer el número de filas y columnas
				num_filas = int(self.atributos['filas'])
				num_columnas = int(self.atributos['columnas'])

				# Iniciar el código HTML de la tabla
				tabla_html = '<table align="center" border="black" height="300" width="85%">\n'

				# Recorrer las filas y columnas para construir la tabla
				for i in range(num_filas):
					tabla_html += '<tr>\n'
					for j in range(num_columnas):
						encontrado = False
						for k in range(num_filas * num_columnas):
							clave_elemento = f'elemento{k}'
							celda = self.atributos.get(clave_elemento, {})
							fila_celda = int(celda.get('fila', '0')) - 1
							columna_celda = int(celda.get('columna', '0')) - 1
							if fila_celda == i and columna_celda == j:
								contenido = celda.get('contenido', '')
								tabla_html += f'<td>{contenido}</td>\n'
								encontrado = True
								break
						if not encontrado:
							tabla_html += '<td></td>\n'
					tabla_html += '</tr>\n'

				tabla_html += '</table>'
				etiqueta = tabla_html
		return etiqueta