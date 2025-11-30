import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from clases.Reservas import Reserva
from cruds.cruds_paquetes import buscar_paquete, ver_nombre_paquetes, buscar_paquete_por_nombre
from cruds.cruds_reservas import obtener_informacion_reserva
from cruds.cruds_usuarios import mostrar_nombres_usuario, buscar_usuario_por_nombre


# Asegúrate de importar tus controladores de Reservas, no de Destinos
# from cruds.cruds_reservas import crear_reserva, actualizar_reserva, buscar_reserva
# from clases.Reservas import Reservas

class ReservasForm(tb.Toplevel):
    def __init__(self, master, callback=None, id_reserva=None):
        super().__init__(master)
        self.master = master
        self.callback = callback
        self.id_reserva = id_reserva

        # Título dinámico
        self.title_text = "Actualizar Reserva" if id_reserva else "Nueva Reserva"
        self.title(self.title_text)
        self.geometry("500x550")  # Ajusté un poco el tamaño
        self.resizable(False, False)

        # Modalidad (bloquea la ventana de atrás)
        self.transient(master)
        self.grab_set()

        # Diccionario para guardar referencias a los inputs
        self.inputs = {}

        self.crear_widgets()

        # Si estamos editando, cargamos datos
        if self.id_reserva is not None:
            self.cargar_datos_reserva(self.id_reserva)

    def crear_widgets(self):
        main_frame = tb.Frame(self, padding="30")
        main_frame.pack(fill='both', expand=True)

        # Título
        tb.Label(main_frame, text=self.title_text, font=("Helvetica", 16, "bold"),
                 bootstyle="primary").pack(pady=(0, 25), anchor="w")

        # --- CAMPO 1: FECHA (Usando DateEntry de ttkbootstrap) ---
        tb.Label(main_frame, text="Fecha de Reserva:", bootstyle="secondary").pack(anchor="w", pady=(5, 0))
        self.inputs['fecha'] = tb.DateEntry(main_frame, bootstyle="primary", firstweekday=0, dateformat="%y-%m-%d")
        self.inputs['fecha'].pack(fill='x', pady=(0, 15))

        # --- CAMPO 2: USUARIO/CLIENTE ---
        tb.Label(main_frame, text="ID Cliente / Usuario:", bootstyle="secondary").pack(anchor="w", pady=(5, 0))
        nombres = mostrar_nombres_usuario()
        self.inputs['usuario'] = tb.Combobox(main_frame, values=nombres, state="readonly")
        self.inputs['usuario'].current(0)
        self.inputs['usuario'].pack(fill='x', pady=(0, 15))

        # --- CAMPO 3: PAQUETE ---
        tb.Label(main_frame, text="Paquete:", bootstyle="secondary").pack(anchor="w", pady=(5, 0))
        paquetes = ver_nombre_paquetes()
        paquetes_limpio =[p[0] for p in paquetes]
        self.inputs['paquete'] = tb.Combobox(main_frame, values=paquetes_limpio, state="readonly")
        self.inputs['paquete'].current(0)
        self.inputs['paquete'].pack(fill='x', pady=(0, 15))

        # --- CAMPO 4: ESTADO (Usando Combobox) ---
        tb.Label(main_frame, text="Estado:", bootstyle="secondary").pack(anchor="w", pady=(5, 0))
        estados = ["Pendiente", "Confirmada", "Cancelada", "Completada"]
        self.inputs['estado'] = tb.Combobox(main_frame, values=estados, state="readonly")
        self.inputs['estado'].current(0)  # Seleccionar 'Pendiente' por defecto
        self.inputs['estado'].pack(fill='x', pady=(0, 15))

        # --- BOTÓN DE ACCIÓN ---
        texto_boton = "Guardar Reserva" if self.id_reserva is None else "Actualizar Reserva"

        btn_guardar = tb.Button(
            main_frame,
            text=texto_boton,
            bootstyle="success",  # Color verde automático
            command=self.guardar_actualizar_reserva
        )
        btn_guardar.pack(fill='x', pady=30)

    def guardar_actualizar_reserva(self):
        # Recolección de datos
        # Nota: DateEntry devuelve la fecha con .entry.get()
        data = {
            "fecha": self.inputs['fecha'].entry.get(),
            "usuario": self.inputs['usuario'].get(),
            "paquete": self.inputs['paquete'].get(),
            "estado": self.inputs['estado'].get()
        }

        # Validación básica
        if not all(data.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            if self.id_reserva is None:
                id_usuario = buscar_usuario_por_nombre(data['usuario'])
                id_paquete = buscar_paquete_por_nombre(data['paquete'])
                nueva_reserva = Reserva(data['fecha'], id_usuario, id_paquete, data['estado'])
                nueva_reserva.guardar()
                messagebox.showinfo("Éxito", "Reserva creada correctamente.")
            else:
                # Lógica de ACTUALIZAR
                id_usuario = buscar_usuario_por_nombre(data['usuario'])
                id_paquete = buscar_paquete_por_nombre(data['paquete'])
                print(data['fecha'], id_usuario, id_paquete, data['estado'])
                reserva_actualizada = Reserva(data['fecha'], id_usuario, id_paquete, data['estado'])
                reserva_actualizada.actualizar(self.id_reserva)
                messagebox.showinfo("Éxito", "Reserva actualizada correctamente.")

            if self.callback:
                self.callback()

            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def cargar_datos_reserva(self, id_reserva):
        # Aquí deberías llamar a tu función real: buscar_reserva(id_reserva)
        # Simulamos datos para el ejemplo visual:
        reserva = obtener_informacion_reserva(self.id_reserva)
        """datos_simulados = {
            "fecha": reserva[1],
            "paquete": "Cancún Todo Incluido",
            "estado": "Confirmada"
        }

        # Cargar datos en los widgets
        self.inputs['fecha'].entry.delete(0, tk.END)
        self.inputs['fecha'].entry.insert(0, datos_simulados['fecha'])

        self.inputs['usuario'].delete(0, tk.END)
        self.inputs['usuario'].insert(0, datos_simulados['usuario'])

        self.inputs['paquete'].delete(0, tk.END)
        self.inputs['paquete'].insert(0, datos_simulados['paquete'])

        self.inputs['estado'].set(datos_simulados['estado'])"""