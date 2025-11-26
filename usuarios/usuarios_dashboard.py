import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from cruds.cruds_reservas import obtener_reservas_por_usuario, eliminar_reserva, insertar_reserva, cancelar_reserva
from cruds.cruds_paquetes import ver_paquetes

class UsuarioDashboard(tb.Frame): 
    def __init__(self, parent, usuario_data):
        super().__init__(parent)
        self.usuario_data = usuario_data
        self.pack(fill="both", expand=True)

        #Configuración ventana padre
        parent.title(f"Viajes Aventura - Panel de Cliente: {self.usuario_data.get('nombre', 'Usuario')}")
        parent.geometry("1200x700") 
        parent.resizable(True, True)

        #--- HEADER ---
        header_frame = tb.Frame(self, bootstyle="primary", height=80)
        header_frame.pack(fill="x")
        
        tb.Label(header_frame, text="Viajes Aventura", font=("Helvetica", 24, "bold"), bootstyle="inverse-primary").pack(side="left", padx=20, pady=20)
        
        nombre_corto = self.usuario_data.get('nombre', 'Usuario').split(' ')[0]
        tb.Label(header_frame, text=f"Hola, {nombre_corto}", font=("Helvetica", 12), bootstyle="inverse-primary").pack(side="right", padx=20)

        #--- CONTENEDOR PRINCIPAL ---
        main_body = tb.Frame(self)
        main_body.pack(fill="both", expand=True, padx=10, pady=10)

        #--- SIDEBAR (IZQUIERDA) ---
        self.sidebar = tb.Frame(main_body, bootstyle="light", width=300)
        self.sidebar.pack(side="left", fill="y", padx=(0, 10)) 
        self.crear_sidebar_perfil()

        #--- PESTAÑAS (DERECHA) ---
        self.notebook = tb.Notebook(main_body, bootstyle="primary")
        self.notebook.pack(side="left", fill="both", expand=True)

        #Pestaña 1: Catálogo
        self.tab_reservar = tb.Frame(self.notebook)
        self.notebook.add(self.tab_reservar, text='Explorar Destinos ')
        self.crear_tab_catalogo() 

        #Pestaña 2: Mis Reservas
        self.tab_mis_reservas = tb.Frame(self.notebook)
        self.notebook.add(self.tab_mis_reservas, text='Mis Reservas ')
        self.crear_tab_mis_reservas()


    def crear_area_con_scroll(self, parent_frame):
        
        canvas = tk.Canvas(parent_frame, highlightthickness=0)
        
        #Scrollbar (La barra vertical)
        scrollbar = tb.Scrollbar(parent_frame, orient="vertical", command=canvas.yview)
        
        #Frame interno (Donde pondremos las tarjetas)
        scrollable_frame = tb.Frame(canvas)

        #Configura que el frame crezca dentro del canvas
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        #Crea la ventana dentro del canvas
        #Guarda el ID de la ventana para poder cambiar su ancho si se redimensiona
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        def configurar_ancho(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind("<Configure>", configurar_ancho)

        #Conectar scrollbar con canvas
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        #Activar Rueda del Mouse (Solo cuando el mouse está encima)
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        def _bound_to_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbound_to_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")

        scrollable_frame.bind('<Enter>', _bound_to_mousewheel)
        scrollable_frame.bind('<Leave>', _unbound_to_mousewheel)

        return scrollable_frame #Devuelve el frame interno para agregar contenido

    # BARRA LATERAL
    
    def crear_sidebar_perfil(self):
        info_frame = tb.Frame(self.sidebar, padding=15)
        info_frame.pack(fill="x")

        tb.Label(info_frame, text="👤", font=("Helvetica", 60)).pack(pady=(10, 5))
        
        nombre_completo = f"{self.usuario_data.get('nombre')} {self.usuario_data.get('apellido')}"
        tb.Label(info_frame, text=nombre_completo, font=("Helvetica", 14, "bold"), justify="center", wraplength=200).pack(pady=5)
        
        rol = self.usuario_data.get('rol', 'Cliente').capitalize()
        tb.Label(info_frame, text=rol, font=("Helvetica", 10), bootstyle="secondary").pack(pady=(0, 20))

        tb.Separator(info_frame, orient="horizontal").pack(fill="x", pady=10)

        self.crear_dato_sidebar(info_frame, "RUT:", self.usuario_data.get('rut'))
        self.crear_dato_sidebar(info_frame, "Correo:", self.usuario_data.get('correo'))
        self.crear_dato_sidebar(info_frame, "Teléfono:", self.usuario_data.get('telefono'))
        self.crear_dato_sidebar(info_frame, "Dirección:", self.usuario_data.get('direccion', 'No registrada'))

        tb.Separator(info_frame, orient="horizontal").pack(fill="x", pady=20)

        btn_salir = tb.Button(info_frame, text="CERRAR SESIÓN", bootstyle="danger", command=self.salir)
        btn_salir.pack(fill="x", pady=20) 

    def crear_dato_sidebar(self, parent, titulo, valor):
        container = tb.Frame(parent)
        container.pack(fill="x", pady=5)
        tb.Label(container, text=titulo, font=("Helvetica", 9, "bold"), bootstyle="secondary").pack(anchor="w")
        tb.Label(container, text=valor, font=("Helvetica", 10), wraplength=220).pack(anchor="w")

    def salir(self):
        if messagebox.askyesno("Salir", "¿Deseas cerrar sesión?"):
            self.master.destroy()

    # VISTA 1: CATÁLOGO

    def crear_tab_catalogo(self):
        #Barra superior
        top_bar = tb.Frame(self.tab_reservar)
        top_bar.pack(fill="x", padx=20, pady=15)
        tb.Label(top_bar, text="¡Encuentra tu próxima aventura!", font=("Helvetica", 18)).pack(side="left")
        
        btn_refresh = tb.Button(top_bar, text="Refrescar Catálogo", bootstyle="outline-primary", command=self.cargar_catalogo_visual)
        btn_refresh.pack(side="right")

        #Contenedor para scroll (Frame intermedio)
        container_scroll = tb.Frame(self.tab_reservar)
        container_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        #CREA ÁREA DE SCROLL MANUAL
        self.frame_catalogo_contenido = self.crear_area_con_scroll(container_scroll)

        #Cargar Datos
        self.cargar_catalogo_visual()

    def cargar_catalogo_visual(self):
        #Limpiar
        for widget in self.frame_catalogo_contenido.winfo_children():
            widget.destroy()

        lista_paquetes = ver_paquetes() 
        
        if not lista_paquetes:
            tb.Label(self.frame_catalogo_contenido, text="No hay paquetes turísticos disponibles.", font=("Helvetica", 14)).pack(pady=50)
            return

        columnas_por_fila = 2
        col = 0
        row = 0

        #Configurar columnas del GRID interno
        self.frame_catalogo_contenido.columnconfigure(0, weight=1)
        self.frame_catalogo_contenido.columnconfigure(1, weight=1)

        for pkg in lista_paquetes:
            self.crear_tarjeta_paquete(self.frame_catalogo_contenido, pkg[0], pkg[1], pkg[2], pkg[3], pkg[4], pkg[5], row, col)
            col += 1
            if col >= columnas_por_fila:
                col = 0
                row += 1

    def crear_tarjeta_paquete(self, parent, p_id, nombre, f_inicio, f_fin, precio, cupos, row, col):
        card = tb.Labelframe(parent, text=f" Cupos: {cupos} ", bootstyle="info", padding=15)
        card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
        
        tb.Label(card, text=nombre, font=("Helvetica", 14, "bold"), wraplength=250).pack(anchor="w", pady=(0, 10))
        tb.Label(card, text="Fechas del viaje:", font=("Helvetica", 10, "bold"), bootstyle="secondary").pack(anchor="w")
        tb.Label(card, text=f"Del {f_inicio} al {f_fin}", font=("Helvetica", 10)).pack(anchor="w", pady=(0, 10))

        precio_fmt = f"${int(precio):,}".replace(",", ".")
        lbl_precio = tb.Label(card, text=precio_fmt, font=("Helvetica", 16, "bold"), bootstyle="success")
        lbl_precio.pack(anchor="e", pady=(0, 15))

        tb.Separator(card, orient="horizontal").pack(fill="x", pady=5)
        
        frame_accion = tb.Frame(card)
        frame_accion.pack(fill="x", pady=5)

        tb.Label(frame_accion, text="Confirmar fecha:", font=("Helvetica", 9)).pack(side="left")
        entry_fecha = tb.Entry(frame_accion, width=12)
        entry_fecha.pack(side="left", padx=5)
        entry_fecha.insert(0, str(f_inicio)) 

        btn = tb.Button(
            card, 
            text="Reservar Ahora", 
            bootstyle="success-outline", 
            width=20,
            command=lambda: self.accion_reservar_tarjeta(p_id, entry_fecha.get())
        )
        btn.pack(pady=10, fill="x")

    def accion_reservar_tarjeta(self, id_paquete, fecha_viaje):
        if not fecha_viaje:
            messagebox.showwarning("Falta fecha", "Por favor confirma la fecha de viaje.")
            return

        id_usuario = self.usuario_data.get('id_usuario')

        if not messagebox.askyesno("Confirmar Reserva", f"¿Deseas reservar este paquete para el {fecha_viaje}?"):
            return

        if insertar_reserva(fecha_viaje, id_usuario, id_paquete, "Pendiente"):
            messagebox.showinfo("¡Felicidades!", "Tu reserva ha sido creada exitosamente.")
            self.cargar_mis_reservas_visual() 
            self.notebook.select(self.tab_mis_reservas) 
        else:
            messagebox.showerror("Error", "Hubo un problema al guardar la reserva.")

    # VISTA 2: MIS RESERVAS

    def crear_tab_mis_reservas(self):
        #Barra superior
        top_bar = tb.Frame(self.tab_mis_reservas)
        top_bar.pack(fill="x", padx=20, pady=15)
        
        tb.Label(top_bar, text="Gestiona tus viajes programados", font=("Helvetica", 18)).pack(side="left")
        
        btn_refresh = tb.Button(top_bar, text="Actualizar Estado", bootstyle="link", command=self.cargar_mis_reservas_visual)
        btn_refresh.pack(side="right")

        #Contenedor para scroll
        container_scroll = tb.Frame(self.tab_mis_reservas)
        container_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        #CREA ÁREA DE SCROLL MANUAL
        self.frame_reservas_contenido = self.crear_area_con_scroll(container_scroll)

        self.cargar_mis_reservas_visual()

    def cargar_mis_reservas_visual(self):
        for widget in self.frame_reservas_contenido.winfo_children():
            widget.destroy()

        try:
            id_u = self.usuario_data.get('id_usuario')
            reservas = obtener_reservas_por_usuario(id_u)

            if not reservas:
                tb.Label(self.frame_reservas_contenido, text="No tienes reservas activas.", font=("Helvetica", 14), bootstyle="secondary").pack(pady=50)
                return

            col = 0
            row = 0
            self.frame_reservas_contenido.columnconfigure(0, weight=1)

            for r in reservas:
                if isinstance(r, dict):
                    v_id, v_paquete = r.get('id_reserva'), r.get('nombre_paquete')
                    v_fecha, v_estado = r.get('fecha'), r.get('estado')
                else:
                    v_id, v_fecha, v_paquete, v_estado = r[0], r[1], r[2], r[3]

                self.crear_tarjeta_reserva_individual(self.frame_reservas_contenido, v_id, v_paquete, v_fecha, v_estado, row, col)
                row += 1

        except Exception as e:
            print(f"Error cargando reservas: {e}")
            tb.Label(self.frame_reservas_contenido, text=f"Error de conexión: {e}", bootstyle="danger").pack()

    def crear_tarjeta_reserva_individual(self, parent, r_id, paquete, fecha, estado, row, col):
        color_estado = "secondary"
        if estado == "Pendiente": color_estado = "warning"
        elif estado == "Confirmada": color_estado = "success"
        elif estado == "Cancelada": color_estado = "secondary"

        card = tb.Labelframe(parent, text=f" Reserva #{r_id} ", bootstyle=color_estado, padding=15)
        card.grid(row=row, column=col, padx=15, pady=10, sticky="ew") 
        
        tb.Label(card, text=paquete, font=("Helvetica", 12, "bold")).pack(anchor="w", pady=(0, 5))
        tb.Label(card, text=f"Fecha: {fecha}", font=("Helvetica", 10)).pack(anchor="w")
        
        tb.Label(card, text=f" {estado} ", bootstyle=f"{color_estado}-inverse", font=("Helvetica", 9, "bold")).pack(anchor="e", pady=(5, 10))

        if estado != "Cancelada":
            tb.Separator(card, orient="horizontal").pack(fill="x", pady=5)
            
            btn_frame = tb.Frame(card)
            btn_frame.pack(fill="x", pady=10)
            
            btn_cancel = tb.Button(
                btn_frame, 
                text="Cancelar Viaje", 
                bootstyle="danger", 
                width=20, 
                command=lambda i=r_id: self.accion_cancelar(i) 
            )
            btn_cancel.pack()

    def accion_cancelar(self, id_reserva):
        if messagebox.askyesno("Confirmar Cancelación", f"¿Estás seguro de que deseas cancelar la reserva #{id_reserva}?"):
            if cancelar_reserva(id_reserva):
                messagebox.showinfo("Cancelado", "Tu reserva ha sido cancelada exitosamente.")
                self.cargar_mis_reservas_visual() 
            else:
                messagebox.showerror("Error", "No se pudo cancelar la reserva.")