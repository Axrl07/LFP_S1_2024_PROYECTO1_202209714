from elementos.error import *
from elementos.lexema import Lexema

reserved = {
    # elementos externos
    'INICIO'               :   'Inicio',
    'ENCABEZADO'           :   'Encabezado',
    'TITULOPAGINA'         :   'TituloPagina',
    'CUERPO'               :   'Cuerpo',
    'TITULO'               :   'Titulo',
    'FONDO'                :   'Fondo',
    'PARRAFO'              :   'Parrafo',
    'TEXTO'                :   'Texto',
    'CODIGO'               :   'Codigo',
    'SALTO'                :   'Salto',
    'TABLA'                :   'Tabla',
    'NEGRITA'              :   'Negrita',
    'CURSIVA'              :   'Cursiva',
    'TACHADO'              :   'Tachado',
    'SUBRAYADO'            :   'Subrayado',
    # Elementos internos
    'TEXTOINTERNO'         :   'texto',
    'POSICION'             :   'posicion',
    'TAMANIO'              :   'tamaño',
    'COLOR'                :   'color',
    'FUENTE'               :   'fuente',
    'FILAS'                :   'filas',
    'COLUMNAS'             :   'columnas',
    'ELEMENTO'             :   'elemento',
    # signos
    'COMILLA'               :   '"',
    'PUNTOYCOMA'            :   ';',
    'DOSPUNTOS'             :   ':',
    'LLAVEINICIO'           :   '{',
    'LLAVEFINAL'            :   '}',
    'CORCHETEINICIO'        :   '[',
    'CORCHETEFINAL'         :   ']',
    'COMA'                  :   ',',   
}

lexemas = list(reserved.values())

nLinea = 0
nColumna = 0
instrucciones = []
listadoLexemas = []
conjuntoLexemas = []
listadoErrores = []

def instruccion(cadena):
    global nLinea
    global nColumna
    global listadoLexemas
    global listadoErrores
    
    lexema = ""
    puntero = 0
    while cadena:
        caracter = cadena[puntero]
        puntero += 1
        
        if caracter == '\"':
            lexema, cadena = armar_lexema(cadena[puntero:])
            if lexema and cadena:
                nColumna += 1
                listadoLexemas.append(Lexema(f'"{lexema}"', nLinea, nColumna))
                nColumna += len(lexema) + 1
                puntero = 0
        elif caracter.isupper():
            lexema, cadena = armar_lexema(cadena[puntero-1:])
            if lexema and cadena:
                nColumna += 1
                listadoLexemas.append(Lexema(lexema, nLinea, nColumna))
                nColumna += len(lexema) + 1
                puntero = 0
        elif caracter.islower():
            lexema, cadena = armar_lexema(cadena[puntero-1:])
            if lexema and cadena:
                nColumna += 1
                listadoLexemas.append(Lexema(lexema, nLinea, nColumna))
                nColumna += len(lexema) + 1
                puntero = 0
        elif caracter == '{' or caracter == '}' or caracter == '[' or caracter == ']' or caracter == ';' or caracter == ',' or caracter == ':':
            lex = Lexema(caracter, nLinea, nColumna)
            if existe(lex) == False:
                listadoLexemas.append(lex)
            cadena = cadena[1:]
            puntero = 0
            nColumna += 1
        elif caracter =="\t":
            nColumna += 4
            cadena = cadena[4:] 
            puntero = 0 
        elif caracter == "\n": 
            cadena = cadena[1:] 
            puntero = 0 
            nLinea += 1
            nColumna = 1
        elif caracter == ' ' or caracter == '\r' or caracter == '.': 
            nColumna += 1
            cadena = cadena[1:] 
            puntero = 0 
        else:
            error = Errores(caracter, nLinea, nColumna)
            listadoErrores.append(error)
            cadena = cadena[1:] 
            puntero = 0 
            nColumna += 1
            
def armar_lexema(cadena):
    global nLinea
    global nColumna
    global listadoLexemas
    lexema = ''
    puntero = ''
 
    for caracter in cadena:
        puntero += caracter 
        if caracter == '"':
            return lexema, cadena[len(puntero):]
        elif caracter == ':':
            return lexema, cadena[len(puntero):]
        elif caracter == '=':
            return lexema, cadena[len(puntero):]
        else:
            lexema += caracter
    return None, None 

def existe(lexema):
    for i in listadoLexemas:
        if i.lexema == lexema.lexema:
            return True
    return False

def armar_diccionarios():
    global listadoLexemas
    global instrucciones
    global lexemas

    for lex in listadoLexemas:
        if lex.lexema == lexemas[lex.lexema]:
            instrucciones.append(lex.lexema)
            
            

extensioncadena = '''Inicio:#{
    Encabezado:{
            TituloPagina:"Ejemplo titulo";
        },#
    Cuerpo:[
        Titulo:{
            texto:"Este es un titulo";
            posicion:"izquierda";
            tamaño:"t1";
            color:"rojo";
        },
        Fondo:{
            color:"cyan";
        },
        Parrafo:{
            texto:"Este es un parrafo de ejemplo.";
            posicion:"izquierda";
        },%
        Texto:{
            fuente="Arial";
            color="azul";
            tamaño="11";
        },
        Codigo:{
            texto:"Muestra el texto con fuente de codigo de ordenador.";
            posicion:"centro";&
        },
        Negrita:{
            texto:"Este texto aparecerá en negrita.";
        },
        Subrayado:{
            texto:"Este texto aparecerá Subrayado.";
        },
        Tachado:{
            texto:"Este texto aparecerá tachado.";
        },
        Cursiva:{
            texto:"Este texto aparecerá en cursiva.";
        },
        Salto:{
            cantidad:"5";
        },
        Tabla:{
            filas:"4";
            columnas:"3";
            elemento:{"fila":"1","columna":"1","Texto mostrado en fila 1 columna 1"};
            elemento:{"fila":"1","columna":"2","Texto mostrado en fila 1 columna 2"};
            elemento:{"fila":"1","columna":"3","Texto mostrado en fila 1 columna 3"};
        },
        Texto:{
            fuente="Arial";
            color="azul";
            tamaño="11";
        },
        Codigo:{
            texto:"Muestra el texto con fuente de codigo de ordenador.";
            posicion:"centro";
        },
        Negrita:{
            texto:"Este texto aparecerá en negrita.";
        },
        Titulo:{
            texto:"Este es un titulo";
            posicion:"izquierda";
            tamaño:"t1";
            color:"rojo";
        }
    ]
}
'''

instruccion(extensioncadena)

# for token in listadoLexemas:
#     print(token.lexema, token.getFila(), token.getColumna())
def getErrores():
    global listadoErrores
    formato = '<table align="center" border="black" height="50%" width="50%">\n'
    formato += '<tr bgcolor="black">\n'
    formato += '<th><font color="white">No.</font</th>\n'
    formato += '<th><font color="white">Lexema</font</th>\n'
    formato += '<th><font color="white">Fila</font</th>\n'
    formato += '<th><font color="white">Columna</font</th>\n'
    formato += '</tr>\n' 
    for i in range(len(listadoErrores)):
        formato += '<tr>\n'
        error = listadoErrores[i]
        formato += error.execute(i+1) + '</tr>\n'
    formato += '</table>\n'
    return formato

nombre = "ListaErrores"+".html"
with open(nombre, 'w') as archivo:
    archivo.write('<!DOCTYPE html>\n')
    archivo.write('<html>\n')
    archivo.write('<head>\n')
    archivo.write('<title>Errores</title>\n')
    archivo.write('</head>\n')
    archivo.write('<body font-size="16">\n')
    archivo.write('<font size="6">\n')
    archivo.write(getErrores())
    archivo.write('</font>\n')
    archivo.write('</body>\n')
    archivo.write('</html>\n')