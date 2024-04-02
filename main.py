# importando tkinter
import tkinter as tk
from tkinter import filedialog
from tkinter import font

#importando clase Analizador 
from analizadorLexico import Analizador

class Ventana():
    def __init__(self, root=tk.Tk()):
        self.root = root
        self.data = []
        
        self.root.title("Proyecto 1 - Lenguajes Formales y de Programacion")
        ancho_ventana = self.root.winfo_reqwidth()
        alto_ventana = self.root.winfo_reqheight()
        pos_x = int(self.root.winfo_screenwidth() / 4 - ancho_ventana / 4)
        pos_y = int(self.root.winfo_screenheight() / 4 - alto_ventana / 4)
        self.root.geometry(f"900x550+{pos_x}+{pos_y}")
        
        self.root.resizable(False, False)
        
        self.boton_abrir = tk.Button(self.root, text="Abrir archivo", command=self.abrir_explorador)
        self.boton_abrir.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.boton_borrar_entrada = tk.Button(self.root, text="Borrar entrada", command=lambda: self.area_entrada.delete("1.0", "end"))
        self.boton_borrar_entrada.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        self.boto_borrar_salida = tk.Button(self.root, text="Borrar salida", command=self.borrar)
        self.boto_borrar_salida.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        self.entrada = tk.Label(self.root, text="Texto de entrada")
        self.entrada.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        
        self.salida = tk.Label(self.root, text="Traduccion")
        self.salida.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        self.area_entrada = tk.Text(self.root, width=50, height=20)
        self.area_entrada.grid(row=4, column=0, padx=10, pady=10)
        
        self.area_salida = tk.Text(self.root, width=50, height=20, state="disabled")
        self.area_salida.grid(row=4, column=1, padx=10, pady=10)
        
        self.boton_traducir = tk.Button(self.root, text="Traducir", command=self.traducir)
        self.boton_traducir.grid(row=6, column=0, padx=10, pady=10, sticky="e")

    def borrar(self):
        self.area_salida.config(state="normal")
        self.area_salida.delete("1.0", "end")
        self.area_salida.config(state="disabled")
        
    def abrir_explorador(self):
        filepath = filedialog.askopenfilename(initialdir="/", title="Selecciona un archivo",
                                              filetypes=(("Archivos de texto", "*.json"), ("Archivos de texto", "*.lfp"),
                                                         ("Todos los archivos", "*.*")))
        self.data = [filepath, filepath.split("/")[-1], open(filepath, "r").read()]
        self.area_entrada.delete("1.0", "end")
        self.area_entrada.insert("1.0", str(self.data[2]))

    def ventanMensaje(self, contenido, advertencia="error"):
        ventana = tk.Tk()
        if advertencia == "error":
            ventana.title("Errores")
        else:
            ventana.title("Mensaje")

        # Centrar la ventana de errores
        ancho_ventana = ventana.winfo_reqwidth()
        alto_ventana = ventana.winfo_reqheight()

        pos_x = int(ventana.winfo_screenwidth() / 4 - ancho_ventana / 4)
        pos_y = int(ventana.winfo_screenheight() / 4 - alto_ventana / 4)

        ventana.geometry(f"600x200+{pos_x}+{pos_y}")

        ventana.resizable(False, False)
        
        fuente = font.Font(size=12)
        negrita = font.Font(size=12, weight="bold")
        
        enunciado = tk.Label(ventana, text=contenido, font=negrita)
        enunciado.pack(expand=True, fill="both")
        
        if advertencia == "error":
            enunciado2 = tk.Label(ventana, text=f"Verifica el archivo de entrada {self.data[1]}", font=fuente)
            enunciado2.pack(expand=True, fill="both")
        else:
            pass

        ventana.mainloop()

    def traducir(self):
        entrada = len(str(self.area_entrada.get("1.0", "end")))
        
        if entrada <= 5:
           return self.ventanMensaje("No hay contenido para traducir")
        else:
            # configurando contenido
            aux, nombre, contenidoArchivo = self.data
            ruta = aux.replace(nombre, "")
            contenidoArea = str(self.area_entrada.get("1.0", "end"))
            contenido = ""
            if contenidoArchivo != contenidoArea:
                contenido = contenidoArea
            else:
                contenido = contenidoArchivo
            # analizandor lexico
            ejecucion = Analizador().progreso(contenido)
            if type(ejecucion) == list:
                self.area_entrada.delete("1.0", "end")
                self.area_salida.config(state="normal")
                self.area_salida.delete("1.0", "end")
                self.area_salida.insert("1.0", "Error")
                self.area_salida.config(state="disabled")
                if ejecucion[0] != "Encabezado" and ejecucion[0] != "Cuerpo" and ejecucion[0] != "Inicio":
                    er, con = ejecucion
                    self.area_salida.config(state="normal")
                    self.area_salida.delete("1.0", "end")
                    self.area_salida.insert("1.0", con)
                    self.area_salida.config(state="disabled")
                    self.ventanMensaje(er)
                else:
                    self.ventanMensaje(f'Error la etiqueta {ejecucion[0]} se repite {ejecucion[1]} veces en el archivo')
                del ejecucion
            elif ejecucion == "errores generados en archivo ListaErrores.html":
                self.area_entrada.delete("1.0", "end")
                self.area_salida.config(state="normal")
                self.area_salida.delete("1.0", "end")
                self.area_salida.insert("1.0", "Errores generados en archivo ListaErrores.html")
                self.area_salida.config(state="disabled")
                self.ventanMensaje(ejecucion)
                del ejecucion
            else:
                men, con = ejecucion
                self.area_salida.config(state="normal")
                self.area_salida.delete("1.0", "end")
                self.area_salida.insert("1.0", con)
                self.area_salida.config(state="disabled")
                self.ventanMensaje(men, "men")
                del ejecucion
    
if __name__ == "__main__":
    # instanciando la interfaz
    app = Ventana()
    app.root.mainloop()
    