import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from cruds.cruds_destinos import buscar_destino
from clases.Destinos import Destinos


class DestinosForm(tb.Toplevel):
    """
    Formulario modal para Crear o Actualizar un destino usando ttkbootstrap.
    """

    def __init__(self, master, callback=None, id_destino=None):
        super().__init__(master)
        self.entries = None
        self.callback = callback
        self.id_destino = id_destino

        # Título y Configuración de Ventana
        self.title_text = "Actualizar Destino" if id_destino else "Crear Nuevo Destino"
        self.title(self.title_text)
        self.geometry("600x550")

        # Comportamiento Modal (Bloquea la ventana padre)
        self.transient(master)
        self.grab_set()
        self.resizable(False, False)

        # Iniciar interfaz
        self.crear_widgets()

        # Cargar datos si es edición
        if self.id_destino is not None:
            self.cargar_datos_simulados(self.id_destino)

    def crear_widgets(self):
        # Frame principal con padding
        main_frame = tb.Frame(self, padding=30)
        main_frame.pack(fill=BOTH, expand=True)

        # Título del Formulario
        lbl_titulo = tb.Label(
            main_frame,
            text=self.title_text,
            font=("Helvetica", 18, "bold"),
            bootstyle="primary"
        )
        lbl_titulo.grid(row=0, column=0, columnspan=2, pady=(0, 30), sticky="w")

        # Configuración de la cuadrícula
        main_frame.columnconfigure(1, weight=1)  # La columna 1 (inputs) se expande

        # Campos del formulario
        campos = [
            ("Nombre:", "nombre"),
            ("Descripción:", "descripcion"),
            ("Actividades:", "actividades"),
            ("Costo:", "costo")
        ]

        self.entries = {}

        for i, (label_text, key) in enumerate(campos, start=1):
            # Etiqueta
            tb.Label(main_frame, text=label_text, font=("Helvetica", 10)).grid(row=i, column=0, sticky="w", pady=10)

            # Campo de entrada (Entry)
            entry = tb.Entry(main_frame, bootstyle="primary")
            entry.grid(row=i, column=1, sticky="ew", padx=(10, 0), pady=10)

            self.entries[key] = entry

        # Botón de Acción
        texto_boton = "💾 Guardar Cambios" if self.id_destino else "➕ Agregar Destino"

        btn_guardar = tb.Button(
            main_frame,
            text=texto_boton,
            bootstyle="success",  # Color verde estilo bootstrap
            width=20,
            command=self.guardar_actualizar_destino
        )
        btn_guardar.grid(row=len(campos) + 1, column=0, columnspan=2, pady=40)

    def crear_destino(self):
        # Recolectar datos
        data = {key: entry.get() for key, entry in self.entries.items()}

        try:
            # Validación simple
            if not all([data['nombre'], data['actividades'], data['costo']]):
                messagebox.showerror("Error de Validación", "Los campos Nombre, Actividades y Costo son obligatorios.")
                return

            # Crear instancia (Nota: el 25 es un valor hardcodeado que tenías originalmente, asumo que es cupos o stock)
            nuevo_destino = Destinos(data['nombre'], data['descripcion'], data['actividades'], data['costo'], 25)
            nuevo_destino.insertar_destino()

            messagebox.showinfo("¡Éxito!", "Destino registrado correctamente.")

            if self.callback:
                self.callback()  # Refresca la tabla en el dashboard

            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al crear: {e}")

    def actualizar_destino(self):
        data = {key: entry.get() for key, entry in self.entries.items()}

        if not all([data['nombre'], data['actividades'], data['costo']]):
            messagebox.showerror("Error de Validación", "Los campos Nombre, Actividades y Costo son obligatorios.")
            return

        try:
            destino_editar = Destinos(data['nombre'], data['descripcion'], data['actividades'], data['costo'], 25)
            destino_editar.actualizar_destino(self.id_destino)

            messagebox.showinfo("¡Éxito!", "Destino actualizado correctamente.")

            if self.callback:
                self.callback()

            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al actualizar: {e}")

    def guardar_actualizar_destino(self):
        if self.id_destino is None:
            self.crear_destino()
        else:
            self.actualizar_destino()

    def cargar_datos_simulados(self, id_destino: int):
        destino = buscar_destino(id_destino)
        if destino:
            # Mapeo según el orden de columnas de tu base de datos
            datos_destino = {
                "nombre": destino[1],
                "descripcion": destino[2],
                "actividades": destino[3],
                "costo": destino[4]
            }

            for key, value in datos_destino.items():
                if key in self.entries:
                    self.entries[key].delete(0, END)  # END viene de constants
                    self.entries[key].insert(0, value)