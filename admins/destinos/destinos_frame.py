import tkinter as tk
from tkinter import ttk, messagebox
from cruds.cruds_destinos import ver_los_destinos
from .destinosForm import DestinosForm


class DestinosFrame(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, padding="10")
        self.controller = controller
        self.pack(fill='both', expand=True)
        self.destinos_tree = None
        self.crear_widgets()

    def crear_widgets(self):
        ttk.Label(self, text="Gestion de destinos",
                  font=("Helvetica", 16, "bold"), foreground='#2D3748').pack(pady=(0, 25), anchor='w')
        columnas = ["ID", "Nombre", "Descripcion", "Actividades", "Costo."]

        self.crear_panel_listado('Destinos')


    def crear_panel_listado(self, entidad):

        listado_frame = ttk.LabelFrame(self, text=f"Listado de {entidad}", padding="15")
        listado_frame.pack(fill='both', expand=True, pady=10)

        columnas = ("id", "nombre", "descripcion", "actividad", "costo")
        self.destinos_tree = ttk.Treeview(listado_frame, columns=columnas, show='headings', style='Treeview')

        self.destinos_tree.heading("id", text="ID")
        self.destinos_tree.heading("nombre", text="Nombre")
        self.destinos_tree.heading("descripcion", text="Descripcion")
        self.destinos_tree.heading("actividad", text="Actividades")
        self.destinos_tree.heading("costo", text="Costo")

        self.destinos_tree.column("id", width=80, anchor=tk.CENTER)
        self.destinos_tree.column("nombre", width=200, anchor=tk.W)
        self.destinos_tree.column("descripcion", width=120, anchor=tk.CENTER)
        self.destinos_tree.column("actividad", width=150, anchor=tk.CENTER)
        self.destinos_tree.column("costo", width=250, anchor=tk.W)

        # Scrollbar y empaquetamiento final
        scrollbar = ttk.Scrollbar(listado_frame, orient="vertical", command=self.destinos_tree.yview)
        self.destinos_tree.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side='right', fill='y')
        self.destinos_tree.pack(side='left', fill='both', expand=True)

        botones_frame = ttk.Frame(self)
        botones_frame.pack(fill='x', pady=10)

        ttk.Button(botones_frame, text="➕ Agregar Destino", style='Action.TButton',
                   command=self.abrir_formulario_crear).pack(side='left', padx=5)
        ttk.Button(botones_frame, text="✏️ Editar Destino", style='Action.TButton',
                   command=self.abrir_formulario_editar).pack(side='left', padx=5)
        ttk.Button(botones_frame, text="❌ Eliminar Destino", style='Action.TButton',
                   command=self.eliminar_empleado).pack(side='left', padx=5)

        self.cargar_datos_destinos()

    def cargar_datos_destinos(self):
        self.destinos_tree.delete(*self.destinos_tree.get_children())

        datos_empleados = ver_los_destinos()

        for item in datos_empleados:
            self.destinos_tree.insert('', tk.END, values=item)

    def abrir_formulario_crear(self):
        DestinosForm(self, callback=self.cargar_datos_destinos)

    def abrir_formulario_editar(self):
        seleccion = self.destinos_tree.selection()
        if seleccion:
            destino_id = self.destinos_tree.item(seleccion)['values'][0]
            DestinosForm(self.master, id_destino=destino_id, callback=self.cargar_datos_destinos)
        else:
            messagebox.showwarning("Advertencia", "Selecciona un destino para editar.")

    def eliminar_empleado(self):
        pass
        """seleccion = self.destinos_tree.selection()
        if seleccion:
            id_destino = self.destinos_tree.item(seleccion)['values'][0]

            respuesta = messagebox.askyesno("Confirmar Eliminación",
                                            f"¿Estás seguro de que deseas eliminar al empleado ID {id_empleado}?")
            if respuesta:
                eliminar_empleado(id_empleado)
                messagebox.showinfo("Adios!", "Empleado eliminado correctamente.")
                self.cargar_datos_empleados()

            else:
                self.cargar_datos_empleados()
        else:
            messagebox.showwarning("Advertencia", "Selecciona un empleado para eliminar.")"""



