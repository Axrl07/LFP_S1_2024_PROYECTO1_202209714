
# from analizadorLexico import Analizador

# contenido = open("prueba copy.lfp", "r").read()
# x = Analizador().progreso(contenido)
# tipo = type(x)

# if tipo == list:
#     print(f'Error la etiqueta {x[0]} se repite {x[1]} veces en el archivo')
# if tipo == str and x == "errores generados en archivo ListaErrores.html":
#     print(x)
#     print("Verifica el archivo de entrada")
# else:
#     print("Archivo traducido con exito", f"resultado de variable: {x}")
#     del x
#     del tipo

# diccionario = {
#     'elemento7': {'fila': '4', 'contenido': 'Texto mostrado en fila 1 columna 1', 'columna': '1'},
#     'filas': '4',
#     'elemento6': {'fila': '4', 'contenido': 'Texto mostrado en fila 1 columna 2', 'columna': '2'},
#     'columnas': '3',
#     'elemento0': {'fila': '1', 'contenido': 'Texto mostrado en fila 1 columna 1', 'columna': '1'},
#     'elemento1': {'fila': '1', 'contenido': 'Texto mostrado en fila 1 columna 2', 'columna': '2'},
#     'elemento2': {'fila': '1', 'contenido': 'Texto mostrado en fila 1 columna 3', 'columna': '3'},
#     'elemento4': {'fila': '2', 'contenido': 'Texto mostrado en fila 1 columna 1', 'columna': '1'},
#     'elemento5': {'fila': '3', 'contenido': 'Texto mostrado en fila 1 columna 2', 'columna': '2'}
# }

# # Leer el número de filas y columnas
# num_filas = int(diccionario['filas'])
# num_columnas = int(diccionario['columnas'])

# # Iniciar el código HTML de la tabla
# tabla_html = '<table border="1">\n'

# # Recorrer las filas y columnas para construir la tabla
# for i in range(num_filas):
#     tabla_html += '  <tr>\n'
#     for j in range(num_columnas):
#         encontrado = False
#         for k in range(num_filas * num_columnas):
#             clave_elemento = f'elemento{k}'
#             celda = diccionario.get(clave_elemento, {})
#             fila_celda = int(celda.get('fila', '0')) - 1
#             columna_celda = int(celda.get('columna', '0')) - 1
#             if fila_celda == i and columna_celda == j:
#                 contenido = celda.get('contenido', '')
#                 tabla_html += f'    <td>{contenido}</td>\n'
#                 encontrado = True
#                 break
#         if not encontrado:
#             tabla_html += '    <td></td>\n'
#     tabla_html += '  </tr>\n'

# # Cerrar el código HTML de la tabla
# tabla_html += '</table>'

# print(tabla_html)
