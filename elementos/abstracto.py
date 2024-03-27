from abc import ABC, abstractmethod

class Expression(ABC):
    
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
    
    @abstractmethod 
    def execute(self, enviroment):
        pass 
 
    @abstractmethod 
    def getFila(self) -> int:
        return self.fila 
 
    @abstractmethod 
    def getColumna(self) -> int:
        return self.columna