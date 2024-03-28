from elementos.abstracto import Expression

class Token(Expression):
    def __init__(self, id, lexema, nLinea, nColumna):
        self.id = id
        self.lexema = lexema
        super().__init__(nLinea, nColumna)
    
    def execute(self, enviroment):
        return self.token
    
    def getFila(self):
        return super().getFila()
    
    def getColumna(self):
        return super().getColumna()