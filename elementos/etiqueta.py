
class Etiqueta():
	def __init__(self, atributo):
		self.atributo = atributo    # el nombre por el que voy a identificar mi diccionario
		self.diccionario = {}       # el diccionario que voy a llenar con los valores que me lleguen

	def llenarDiccionario(self, clave, valor):
		self.diccionario[clave] = valor

	def getDiccionario(self):
		for clave, valor in self.diccinario:
			print(f" el subatributo {clave} tiene un valor de {valor}")
