import tkinter as tk
from tkinter import ttk, messagebox
from cruds.cruds_reservas import ver_reservas, eliminar_reserva
from .reservasForm import ReservasForm



class ReservasFrame(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, padding="10")
        self.controller = controller
        self.pack(fill='both', expand=True)
        self.reservas_tree = None
        self.crear_widgets()

    def crear_widgets(self):
        ttk.Label(self, text="Gestion de Reservas",
                  font=("Helvetica", 16, "bold"), foreground='#2D3748').pack(pady=(0, 25), anchor='w')
        columnas = ["ID", "Nombre", "Descripcion", "Actividades", "Costo."]

        self.crear_panel_listado('Reservas')


    def crear_panel_listado(self, entidad):

        listado_frame = ttk.LabelFrame(self, text=f"Listado de {entidad}", padding="15")
        listado_frame.pack(fill='both', expand=True, pady=10)

        columnas = ("id", "fecha", "usuario", "paquete", "estado")
        self.reservas_tree = ttk.Treeview(listado_frame, columns=columnas, show='headings', style='Treeview')

        self.reservas_tree.heading("id", text="ID")
        self.reservas_tree.heading("fecha", text="Fecha")
        self.reservas_tree.heading("usuario", text="Cliente")
        self.reservas_tree.heading("paquete", text="Paquete")
        self.reservas_tree.heading("estado", text="Estado")

        self.reservas_tree.column("id", width=80, anchor=tk.CENTER)
        self.reservas_tree.column("fecha", width=200, anchor=tk.W)
        self.reservas_tree.column("usuario", width=120, anchor=tk.CENTER)
        self.reservas_tree.column("paquete", width=150, anchor=tk.CENTER)
        self.reservas_tree.column("estado", width=250, anchor=tk.W)

        # Scrollbar y empaquetamiento final
        scrollbar = ttk.Scrollbar(listado_frame, orient="vertical", command=self.reservas_tree.yview)
        self.reservas_tree.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side='right', fill='y')
        self.reservas_tree.pack(side='left', fill='both', expand=True)

        botones_frame = ttk.Frame(self)
        botones_frame.pack(fill='x', pady=10)

        #ttk.Button(botones_frame, text="➕ Agregar Destino", style='Action.TButton',
                   #command=self.abrir_formulario_crear).pack(side='left', padx=5)
        ttk.Button(botones_frame, text="✏️ Editar Reserva", style='Action.TButton',
                   command=self.abrir_formulario_editar).pack(side='left', padx=5)
        ttk.Button(botones_frame, text="❌ Eliminar Reserva", style='Action.TButton',
                   command=self.eliminar_reserva).pack(side='left', padx=5)

        self.cargar_datos_reservas()

    def cargar_datos_reservas(self):
        self.reservas_tree.delete(*self.reservas_tree.get_children())

        datos_reservas = ver_reservas()

        for item in datos_reservas:
            self.reservas_tree.insert('', tk.END, values=item)

    def abrir_formulario_crear(self):
        ReservasForm(self, callback=self.cargar_datos_reservas)

    def abrir_formulario_editar(self):
        seleccion = self.reservas_tree.selection()
        if seleccion:
            reserva_id = self.reservas_tree.item(seleccion)['values'][0]
            ReservasForm(self.master, id_reserva=reserva_id, callback=self.cargar_datos_reservas)
        else:
            messagebox.showwarning("Advertencia", "Selecciona una reserva para editar.")

    def eliminar_reserva(self):
        seleccion = self.reservas_tree.selection()
        if seleccion:
            id_reserva = self.reservas_tree.item(seleccion)['values'][0]

            respuesta = messagebox.askyesno("Confirmar Eliminación",
                                            f"¿Estás seguro de que deseas eliminar la reserva ID {id_reserva}?")
            if respuesta:
                eliminar_reserva(id_reserva)
                messagebox.showinfo("Adios!", "Reserva eliminada correctamente.")
                self.cargar_datos_reservas()

            else:
                self.cargar_datos_reservas()
        else:
            messagebox.showwarning("Advertencia", "Selecciona una reserva para eliminar.")



