import tkinter as tk
from tkinter import ttk, messagebox
from cruds.cruds_destinos import insertar_destino
from clases.Destinos import Destinos


class DestinosForm(tk.Toplevel):
    #Este es el formulario para crear un usuario en el sistema!

    def __init__(self, master, callback=None, id_destino = None):
        super().__init__(master)
        self.entries = None
        self.master = master
        self.callback = callback
        self.id_destino = id_destino

        self.title_text = "Crear Nuevo Destino"
        self.title(self.title_text)
        self.geometry("650x600")
        self.transient(master)
        self.grab_set()
        self.resizable(False, False)

        # Estilo para la ventana Toplevel
        style = ttk.Style()
        style.configure('TLabel', font=('Helvetica', 10))
        style.configure('TEntry', font=('Helvetica', 10))
        style.configure('TButton', font=('Helvetica', 10, 'bold'))
        style.configure('Accent.TButton', background='#48BB78', foreground='white')
        style.map('Accent.TButton', background=[('active', '#38A169')])

        self.crear_widgets()

    def crear_widgets(self):
        main_frame = ttk.Frame(self, padding="30")  # Más padding
        main_frame.pack(fill='both', expand=True)

        ttk.Label(main_frame, text=self.title_text, font=("Helvetica", 16, "bold"),
                  foreground='#2D3748').grid(row=0, column=0, columnspan=2, pady=(0, 25), sticky="w")

        # Configuración de la cuadrícula
        main_frame.grid_columnconfigure(0, weight=0)  # Etiqueta fija
        main_frame.grid_columnconfigure(1, weight=1)  # Entrada expandible


        # Campos de texto y entrada
        campos = [
            ("Nombre:", "nombre"),
            ("Descripcion:", "descripcion"),
            ("Actividades:", "actividades"),
            ("Costo:", "costo")
            ]

        self.entries = {}
        row_num = 1
        for label_text, key in campos:

            ttk.Label(main_frame, text=label_text, width=30).grid(row=row_num, column=0, sticky="w", pady=7)  # Más pady

            entry = ttk.Entry(main_frame, width=50)  # Mayor ancho
            entry.grid(row=row_num, column=1, sticky="ew", pady=7)
            self.entries[key] = entry



            row_num += 1

        btn_guardar = ttk.Button(main_frame, text="Agregar destino",
                                 command=self.crear_destino, style='Accent.TButton')
        btn_guardar.grid(row=row_num, column=0, columnspan=2, pady=30, sticky="n")

    def crear_destino(self):
        #Validar y crear usuario
        data = {key: entry.get() for key, entry in self.entries.items()}


        try:
            # Requisito: Validación de Entradas Seguras
            if not all([data['nombre'], data['actividades'], data['costo']]):
                messagebox.showerror("Error de Validación",
                                     "Los campos Nombre, Actividades y Costo son obligatorios.")
                return

            nuevo_destino = Destinos(data['nombre'], data['descripcion'], data['actividades'], data['costo'], 25)
            nuevo_destino.insertar_destino()
            messagebox.showinfo("Correcto!", "Destino registrado correctamente.")
            if self.callback:
                self.callback()  # Refresca el listado en el Dashboard

            self.destroy()


        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")





    def actualizar_destino(self):

        data = {key: entry.get() for key, entry in self.entries.items()}

        # Requisito: Validación de Entradas Seguras
        if not all([data['nombre'], data['actividades'], data['costo']]):
            messagebox.showerror("Error de Validación",
                                 "Los campos Nombre, actividades y costo son obligatorios.")
            return

        destino_editar = Destinos(data['nombre'],data['descripcion'], data['actividades'], data['costo'], 25)
        destino_editar.actualizar_destino(self.id_destino)

        if self.callback:
            self.callback()  # Refresca el listado en el Dashboard

        self.destroy()

