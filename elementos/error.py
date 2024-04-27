from elementos.abstracto import Expression

class Errores(Expression):
    
    def __init__(self, caracter, fila, columna):
        self.caracter = caracter
        super().__init__(fila, columna)
        
    def execute(self, num):
        numero = f'<td align="center">{num}</td>\n'
        lexema = f'<td align="center">{self.caracter}</td>\n'
        fila = f'<td align="center">{self.fila}</td>\n'
        columna = f'<td align="center">{self.columna}</td>\n'
        return f'{numero + lexema + fila + columna}'
    
    def getFila(self):
        return super().getFila()
    
    def getColumna(self):
        return super().getColumna()