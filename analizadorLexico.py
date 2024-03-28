# importando clases principales
from elementos.error import Errores
from elementos.lexema import Lexema
from elementos.token import Token

# importando diccionario de palabras clave y de traduccion
from elementos.diccionario import reservadas

class Analizador():
    
    def __init__(self):
        # variables globales
        self.nLinea = 0
        self.nColumna = 0
        self.listadoLexemas = []
        self.listadoLexemas_sinRepetir = []
        self.listadoErrores = []
        self.listadoTokens = []

    # analizador lexico
    def analizar_entrada(self,cadena):
        lexema = ""
        puntero = 0
        # recorriendo la cadena y analizando cada caracter
        while cadena:
            caracter = cadena[puntero]
            puntero += 1
            
            if caracter == '\"':
                l = Lexema(caracter, self.nLinea, self.nColumna)
                for i in self.listadoLexemas_sinRepetir:
                    if l.lexema == i.lexema:
                        break
                    if i == self.listadoLexemas_sinRepetir[-1]:
                        if l.lexema != i.lexema:
                            self.listadoLexemas_sinRepetir.append(l)
                lexema, cadena = self.armar_lexema(cadena[puntero:])
                if lexema and cadena:
                    lex = Lexema(f'"{lexema}"', self.nLinea, self.nColumna)
                    self.listadoLexemas.append(lex)
                    if self.existe(lex) == False:
                        self.listadoLexemas_sinRepetir.append(lex)
                    self.nColumna += len(lexema) + 1
                    puntero = 0
            elif caracter.isupper() or caracter.islower():
                lexema, cadena = self.armar_lexema(cadena[puntero-1:])
                if lexema and cadena:
                    lex = Lexema(lexema, self.nLinea, self.nColumna)
                    self.listadoLexemas.append(lex)
                    if self.existe(lex) == False:
                        self.listadoLexemas_sinRepetir.append(lex)
                    self.nColumna += len(lexema) + 1
                    puntero = 0
            elif caracter == '{' or caracter == '}' or caracter == '[' or caracter == ']' or caracter == ';' or caracter == ',' or caracter == ':' or caracter == '=':
                lex = Lexema(caracter, self.nLinea, self.nColumna)
                self.listadoLexemas.append(lex)
                if self.existe(lex) == False:
                    self.listadoLexemas_sinRepetir.append(lex)
                cadena = cadena[1:]
                puntero = 0
                self.nColumna += 1
            elif caracter =="\t":
                self.nColumna += 4
                cadena = cadena[4:] 
                puntero = 0 
            elif caracter == "\n": 
                cadena = cadena[1:] 
                puntero = 0 
                self.nLinea += 1
                self.nColumna = 1
            elif caracter == ' ' or caracter == '\r':
                self.nColumna += 1
                cadena = cadena[1:] 
                puntero = 0 
            else:
                error = Errores(caracter, self.nLinea, self.nColumna)
                self.listadoErrores.append(error)
                self.nColumna += 1
                cadena = cadena[1:] 
                puntero = 0
        
        # si hay errores se detiene el analisis
        detenerse = self.analizarErrores()
        if type(detenerse) == list:
            print(detenerse[0], detenerse[1])
            return detenerse # retorna lista [tiqueta, problema]
        elif type(detenerse) == str:
            print(detenerse)
            return detenerse # retorna mensaje de error y exportacion de errores
        
        # si no hay errores se continua con el analisis
        self.crearTokens()
        # print("-"*75)
        # for token in self.listadoLexemas:
        #     print("lexema: "+token.lexema)
        # print("fin")
        
    def descomponerCadenas(self, cadena) -> list:
        listadoComponentes = []
        lexema = ""
        puntero = 0
        columna = 0
        fila = 0
        
        while cadena:
            caracter = cadena[puntero]
            puntero += 1
            
            if caracter == '\"':
                '''
                    " f i l a "
                    0 1 2 3 4 5
                    [puntero:puntero+5] = "fila"
                    [puntero+1:puntero+4] = fila
                    
                    " c o l u m n a "
                    0 1 2 3 4 5 6 7 8
                    [puntero:puntero+6] = "columna"
                    [puntero+1:puntero+7] = columna
                '''
                cadena_fila = cadena[puntero:puntero+5]
                cadena_colum = cadena[puntero:puntero+8]
                if cadena_fila == '"fila"':
                    cadenaInteres = cadena_fila[puntero+1:puntero+4]
                    print(cadenaInteres)
                    listadoComponentes.append(cadenaInteres)
                    cadena = cadena[puntero:puntero+5]
                    columna += len(cadenaInteres) + 1
                    puntero = 0
                elif cadena_colum == '"columna"':
                    cadenaInteres = cadena_colum[puntero+1:puntero+7]
                    print(cadenaInteres)
                    listadoComponentes.append(cadenaInteres)
                    cadena = cadena[puntero:puntero+8]
                    columna += len(cadenaInteres) + 1
                    puntero = 0
                else:
                    cadena = cadena[puntero:]
                    puntero = 0
                    columna += 1
            elif caracter.isdigit():
                lexema, cadena = self.armar_lexema(cadena[puntero:],2)
                if lexema and cadena:
                    lex = Lexema(lexema, fila, columna)
                    listadoComponentes.append(lex)
                    columna += len(lexema) + 1
                    puntero = 0
            elif caracter == "\n":
                cadena = cadena[1:] 
                puntero = 0 
                fila += 1
                columna += 1
            elif caracter == "\t":
                cadena = cadena[4:] 
                puntero = 0
                columna += 4
            else:
                lexema, cadena = self.armar_lexema(cadena[puntero:],2)
                if lexema and cadena:
                    lex = lexema(lexema, fila, columna)
                    listadoComponentes.append(lex)
                    columna += len(lexema) + 1
                    puntero = 0
                    
            
    
    def armar_lexema(self, cadena, analisis=1) -> tuple:
        lexema = ''
        puntero = ''
        if analisis == 1:
            for caracter in cadena:
                puntero += caracter
                if caracter == '\"':
                    return lexema, cadena[len(puntero):]
                elif caracter == ':' or caracter == '=':
                    return lexema, cadena[len(puntero)-1:]
                else:
                    lexema += caracter
        else:
            for caracter in cadena:
                puntero += caracter
                if caracter == '\"':
                    return lexema, cadena[len(puntero):]
                else:
                    lexema += caracter
        return None, None 

    # funciones de apoyo
    def existe(self, lexema) -> bool:
        listado = self.listadoLexemas_sinRepetir
        for i in listado:
            if i.lexema == lexema.lexema:
                return True
        return False

    def imprimir(self, tipo="repetir") -> None:
        if tipo == "sin repetir":
            for token in self.listadoLexemas_sinRepetir:
                print(token.lexema)
        else:
            for token in self.listadoLexemas:
                print(token.lexema)
                
    # errores
    def getErrores(self) -> str:
        self.listadoErrores
        formato = '<table align="center" border="black" height="50%" width="50%">\n'
        formato += '<tr bgcolor="black">\n'
        formato += '<th><font color="white">No.</font</th>\n'
        formato += '<th><font color="white">Lexema</font</th>\n'
        formato += '<th><font color="white">Fila</font</th>\n'
        formato += '<th><font color="white">Columna</font</th>\n'
        formato += '</tr>\n' 
        for i in range(len(self.listadoErrores)):
            formato += '<tr>\n'
            error = self.listadoErrores[i]
            formato += error.execute(i+1) + '</tr>\n'
        formato += '</table>\n'
        return formato

    def getErrores2(self) -> list:
        c1, c2 = 0, 0
        for lexema in self.listadoLexemas:
            if lexema.lexema == "Encabezado":
                c1 += 1
            elif lexema.lexema == "Cuerpo":
                c2 += 1
            else:
                continue
        if c1 == 0 or c1 > 1:
            return ["Encabezado", c1]
        if c2 == 0 or c2 > 1:
            return ["Cuerpo", c2]
        return None, None

    def exportarErrores(self):
        nombre = "ListaErrores"+".html"
        with open(nombre, 'w') as archivo:
            archivo.write('<!DOCTYPE html>\n')
            archivo.write('<html>\n')
            archivo.write('<head>\n')
            archivo.write('<title>Errores</title>\n')
            archivo.write('</head>\n')
            archivo.write('<body font-size="16">\n')
            archivo.write('<font size="6">\n')
            archivo.write(self.getErrores())
            archivo.write('</font>\n')
            archivo.write('</body>\n')
            archivo.write('</html>\n')

    def analizarErrores(self):
        erroresLexicos = len(self.listadoErrores)
        if erroresLexicos > 0:
            self.exportarErrores()
            return "errores generados en archivo ListaErrores.html"
        atributo, problema = self.getErrores2()
        lista = [atributo, problema]
        if atributo != None:
            return lista
        return None

    # exportacion de tokens
    def crearTokens(self):
        # primero analizamos las palabras reservadas y separamos de strings y numeros
        global reservadas
        contadorCadenas = 1
        listadoCadenas = []
        for lexema in self.listadoLexemas_sinRepetir:
            if len(lexema.lexema) == 1:
                if lexema.lexema == reservadas.get(lexema.lexema,None):
                    self.listadoTokens.append(
                        Token("Simbolo", lexema.lexema, lexema.getFila(), lexema.getColumna())
                    )
                    print(lexema.lexema)
                continue
            clave = lexema.lexema.upper()
            valor = reservadas.get(clave, None)
            if lexema.lexema == valor and valor != None:
                self.listadoTokens.append(
                    Token("Palabra Reservada", lexema.lexema, lexema.getFila(), lexema.getColumna())
                )
            elif lexema.lexema.isdigit():
                self.listadoTokens.append(
                    Token("Numero", lexema.lexema, lexema.getFila(), lexema.getColumna())
                )
            else:
                self.listadoTokens.append(
                    Token(f"Cadena no.{contadorCadenas}", lexema.lexema, lexema.getFila(), lexema.getColumna())
                )
                contadorCadenas += 1
                listadoCadenas.append(lexema)
        return listadoCadenas
        
