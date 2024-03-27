import tkinter as tk
from tkinter import filedialog

#importando clases 



class Ventana():
    def __init__(self, root=tk.Tk()):
        self.root = root
        
        self.root.title("Proyecto 1 - Lenguajes Formales y de Programacion")
        self.root.geometry("900x500")
        self.root.resizable(False, False)
        
        self.boton_abrir = tk.Button(self.root, text="Abrir archivo", command=self.abrir_explorador)
        self.boton_abrir.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.entrada = tk.Label(self.root, text="Texto de entrada")
        self.entrada.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        
        self.salida = tk.Label(self.root, text="Traduccion")
        self.salida.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        self.area_entrada = tk.Text(self.root, width=50, height=20)
        self.area_entrada.grid(row=4, column=0, padx=10, pady=10)
        
        self.area_salida = tk.Text(self.root, width=50, height=20, state="disabled")
        self.area_salida.grid(row=4, column=1, padx=10, pady=10)
        
        self.boton_traducir = tk.Button(self.root, text="Traducir", command=self.logica_lfp)
        self.boton_traducir.grid(row=6, column=0, padx=10, pady=10, sticky="e")

    def abrir_explorador(self):
        filepath = filedialog.askopenfilename(initialdir="/", title="Selecciona un archivo",
                                              filetypes=(("Archivos de texto", "*.txt"), 
                                                         ("Todos los archivos", "*.lfp")))
        self.data = [filepath, filepath.split("/")[-1], open(filepath, "r").read()]

    def logica_lfp(self):
        print("logica_lfp")
        ruta, nombre, contenido = self.data # imprimiendo ruta y contenido del archivo
        ruta = ruta.replace(nombre,"") # limpiando ruta para almacenar datos
        
        
    def traducir(self):
        self.area_salida.config(state="normal")
        self.area_salida.delete("1.0", "end")
        contenido = self.area_entrada.get("1.0", "end")
        self.area_salida.insert("1.0", contenido)
        self.area_salida.config(state="disabled")
    
if __name__ == "__main__":
    # instanciando la interfaz
    app = Ventana()
    app.root.mainloop()
    