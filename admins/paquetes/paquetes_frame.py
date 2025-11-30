import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from cruds.cruds_paquetes import ver_paquetes, eliminar_paquete, obtener_destinos_de_paquete
from .paquetesForm import PaquetesForm


class PaquetesFrame(tb.Frame):
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
        tb.Label(header_frame, text="Gestión de Paquetes",
                 font=("Helvetica", 18, "bold"),
                 bootstyle="primary").pack(side=LEFT)

        # Botón Agregar (Arriba a la derecha)
        tb.Button(header_frame, text="Nuevo Paquete", bootstyle="success",
                  command=self.abrir_formulario_crear).pack(side=RIGHT)

        # --- ÁREA DE SCROLL ---
        self.crear_area_scroll()

        # Cargar datos
        self.cargar_datos_paquetes()

    def crear_area_scroll(self):
        # 1. Canvas
        canvas = tk.Canvas(self, highlightthickness=0)

        # 2. Scrollbar
        scrollbar = tb.Scrollbar(self, orient="vertical", command=canvas.yview, bootstyle="round")

        # 3. Frame interno
        self.scrollable_content = tb.Frame(canvas)

        # Configuración para que el scroll se ajuste al contenido
        self.scrollable_content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Crear ventana en el canvas
        canvas_window = canvas.create_window((0, 0), window=self.scrollable_content, anchor="nw")

        # Ajuste de ancho responsivo
        def configurar_ancho(event):
            canvas.itemconfig(canvas_window, width=event.width)

        canvas.bind("<Configure>", configurar_ancho)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Layout
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Scroll con rueda del mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.scrollable_content.bind('<Enter>', lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        self.scrollable_content.bind('<Leave>', lambda e: canvas.unbind_all("<MouseWheel>"))

    def cargar_datos_paquetes(self):
        # Limpiar tarjetas anteriores
        for widget in self.scrollable_content.winfo_children():
            widget.destroy()

        datos_paquetes = ver_paquetes()

        if not datos_paquetes:
            tb.Label(self.scrollable_content, text="No hay paquetes registrados.", font=("Helvetica", 12)).pack(pady=20)
            return

        # Configuración de Grid (3 columnas)
        columnas_por_fila = 3
        col = 0
        row = 0

        for i in range(columnas_por_fila):
            self.scrollable_content.columnconfigure(i, weight=1)

        for paquete in datos_paquetes:
            # Asumiendo el orden: id, nombre, f_inicio, f_fin, precio, cupos
            # Ajusta esto si tu consulta SQL devuelve más columnas o en otro orden
            p_id, p_nom, p_ini, p_fin, p_prec, p_cupos = paquete

            self.crear_tarjeta(p_id, p_nom, p_ini, p_fin, p_prec, p_cupos, row, col)

            col += 1
            if col >= columnas_por_fila:
                col = 0
                row += 1

    def crear_tarjeta(self, p_id, nombre, f_ini, f_fin, precio, cupos, row, col):
        # Tarjeta
        card = tb.Labelframe(self.scrollable_content, text=nombre, padding=15, bootstyle="info")
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        # --- Contenido de la Tarjeta ---

        # Precio destacado
        costo_l = f"${int(precio):,}".replace(",", ".")
        lbl_precio = tb.Label(card, text=f"{costo_l}", font=("Helvetica", 14, "bold"), bootstyle="success")
        lbl_precio.pack(anchor="w", pady=(0, 10))

        # Fechas
        tb.Label(card, text="Fechas del viaje:", font=("Helvetica", 9, "bold"), bootstyle="secondary").pack(
            anchor="w")
        tb.Label(card, text=f"Desde: {f_ini}", font=("Helvetica", 10)).pack(anchor="w")
        tb.Label(card, text=f"Hasta:  {f_fin}", font=("Helvetica", 10)).pack(anchor="w", pady=(0, 10))
        #Destinos
        lbl_destinos = tb.Label(card, text="Destinos:", font=("Helvetica", 9, "bold"), bootstyle="secondary")
        lbl_destinos.pack(anchor="w")

        destinos = obtener_destinos_de_paquete(p_id)
        for destino in destinos:
            tb.Label(card, text=f"{destino[1]}", font=("Helvetica", 10)).pack(anchor="w")

        # Cupos
        color_cupo = "danger" if int(cupos) < 5 else "primary"
        tb.Label(card, text=f"Cupos disponibles: {cupos}", font=("Helvetica", 10, "bold"), bootstyle=color_cupo).pack(
            anchor="w")

        tb.Separator(card, orient="horizontal").pack(fill=X, pady=10)

        # --- Botones de Acción ---
        btn_frame = tb.Frame(card)
        btn_frame.pack(fill=X)

        # Editar
        tb.Button(btn_frame, text="✏", bootstyle="warning-outline", width=4,
                  command=lambda i=p_id: self.abrir_formulario_editar(i)).pack(side=LEFT, padx=(0, 5))

        # Eliminar
        tb.Button(btn_frame, text="🗑", bootstyle="danger-outline", width=4,
                  command=lambda i=p_id: self.eliminar_paquete(i)).pack(side=RIGHT)

    # --- MÉTODOS LÓGICOS (CRUD) ---

    def abrir_formulario_crear(self):
        PaquetesForm(self, callback=self.cargar_datos_paquetes)

    def abrir_formulario_editar(self, id_paquete):
        # Recibimos el ID directamente del lambda de la tarjeta
        PaquetesForm(self, callback=self.cargar_datos_paquetes, id_paquete=id_paquete)

    def eliminar_paquete(self, id_paquete):
        respuesta = messagebox.askyesno("Confirmar Eliminación",
                                        f"¿Estás seguro de que deseas eliminar el paquete ID {id_paquete}?")
        if respuesta:
            eliminar_paquete(id_paquete)
            messagebox.showinfo("Eliminado", "Paquete eliminado correctamente.")
            self.cargar_datos_paquetes()