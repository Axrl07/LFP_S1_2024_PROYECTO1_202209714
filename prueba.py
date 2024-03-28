
from analizadorLexico import Analizador

contenido = open("prueba.json", "r").read()
x = Analizador().analizar_entrada(contenido)
tipo = type(x)

if tipo == list:
    print(f'Error la etiqueta {x[0]} se repite {x[1]} veces en el archivo')
if tipo == str and x == "errores generados en archivo ListaErrores.html":
    print(x)
    print("Verifica el archivo de entrada")
else:
    print("Archivo traducido con exito", f"resultado de variable: {x}")
    del x
    del tipo