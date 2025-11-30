import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb  # Importamos ttkbootstrap
from ttkbootstrap.constants import *  # Importamos constantes como PRIMARY, DANGER, etc.

# Asumiendo que tus imports funcionan igual
from cruds.cruds_reservas import ver_reservas, eliminar_reserva, cancelar_reserva
from .reservasForm import ReservasForm


class ReservasFrame(tb.Frame):  # <--- Cambio 1: Heredamos de tb.Frame
    def __init__(self, master, controller):
        super().__init__(master, padding="10")
        self.controller = controller
        self.pack(fill='both', expand=True)
        self.reservas_tree = None
        self.crear_widgets()

    def crear_widgets(self):
        # Usamos tb.Label. Podemos mantener tus fuentes personalizadas o usar bootstyle="inverse-primary"
        tb.Label(self, text="Gestión de Reservas",
                 font=("Helvetica", 16, "bold"),
                 bootstyle="primary").pack(pady=(0, 25), anchor='w')

        self.crear_panel_listado('Reservas')

    def crear_panel_listado(self, entidad):
        # Cambio 2: tb.LabelFrame con un estilo de color
        listado_frame = tb.Labelframe(self, text=f"Listado de {entidad}", padding="15", bootstyle="info")
        listado_frame.pack(fill='both', expand=True, pady=10)

        columnas = ("id", "fecha", "usuario", "paquete", "estado")

        # Cambio 3: tb.Treeview con estilo 'striped' (filas alternas)
        self.reservas_tree = tb.Treeview(
            listado_frame,
            columns=columnas,
            show='headings',
            bootstyle="primary"  # Colorea las cabeceras
        )

        self.reservas_tree.heading("id", text="ID")
        self.reservas_tree.heading("fecha", text="Fecha")
        self.reservas_tree.heading("usuario", text="Cliente")
        self.reservas_tree.heading("paquete", text="Paquete")
        self.reservas_tree.heading("estado", text="Estado")

        self.reservas_tree.column("id", width=50, anchor=tk.CENTER)
        self.reservas_tree.column("fecha", width=150, anchor=tk.W)
        self.reservas_tree.column("usuario", width=120, anchor=tk.CENTER)
        self.reservas_tree.column("paquete", width=150, anchor=tk.CENTER)
        self.reservas_tree.column("estado", width=150, anchor=tk.W)

        # Cambio 4: tb.Scrollbar (se ve más redondeado y moderno)
        scrollbar = tb.Scrollbar(listado_frame, orient="vertical", command=self.reservas_tree.yview, bootstyle="round")
        self.reservas_tree.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side='right', fill='y')
        self.reservas_tree.pack(side='left', fill='both', expand=True)

        botones_frame = tb.Frame(self)
        botones_frame.pack(fill='x', pady=10)

        # Cambio 5: Botones con bootstyle (colores automáticos)
        # Editar -> Warning (Amarillo/Naranja)
        tb.Button(botones_frame, text="Editar Reserva",
                  bootstyle="warning",  # <--- Estilo visual
                  command=self.abrir_formulario_editar).pack(side='left', padx=5)

        # Eliminar -> Danger (Rojo)
        tb.Button(botones_frame, text="Cancelar Reserva",
                  bootstyle="danger",  # <--- Estilo visual
                  command=self.eliminar_reserva).pack(side='left', padx=5)

        self.cargar_datos_reservas()

    def cargar_datos_reservas(self):
        # Limpiar datos antiguos
        self.reservas_tree.delete(*self.reservas_tree.get_children())

        datos_reservas = ver_reservas()

        # Inserción de datos (igual que antes)
        if datos_reservas:
            for item in datos_reservas:
                self.reservas_tree.insert('', tk.END, values=item)

    def abrir_formulario_crear(self):
        # Nota: Asegúrate de que ReservasForm acepte 'self' o 'self.master' correctamente
        ReservasForm(self, callback=self.cargar_datos_reservas)

    def abrir_formulario_editar(self):
        seleccion = self.reservas_tree.selection()
        if seleccion:
            reserva_id = self.reservas_tree.item(seleccion)['values'][0]
            # Pasamos self.master o self dependiendo de como funcione tu Toplevel
            ReservasForm(self.master, id_reserva=reserva_id, callback=self.cargar_datos_reservas)
        else:
            messagebox.showwarning("Advertencia", "Selecciona una reserva para editar.")

    def eliminar_reserva(self):
        seleccion = self.reservas_tree.selection()
        if seleccion:
            id_reserva = self.reservas_tree.item(seleccion)['values'][0]

            # Nota: Podrías usar Messagebox de ttkbootstrap también, pero el estandard funciona bien
            respuesta = messagebox.askyesno("Confirmar Cancelacion",
                                            f"¿Estás seguro de que deseas cancelar la reserva ID {id_reserva}?")
            if respuesta:
                cancelar_reserva(id_reserva)
                messagebox.showinfo("Éxito", "Reserva eliminada correctamente.")
                self.cargar_datos_reservas()
        else:
            messagebox.showwarning("Advertencia", "Selecciona una reserva para cancelar.")