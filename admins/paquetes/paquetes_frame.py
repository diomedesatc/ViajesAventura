import tkinter as tk
from tkinter import ttk, messagebox
from cruds.cruds_paquetes import ver_paquetes, eliminar_paquete
from .paquetesForm import PaquetesForm


class PaquetesFrame(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, padding="10")
        self.controller = controller
        self.pack(fill='both', expand=True)
        self.paquetes_tree = None
        self.crear_widgets()

    def crear_widgets(self):
        ttk.Label(self, text="Gestion de paquetes",
                  font=("Helvetica", 16, "bold"), foreground='#2D3748').pack(pady=(0, 25), anchor='w')
        columnas = ["ID", "Nombre", "Fecha Inicio", "Fecha Fin", "Destinos","Precio", "Capacidad Actual"]

        self.crear_panel_listado('Paquetes')


    def crear_panel_listado(self, entidad):

        listado_frame = ttk.LabelFrame(self, text=f"Listado de {entidad}", padding="15")
        listado_frame.pack(fill='both', expand=True, pady=10)

        columnas = ("id", "nombre", "fecha_inicio", "fecha_fin", "precio", "cupos_disponibles")
        self.paquetes_tree = ttk.Treeview(listado_frame, columns=columnas, show='headings', style='Treeview')

        self.paquetes_tree.heading("id", text="ID")
        self.paquetes_tree.heading("nombre", text="Nombre")
        self.paquetes_tree.heading("fecha_inicio", text="Fecha Inicio")
        self.paquetes_tree.heading("fecha_fin", text="Fecha Fin")
        self.paquetes_tree.heading("precio", text="Precio")
        self.paquetes_tree.heading("cupos_disponibles", text="Capacidad Actual")

        self.paquetes_tree.column("id", width=80, anchor=tk.CENTER)
        self.paquetes_tree.column("nombre", width=200, anchor=tk.W)
        self.paquetes_tree.column("fecha_inicio", width=120, anchor=tk.CENTER)
        self.paquetes_tree.column("fecha_fin", width=150, anchor=tk.CENTER)
        self.paquetes_tree.column("precio", width=250, anchor=tk.W)
        self.paquetes_tree.column("cupos_disponibles", width=150, anchor=tk.CENTER)


        # Scrollbar y empaquetamiento final
        scrollbar = ttk.Scrollbar(listado_frame, orient="vertical", command=self.paquetes_tree.yview)
        self.paquetes_tree.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side='right', fill='y')
        self.paquetes_tree.pack(side='left', fill='both', expand=True)

        botones_frame = ttk.Frame(self)
        botones_frame.pack(fill='x', pady=10)

        ttk.Button(botones_frame, text="➕ Agregar Paquete", style='Action.TButton',
                   command=self.abrir_formulario_crear).pack(side='left', padx=5)
        ttk.Button(botones_frame, text="✏️ Editar Paquete", style='Action.TButton',
                   command=self.abrir_formulario_editar).pack(side='left', padx=5)
        ttk.Button(botones_frame, text="❌ Eliminar Paquete", style='Action.TButton',
                   command=self.eliminar_paquete).pack(side='left', padx=5)

        self.cargar_datos_paquetes()

    def cargar_datos_paquetes(self):
        self.paquetes_tree.delete(*self.paquetes_tree.get_children())

        datos_paquetes = ver_paquetes()

        for item in datos_paquetes:
            self.paquetes_tree.insert('', tk.END, values=item)

    def abrir_formulario_crear(self):
        PaquetesForm(self, callback=self.cargar_datos_paquetes)

    def abrir_formulario_editar(self):
        seleccion = self.paquetes_tree.selection()
        if seleccion:
            paquete_id = self.paquetes_tree.item(seleccion)['values'][0]
            PaquetesForm(self.master,  callback=self.cargar_datos_paquetes,id_paquete=paquete_id)
        else:
            messagebox.showwarning("Advertencia", "Selecciona un paquete para editar.")

    def eliminar_paquete(self):
        seleccion = self.paquetes_tree.selection()
        if seleccion:
            id_paquete = self.paquetes_tree.item(seleccion)['values'][0]

            respuesta = messagebox.askyesno("Confirmar Eliminación",
                                            f"¿Estás seguro de que deseas eliminar el paquete ID {id_paquete}?")
            if respuesta:
                eliminar_paquete(id_paquete)
                messagebox.showinfo("Adios!", "Paquete eliminado correctamente.")
                self.cargar_datos_paquetes()

            else:
                self.cargar_datos_paquetes()
        else:
            messagebox.showwarning("Advertencia", "Selecciona un paquete para eliminar.")



