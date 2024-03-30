from elementos.abstracto import Expression

class Token(Expression):
    def __init__(self, id, lexema, fila, columna):
        self.id = id
        self.lexema = lexema
        super().__init__(fila, columna)
    
    def execute(self, enviroment=None):
        id = f'<td align="center">{self.id}</td>\n'
        lexema = f'<td align="center">{self.lexema}</td>\n'
        fila = f'<td align="center">{self.fila}</td>\n'
        columna = f'<td align="center">{self.columna}</td>\n'
        return f'{id + lexema + columna + fila}'
    
    def getFila(self):
        return super().getFila()
    
    def getColumna(self):
        return super().getColumna()