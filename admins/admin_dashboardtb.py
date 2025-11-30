import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *

# IMPORTAR TUS VISTAS DE GESTIÓN (Asegúrate de tener estos archivos o crea placeholders)
from admins.destinos.destinos_frame import DestinosFrame
from admins.paquetes.paquetes_frame import PaquetesFrame
from admins.reservas.reservas_frame import ReservasFrame


# from admins.paquetes.paquetes_frame import PaquetesFrame
# from admins.usuarios.usuarios_frame import UsuariosFrame

class AdminDashboard_(tb.Frame):
    def __init__(self, parent, usuario_data):
        super().__init__(parent)
        self.usuario_data = usuario_data
        self.pack(fill="both", expand=True)

        # --- 1. CONFIGURACIÓN VENTANA PADRE ---
        parent.title(f"Viajes Aventura - Administración: {self.usuario_data.get('nombre', 'Admin')}")
        parent.geometry("1200x700")
        parent.resizable(True, True)

        # --- 2. HEADER (Igual que UsuarioDashboard pero con otro color si gustas) ---
        # Usamos bootstyle="dark" para diferenciar que es zona Admin
        header_frame = tb.Frame(self, bootstyle="dark", height=80)
        header_frame.pack(fill="x")

        # Logo / Título
        tb.Label(header_frame, text="Viajes Aventura | ADMIN", font=("Helvetica", 24, "bold"),
                 bootstyle="inverse-dark").pack(side="left", padx=20, pady=20)

        # Saludo derecha
        nombre_corto = self.usuario_data.get('nombre', 'Admin').split(' ')[0]
        tb.Label(header_frame, text=f"Admin: {nombre_corto}", font=("Helvetica", 12), bootstyle="inverse-dark").pack(
            side="right", padx=20)

        # --- 3. CONTENEDOR PRINCIPAL (Cuerpo) ---
        main_body = tb.Frame(self)
        main_body.pack(fill="both", expand=True, padx=10, pady=10)

        # --- 4. SIDEBAR (IZQUIERDA - Datos del Admin) ---
        self.sidebar = tb.Frame(main_body, bootstyle="light", width=280)
        self.sidebar.pack(side="left", fill="y", padx=(0, 10))
        self.crear_sidebar_perfil()

        # --- 5. PESTAÑAS (DERECHA - Módulos de Gestión) ---
        # Usamos bootstyle="dark" para las pestañas activas
        self.notebook = tb.Notebook(main_body, bootstyle="dark")
        self.notebook.pack(side="left", fill="both", expand=True)

        # --- CREACIÓN DE TABS (Módulos) ---

        # Pestaña 1: Destinos (Aquí incrustamos tu DestinosFrame anterior)
        self.tab_destinos = tb.Frame(self.notebook)
        self.notebook.add(self.tab_destinos, text='Destinos ')
        self.cargar_modulo_destinos()

        # Pestaña 2: Paquetes
        self.tab_paquetes = tb.Frame(self.notebook)
        self.notebook.add(self.tab_paquetes, text='Paquetes ')
        self.cargar_modulo_paquetes()  # Placeholder

        # Pestaña 3: Usuarios
        self.tab_usuarios = tb.Frame(self.notebook)
        self.notebook.add(self.tab_usuarios, text='Usuarios ')
        # self.cargar_modulo_usuarios()

        # Pestaña 4: Reservas Globales
        self.tab_reservas = tb.Frame(self.notebook)
        self.notebook.add(self.tab_reservas, text='Reservas ')
        self.cargar_modulo_reservas()

    # ----------------------------------------------------------------
    # MÉTODOS DE LA SIDEBAR (Idénticos a UsuarioDashboard)
    # ----------------------------------------------------------------
    def crear_sidebar_perfil(self):
        info_frame = tb.Frame(self.sidebar, padding=15)
        info_frame.pack(fill="x")

        # Icono diferente para Admin (ej. user-tie si tuvieras iconos, o un emoji)
        tb.Label(info_frame, text="👨‍💼", font=("Helvetica", 60)).pack(pady=(10, 5))

        nombre_completo = f"{self.usuario_data.get('nombre', '')} {self.usuario_data.get('apellido', '')}"
        tb.Label(info_frame, text=nombre_completo, font=("Helvetica", 14, "bold"), justify="center",
                 wraplength=200).pack(pady=5)

        # Etiqueta de ROL
        tb.Label(info_frame, text="ADMINISTRADOR", font=("Helvetica", 10, "bold"), bootstyle="danger").pack(
            pady=(0, 20))

        tb.Separator(info_frame, orient="horizontal").pack(fill="x", pady=10)

        self.crear_dato_sidebar(info_frame, "ID Admin:", str(self.usuario_data.get('id_usuario', 'N/A')))
        self.crear_dato_sidebar(info_frame, "Correo:", self.usuario_data.get('correo', 'N/A'))

        tb.Separator(info_frame, orient="horizontal").pack(fill="x", pady=20)

        # Botón Salir
        btn_salir = tb.Button(info_frame, text="CERRAR SESIÓN", bootstyle="outline-danger", command=self.salir)
        btn_salir.pack(fill="x", pady=20)

    def crear_dato_sidebar(self, parent, titulo, valor):
        container = tb.Frame(parent)
        container.pack(fill="x", pady=5)
        tb.Label(container, text=titulo, font=("Helvetica", 9, "bold"), bootstyle="secondary").pack(anchor="w")
        tb.Label(container, text=valor, font=("Helvetica", 10), wraplength=220).pack(anchor="w")

    def salir(self):
        if messagebox.askyesno("Salir", "¿Deseas cerrar sesión?"):
            self.master.destroy()
            # Aquí podrías llamar a una función para volver al Login si tienes un MainController

    # ----------------------------------------------------------------
    # MÉTODOS PARA CARGAR LOS MÓDULOS (FRAMES)
    # ----------------------------------------------------------------

    def cargar_modulo_destinos(self):
        """
        Aquí instanciamos el DestinosFrame que creamos anteriormente.
        Le pasamos 'self.tab_destinos' como padre para que se dibuje dentro de la pestaña.
        """
        # Limpiar por si acaso
        for widget in self.tab_destinos.winfo_children():
            widget.destroy()

        # Instanciar el frame.
        # NOTA: Pasamos 'self' como controller si DestinosFrame necesita acceder al usuario_data o métodos del dashboard
        frame = DestinosFrame(self.tab_destinos, controller=self)
        frame.pack(fill="both", expand=True)

    def cargar_modulo_paquetes(self):
        frame = PaquetesFrame(self.tab_paquetes, controller=self)
        frame.pack(fill="both", expand=True)
    def cargar_modulo_reservas(self):
        frame = ReservasFrame(self.tab_reservas, controller=self)
        frame.pack(fill="both", expand=True)