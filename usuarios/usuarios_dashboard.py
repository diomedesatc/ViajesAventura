import tkinter as tk
from tkinter import ttk, messagebox

class UsuarioDashboard(ttk.Frame):

    def __init__(self, master, db_manager=None, empleado_id = None):
        super().__init__(master)
        self.empleados_tree = None
        self.reporte_var = None
        self.content_frame = None
        self.empleado_id = empleado_id

        self.master = master
        self.db = db_manager
        self.pack(expand=True, fill='both')
        self.current_view = None

        self.configurar_estilo()
        self.crear_diseno()
        self.mostrar_vista("Gestionar Tiempos")  # Muestra la vista de gestión de usuarios como inicio

    def configurar_estilo(self):
        """Configura el tema y los estilos personalizados de la aplicación."""
        style = ttk.Style()
        style.theme_use('clam')  # Un tema más moderno que el default

        # Color primario de EcoTech Solutions (verde)
        PRIMARY_COLOR = '#48BB78'
        DARK_BG_COLOR = '#2D3748'
        LIGHT_BG_COLOR = '#EDF2F7'

        # Estilo general para el fondo del dashboard
        style.configure('Dashboard.TFrame', background=LIGHT_BG_COLOR)
        self.config(style='Dashboard.TFrame')

        # Estilos para el menú lateral
        style.configure('Menu.TFrame', background=DARK_BG_COLOR)
        style.configure('Menu.TButton',
                        font=('Helvetica', 11, 'bold'),
                        background=DARK_BG_COLOR,
                        foreground='white',
                        padding=[15, 10])  # Aumentamos el padding para un mejor target táctil
        style.map('Menu.TButton',
                  background=[('active', PRIMARY_COLOR), ('pressed', PRIMARY_COLOR)],
                  foreground=[('active', DARK_BG_COLOR)])  # Texto oscuro al estar activo

        # Estilo para botones de acción (CRUD)
        style.configure('Action.TButton',
                        font=('Helvetica', 10, 'bold'),
                        padding=8,
                        background=PRIMARY_COLOR,
                        foreground='white')
        style.map('Action.TButton', background=[('active', '#38A169')])  # Tono más oscuro al pasar el ratón

        # Estilo para Treeview (Mejor lectura)
        style.configure('Treeview.Heading', font=('Helvetica', 10, 'bold'), background=PRIMARY_COLOR,
                        foreground='white')
        style.configure('Treeview', font=('Helvetica', 10), rowheight=25)

    def crear_diseno(self):
        # 1. Menú Lateral
        menu_frame = ttk.Frame(self, width=220, style='Menu.TFrame')
        menu_frame.pack(side='left', fill='y', padx=0, pady=0)

        # Título del Menú
        ttk.Label(menu_frame, text="EcoTech SGE", font=("Helvetica", 18, "bold"),
                  foreground='#48BB78', background='#2D3748').pack(pady=(20, 10), fill='x', padx=10)

        botones = [
            ("⏱️ Registro de Tiempo", "Gestionar Tiempos"),
            ("📊 Consultas de indicadores", "Consultar Indicadores")
        ]

        btn_container = ttk.Frame(menu_frame, padding=5, style='Menu.TFrame')
        btn_container.pack(fill='both', expand=True)

        for texto, vista in botones:
            btn = ttk.Button(btn_container, text=texto, style='Menu.TButton',
                             command=lambda v=vista: self.mostrar_vista(v))
            btn.pack(fill='x', padx=5, pady=5)

        # 2. Área de Contenido Principal
        self.content_frame = ttk.Frame(self, padding="30", style='Dashboard.TFrame')
        self.content_frame.pack(side='right', fill='both', expand=True)

    def limpiar_contenido(self):
        """Elimina todos los widgets del área de contenido."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def mostrar_vista(self, vista: str):
        """Carga el widget correspondiente a la vista seleccionada."""
        self.limpiar_contenido()

        if vista == "Gestionar Usuarios":
            pass
            #self.current_view = GestionEmpleadosFrame(self.content_frame, self)

        elif vista == "Gestionar Departamentos":
            pass
            #self.current_view = GestionDepartamentosFrame(self.content_frame, self)

        elif vista == "Gestionar Proyectos":
            pass
            #self.current_view = GestionProyectosFrame(self.content_frame, self)

        elif vista == "Gestionar Tiempos":
            pass
            #self.current_view = GestionIngresosDeHorasTrabajadasFrame(self.content_frame, self, self.empleado_id)

        elif vista == "Generar Informes":
            pass
            #self.current_view = GeneracionDeInformes(self.content_frame, self, self.empleado_id)
        elif vista == "Ver Asignaciones":
            pass
            #self.current_view = VistaProyectosAsignacionesFrame(self.content_frame, self)

        elif vista == "Consultar Indicadores":
            pass
            #self.current_view =GestionConsultasIndicadoresFrame(self.content_frame, self, self.empleado_id)

    def mostrar_vista_con_args(self, vista: str, **kwargs):
        self.limpiar_contenido()
        self.current_view = None
        if vista == "Ver Asignaciones":
            pass
            #self.current_view = VistaProyectosAsignacionesFrame(self.content_frame, self, **kwargs)

