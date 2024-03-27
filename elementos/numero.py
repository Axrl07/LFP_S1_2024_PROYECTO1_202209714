from elementos.abstracto import Expresion

class Numero(Expresion):
    def __init__(self, valor, fila, columna):
        self.valor = valor
        super().__init__(fila, columna)
        
    def execute(self, enviroment):
        return self.valor
    
    def getFila(self):
        return super().getFila()
    
    def getColuman(self):
        return super().getColumna()