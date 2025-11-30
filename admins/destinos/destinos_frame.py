import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from cruds.cruds_destinos import ver_los_destinos, eliminar_destino
from .destinosForm import DestinosForm


class DestinosFrame(tb.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        self.controller = controller

        # Área donde se dibujarán las tarjetas
        self.scrollable_content = None

        self.crear_widgets()

    def crear_widgets(self):
        # --- HEADER (Título + Botón Agregar) ---
        header_frame = tb.Frame(self)
        header_frame.pack(fill=X, pady=(0, 20))

        # Título
        tb.Label(header_frame, text="Gestión de Destinos",
                 font=("Helvetica", 18, "bold"),
                 bootstyle="primary").pack(side=LEFT)

        # Botón Agregar (Ahora está arriba)
        tb.Button(header_frame, text="➕ Nuevo Destino", bootstyle="success",
                  command=self.abrir_formulario_crear).pack(side=RIGHT)

        # --- ÁREA DE CONTENIDO CON SCROLL ---
        # Crear un contenedor que permita hacer scroll
        self.crear_area_scroll()

        # Cargar los datos iniciales
        self.cargar_datos_destinos()

    def crear_area_scroll(self):
        # 1. Canvas (El lienzo deslizable)
        canvas = tk.Canvas(self, highlightthickness=0)

        # 2. Scrollbar vertical linkeado al canvas
        scrollbar = tb.Scrollbar(self, orient="vertical", command=canvas.yview, bootstyle="round")

        # 3. Frame interno (Aquí irán las tarjetas)
        self.scrollable_content = tb.Frame(canvas)

        # Configurar que el frame interno crezca con el contenido
        self.scrollable_content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Crear la ventana dentro del canvas
        # window_height se ajusta solo, width intentamos que ocupe el ancho disponible
        canvas_window = canvas.create_window((0, 0), window=self.scrollable_content, anchor="nw")

        # Función para que el ancho de las tarjetas se ajuste al redimensionar la ventana
        def configurar_ancho(event):
            canvas.itemconfig(canvas_window, width=event.width)

        canvas.bind("<Configure>", configurar_ancho)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Empaquetar (Layout)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Habilitar scroll con rueda del mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        # Bindear eventos de mouse solo cuando entra al área
        self.scrollable_content.bind('<Enter>', lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        self.scrollable_content.bind('<Leave>', lambda e: canvas.unbind_all("<MouseWheel>"))

    def cargar_datos_destinos(self):
        # 1. Limpiar tarjetas antiguas
        for widget in self.scrollable_content.winfo_children():
            widget.destroy()

        # 2. Obtener datos
        datos_destinos = ver_los_destinos()

        if not datos_destinos:
            tb.Label(self.scrollable_content, text="No hay destinos registrados.", font=("Helvetica", 12)).pack(pady=20)
            return

        # 3. Configuración de la Grid (Cuadrícula)
        columnas_por_fila = 3  # Cuántas tarjetas quieres por fila
        col = 0
        row = 0

        # Configurar peso de columnas para que se expandan igual
        for i in range(columnas_por_fila):
            self.scrollable_content.columnconfigure(i, weight=1)

        # 4. Crear tarjetas
        for destino in datos_destinos:
            # Desempaquetar datos (Asegúrate que coincida con tu select de BD)
            # id, nombre, descripcion, actividad, costo
            d_id, d_nom, d_desc, d_act, d_costo = destino

            self.crear_tarjeta(d_id, d_nom, d_desc, d_act, d_costo, row, col)

            # Lógica de grid
            col += 1
            if col >= columnas_por_fila:
                col = 0
                row += 1

    def crear_tarjeta(self, id_d, nombre, desc, act, costo, row, col):
        # El contenedor de la tarjeta
        card = tb.Labelframe(self.scrollable_content, text=nombre, padding=15, bootstyle="info")
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        # Contenido de la tarjeta
        # Wraplength es importante para que el texto largo no ensanche la tarjeta infinitamente
        costo_l = f"${int(costo):,}".replace(",", ".")
        tb.Label(card, text=f"Costo: ${costo_l}", font=("Helvetica", 12, "bold"), bootstyle="success").pack(anchor="w",
                                                                                                            pady=(0, 5))

        lbl_desc = tb.Label(card, text=desc, font=("Helvetica", 10), wraplength=200)
        lbl_desc.pack(anchor="w", fill=X)

        tb.Label(card, text=f"{act}", font=("Helvetica", 9), bootstyle="secondary").pack(anchor="w", pady=(10, 0))

        tb.Separator(card, orient="horizontal").pack(fill=X, pady=10)

        # Botones de Acción
        btn_frame = tb.Frame(card)
        btn_frame.pack(fill=X)

        # IMPORTANTE: Usamos lambda i=id_d: ... para capturar el ID específico de esta vuelta del bucle
        btn_edit = tb.Button(btn_frame, text="✏", bootstyle="warning-outline", width=4,
                             command=lambda i=id_d: self.abrir_formulario_editar(i))
        btn_edit.pack(side=LEFT, padx=(0, 5))

        btn_del = tb.Button(btn_frame, text="🗑", bootstyle="danger-outline", width=4,
                            command=lambda i=id_d: self.eliminar_destino(i))
        btn_del.pack(side=RIGHT)

    # --- MÉTODOS DE LÓGICA (MODIFICADOS PARA RECIBIR ID DIRECTAMENTE) ---

    def abrir_formulario_crear(self):
        DestinosForm(self, callback=self.cargar_datos_destinos)

    def abrir_formulario_editar(self, id_destino):
        # Ya no buscamos en el treeview, recibimos el ID directamente del botón
        DestinosForm(self, id_destino=id_destino, callback=self.cargar_datos_destinos)

    def eliminar_destino(self, id_destino):
        # Ya no buscamos en el treeview, recibimos el ID directamente del botón
        respuesta = messagebox.askyesno("Confirmar Eliminación",
                                        f"¿Estás seguro de que deseas eliminar el destino ID {id_destino}?")
        if respuesta:
            eliminar_destino(id_destino)
            # Usamos un toast (notificación flotante) si tienes la versión nueva de tb, sino messagebox
            messagebox.showinfo("Eliminado", "Destino eliminado correctamente.")
            self.cargar_datos_destinos()