# import para denotar que una función tiene diferentes tipos de retornos
from typing import List, Union, Tuple

# importando clases principales
from elementos.error import Errores
from elementos.lexema import Lexema
from elementos.token import Token
from elementos.etiqueta import Etiqueta

# importando diccionario de palabras clave y de traduccion
from elementos.diccionario import *

class Analizador():
    
    def __init__(self):
        # variables globales
        self.nLinea = 0
        self.nColumna = 0
        self.listadoLexemas = []
        self.listadoLexemas_sinRepetir = []
        self.listadoErrores = []
        self.listadoTokens = []
        self.etiquetas = []
        self.html = ""

    # analizador lexico
    def analizar_entrada(self,cadena):
        lexema = ""
        puntero = 0
        
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
                lexema, cadena = self.armar_lexema(cadena[puntero:],3)
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
        
    def descomponerCadenas(self, cadena):
        valor = ""
        lexema = ""
        puntero = 0
        columna = 0
        
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
                if cadena == '"fila"' and len(cadena) == 6:
                    cadenaInteres = cadena[puntero:puntero+4]
                    valor = cadenaInteres
                    cadena = cadena[puntero+4:]
                    puntero = 0
                    columna += 1
                elif cadena == '"columna"' and len(cadena) == 9:
                    cadenaInteres = cadena[puntero:puntero+7]
                    valor = cadenaInteres
                    cadena = cadena[puntero+7:]
                    puntero = 0
                    columna += 1
                else:
                    cadena = cadena[1:]
                    puntero = 0
                    columna += 1
            elif caracter.isalpha():
                lexema, cadena = self.armar_lexema(cadena[puntero-1:],2)
                if lexema and cadena:
                    valor = f'"{lexema}"'
                    columna += len(lexema) + 1
                    puntero = 0
            elif caracter.isdigit():
                lexema, cadena = self.armar_lexema(cadena[puntero-1:],2)
                if lexema and cadena:
                    if len(lexema) == 6:
                        valor = lexema
                    else:
                        valor = int(lexema)
                    columna += len(lexema) + 1
                    puntero = 0
            else:
                cadena = cadena[1:]
                puntero = 0
                columna += 1
        return valor
                    
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
        elif analisis == 3:
            for caracter in cadena:
                puntero += caracter
                if caracter == '\"':
                    return lexema, cadena[len(puntero):]
                else:
                    lexema += caracter
        else:
            for caracter in cadena:
                puntero += caracter
                if caracter == '\"':
                    return lexema, cadena[len(puntero)-1:]
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
        c1, c2, c3 = 0, 0, 0
        for lexema in self.listadoLexemas:
            if lexema.lexema == "Encabezado":
                c1 += 1
            elif lexema.lexema == "Cuerpo":
                c2 += 1
            elif lexema.lexema == "Inicio":
                c3 += 1
            else:
                continue
        if c3 == 0 or c3 > 1:
            return ["Inicio", c3]
        elif c1 == 0 or c1 > 1:
            return ["Encabezado", c1]
        elif c2 == 0 or c2 > 1:
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

    def analizarErrores(self) -> Union[List, str]:
        erroresLexicos = len(self.listadoErrores)
        if erroresLexicos > 0:
            self.exportarErrores()
            return "errores generados en archivo ListaErrores.html"
        
        # verificando etiqueta encabezado y cuerpo
        atributo, problema = self.getErrores2()
        lista = [atributo, problema]
        if atributo != None:
            return lista
        
        la, lc, ca, cc = 0, 0, 0, 0
        listadoSignos = ""
        for signo in self.listadoLexemas:
            if signo.lexema == "{":
                la += 1
                listadoSignos += f'{signo.lexema} , {signo.getFila()} , {signo.getColumna()}'+'\n'
            elif signo.lexema == "[":
                ca += 1
                listadoSignos += f'{signo.lexema} , {signo.getFila()} , {signo.getColumna()}'+'\n'
            elif signo.lexema == "}":
                lc += 1
                listadoSignos += f'{signo.lexema} , {signo.getFila()} , {signo.getColumna()}'+'\n'
            elif signo.lexema == "]":
                cc += 1
                listadoSignos += f'{signo.lexema} , {signo.getFila()} , {signo.getColumna()}'+'\n'
            else:
                continue
        llaves = la == lc
        corchetes = ca == cc
        if llaves == True and corchetes == True:
            return None
        else:
            error = f' el simbolo {"{"+" "}aparece {la} veces y el simbolo {"}"+" "} aparece {lc} veces'+'\n'
            error += f' el simbolo "[" aparece {ca} veces y el simbolo "]" aparece {cc} veces'+'\n'*2
            error += "Listado de ocurrencias de llaves y corchetes: \n"
            error += listadoSignos
            return ["error en la cantidad de llaves y corchetes", error]

    # tokens
    def getLexema(self, lexema):
        for i in self.listadoLexemas_sinRepetir:
            lex = i.lexema[1:len(i.lexema)-1]
            if lex == lexema:
                return i
        return None
    
    def crearTokens(self, cadenas=True, listado=[]):
        # primero analizamos las palabras reservadas y separamos de strings y numeros
        global reservadas
        contadorCadenas = 1
        if cadenas:
            for lexema in self.listadoLexemas_sinRepetir:
                if len(lexema.lexema) == 1:
                    if lexema.lexema == reservadas.get(lexema.lexema,None):
                        self.listadoTokens.append(
                            Token("Simbolo", lexema.lexema, lexema.getFila(), lexema.getColumna())
                        )
                    continue
                clave = ""
                if lexema.lexema == "texto":
                    clave = lexema.lexema.lower()
                else:
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
        else:
            contadorFilas = 0
            contadorColumnas = 0
            for lexema in listado:
                clave = ""
                if lexema == "fila":
                    contadorFilas += 1
                    clave = lexema.upper()
                elif lexema == "columna":
                    contadorColumnas += 1
                    clave = lexema.upper()
                else:
                    clave = lexema
                if lexema == reservadas.get(clave,None):
                    if contadorFilas == 1 and len(lexema) == 4:
                        objeto = self.getLexema(lexema)
                        tokenAntiguo = None
                        for elem in self.listadoTokens:
                            if elem.lexema == objeto.lexema:
                                tokenAntiguo = elem
                        tokenAntiguo.id = "Palabra reservada"
                        tokenAntiguo.lexema = lexema
                        tokenAntiguo.fila = objeto.getFila() + 1
                    elif contadorColumnas == 1 and len(lexema) == 7:
                        objeto = self.getLexema(lexema)
                        tokenAntiguo = None
                        for elem in self.listadoTokens:
                            if elem.lexema == objeto.lexema:
                                tokenAntiguo = elem
                        tokenAntiguo.id = "Palabra reservada"
                        tokenAntiguo.lexema = lexema
                        tokenAntiguo.fila = objeto.getFila() + 1

    def getTokens(self) -> str:
        self.listadoErrores
        formato = '<table align="center" border="black" height="50%" width="50%">\n'
        formato += '<tr bgcolor="black">\n'
        formato += '<th><font color="white">Token</font</th>\n'
        formato += '<th><font color="white">Lexema</font</th>\n'
        formato += '<th><font color="white">Columna</font</th>\n'
        formato += '<th><font color="white">Fila</font</th>\n'
        formato += '</tr>\n' 
        for i in range(len(self.listadoTokens)):
            formato += '<tr>\n'
            token = self.listadoTokens[i]
            formato += token.execute() + '</tr>\n'
        formato += '</table>\n'
        return formato
    
    def escribirTokens(self):
        retorno = ""
        for i in self.listadoTokens:
            retorno += i.execute() + "\n"
        return retorno
    
    def exportarTokens(self) -> None:
        nombre = "ListaTokens"+".html"
        with open(nombre, 'w') as archivo:
            archivo.write('<!DOCTYPE html>\n')
            archivo.write('<html>\n')
            archivo.write('<head>\n')
            archivo.write('<title>Errores</title>\n')
            archivo.write('</head>\n')
            archivo.write('<body font-size="16">\n')
            archivo.write('<font size="6">\n')
            archivo.write(self.getTokens())
            archivo.write('</font>\n')
            archivo.write('</body>\n')
            archivo.write('</html>\n')

    def listadoCadenas(self) -> list:
        cadenas = []
        for i in self.listadoLexemas:
            first_char = i.lexema[0]
            last_char = i.lexema[-1]
            condicional = first_char == '\"' and last_char == '\"'
            if condicional:
                cadenas.append(i)
            else:
                continue
        return cadenas
    
    # traduccion
    def armandoBloque(self, listado, tipo="c") -> tuple:
        bloque = []
        subBloque = []
        if tipo == "c":
            for elemento in listado:
                el = elemento.lexema
                if el == '[':
                    continue
                elif el == ']':
                    return bloque
                else:
                    bloque.append(el)
        else:
            for elemento in listado:
                el = elemento.lexema
                if el == '{':
                    indice = listado.index(elemento)
                    for elem in listado[indice+1:]:
                        if elem.lexema == '}':
                            indice = listado.index(elemento)+1
                            siguiente = listado[indice].lexema
                            comparacion = el+siguiente
                            if comparacion == "};":
                                bloque.append(subBloque)
                                break
                        else:
                            subBloque.append(elem.lexema)
                elif el == '}':
                    indice = listado.index(elemento)+1
                    siguiente = listado[indice].lexema
                    if siguiente == ",":
                        return bloque
                    elif siguiente== "}":
                        return bloque
                else:
                    bloque.append(el)
                    
    def creandoBloques(self, listadoAux) -> list:
        listadoBloques = []
        for l in enumerate(listadoAux):
            index, elem = l
            lex = elem.lexema
            clave = ""
            if lex.isalpha():
                clave = lex.upper()
            else:
                clave = lex
            if lex == reservadas.get(clave,None):
                concat = ""
                if len(listadoAux) > index+2:
                    concat = lex + listadoAux[index+1].lexema + listadoAux[index+2].lexema
                comp = lex + ":" + "["
                comp2 = lex + ":" + "{"
                if concat == comp:
                    inicio = index + 2
                    lis = listadoAux[inicio:]
                    bloque = self.armandoBloque(lis)
                    listadoBloques.append(bloque)
                elif concat == comp2:
                    inicio = index + 3
                    lis = listadoAux[inicio:]
                    bloque = self.armandoBloque(lis,"p")
                    listadoBloques.append(bloque)
                else:
                    continue
        return listadoBloques
    
    def crearEtiquetas(self,listado):
        diccionario = {}
        nombreEtiqueta = ""
        nombreAtributo = ""
        etiqueta = ""
        css = ""
        posiciones = 0
        numerador = 0
        valores = []
        while listado:
            actual = listado[posiciones]
            posiciones += 1
            siguiente= ""
            if actual.isalpha():
                if actual[0].isupper():
                    if actual == reservadas.get(actual.upper(),None):
                        nombreEtiqueta = actual
            if len(listado) > posiciones:
                siguiente = listado[posiciones]
                  
            if actual+siguiente != "}," and actual+siguiente != "}]":
                if actual == "elemento" and siguiente == ":":
                    indice1 = listado.index(siguiente)
                    listadoAux = listado[indice1+1:]
                    posAux = 0
                    for j in listadoAux:
                        posiciones += 1
                        posAux += 1
                        j_siguiente = listadoAux[posAux]
                        if j+j_siguiente != "};":
                            if j != ":" and j != "{":
                                valores.append(j)
                            else:
                                continue
                        else:
                            diccionarioAux = {}
                            for k in enumerate(valores):
                                index, elemento = k
                                if elemento != ",":
                                    if elemento == "fila":
                                        diccionarioAux[elemento] = valores[index+1]
                                    elif elemento == "columna":
                                        diccionarioAux[elemento] = valores[index+1]
                                    else:
                                        diccionarioAux["contenido"] = elemento
                                else:
                                    continue
                            diccionario[actual+str(numerador)] = diccionarioAux
                            listado = listado[posiciones+2:]
                            posiciones = 0
                            numerador += 1
                            break
                elif siguiente == ":" or siguiente == "=":
                    if actual == "texto":
                        nombreAtributo = actual
                        listado = listado[posiciones+1:]
                        posiciones = 0
                    elif reservadas.get(actual.upper(),None)[0].isupper():
                        nombreEtiqueta = actual
                        listado = listado[posiciones+2:]
                        posiciones = 0
                    elif reservadas.get(actual.upper(),None)[0].islower():
                        
                        nombreAtributo = actual
                        listado = listado[posiciones+1:]
                        posiciones = 0
                elif actual == ";" or actual == ",":
                    listado = listado[posiciones+1:]
                    posiciones = 0
                else:
                    diccionario[nombreAtributo] = actual
                    listado = listado[posiciones+1:]
                    posiciones = 0
                    continue
            else:
                e = Etiqueta(nombreEtiqueta)
                e.atributos = diccionario
                name = ""
                if nombreEtiqueta != "Salto":
                    et = e.crearEtiquetahtml()
                else:
                    cantidad = int(e.atributos["cantidad"])
                    nombreEtiqueta = "<br>"*cantidad
                    name = "Salto"
                
                if name == "Salto":
                    self.etiquetas.append(nombreEtiqueta)
                    name = ""
                else:
                    self.etiquetas.append(et)
                    
                listado = listado[posiciones+1:]
                posiciones = 0
                numerador = 0
                diccionario = {}
                valores = []
    
    def exportandoEtiquetas(self, head):
        # for i in self.etiquetas:
        #     print(i)
        self.html += f'<!DOCTYPE html>\n'
        self.html += f'<html>\n'
        self.html += f'<head>\n'
        self.html += f'<title>{head}</title>\n'
        self.html += f'<link rel="stylesheet" type="text/css" href="estilos.css">\n'
        self.html += f'</head>\n'
        self.html += f'<body>\n'
        
        for i in self.etiquetas:
            if i[0] != "<":
                nombre = "estilos"+".css"
                with open(nombre, 'w') as archivo:
                    archivo.write(f'body'+ " {" + "\n\t" + i + "\n" + "}" + "\n")
                    archivo.write(f'.codigo'+ " {" + "\n\t" + "text-align: center;" + "\n\t" + "font-family: JetBrains Mono;" + "\n" +"}")
            else:
                self.html += i + "\n"
        
        self.html += f'</body>\n'
        self.html += f'</html>\n'
        nombre = "pagina"+".html"
        open(nombre, 'w').write(self.html)
    
    # funcion de ejecucion
    def progreso(self, cadena) -> Union[List, str, Tuple[str, List]]:
        
        # literalmente el analizador lexico
        
        self.analizar_entrada(cadena)
        
        # manejo de errores
        
        detenerse = self.analizarErrores()
        if type(detenerse) == list:
            # retorna una Lista
            return detenerse
        elif type(detenerse) == str:
            # retorna un string
            return detenerse
        
        # creacion de tokens
        
        self.crearTokens()
        cadenas = self.listadoCadenas()
        listadoDescomposiciones = []
        for c in cadenas:
            valor = self.descomponerCadenas(c.lexema)
            listadoDescomposiciones.append(valor)
        self.crearTokens(False, listadoDescomposiciones)
        self.exportarTokens()
        
        # comienzo de traducción de datos
        
        listadoAux = self.listadoLexemas[3:len(self.listadoLexemas)-1]
        for l in listadoAux:
            if l.lexema[0] == '\"':
                longitud = len(l.lexema) - 1
                cadenaTexto = l.lexema[1:longitud]
                l.lexema = cadenaTexto
        
        # obteniendo bloques de datos
        listadoBloques = self.creandoBloques(listadoAux)
        encabezado = listadoBloques[0]
        cuerpo = listadoBloques[1]
        cuerpo.append("]")
        self.crearEtiquetas(cuerpo)
        
        # traduciendo y creando HTML
        self.exportandoEtiquetas(encabezado[2])
        
        # retornando mensaje de exito
        return "Archivo generado con exito", self.html
    