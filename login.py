from tkinter import messagebox
import ttkbootstrap as tb
from usuarios.formularioRegistroUsuario import UsuarioForm
from cruds.cruds_usuarios import buscar_usuario, validar_contrasena
from usuarios.usuarios_dashboard import UsuarioDashboard
from admins.admin_dashboardtb import AdminDashboard_

# --- CONFIGURACIÓN GENERAL ---
APP_TITLE = "Viajes Aventura - Sistema de Gestión"
THEME_NAME = "sandstone"  # Opciones: yeti, flatly, sandstone, united
LOGIN_SIZE = "450x450"
MAIN_SIZE = "1200x700"

class LoginWindow(tb.Toplevel):
    """Ventana emergente para el inicio de sesión"""

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configurar_ventana()
        self.inicializar_ui()

    def configurar_ventana(self):
        """Configuraciones de geometría y título"""
        self.title("Inicio de Sesión")
        self.geometry(LOGIN_SIZE)
        self.resizable(False, False)
        # Si cierran el login, cerramos toda la app
        self.protocol("WM_DELETE_WINDOW", self.master.on_closing)

    def inicializar_ui(self):
        """Método maestro que orquesta la creación de la interfaz"""
        self.main_frame = tb.Frame(self, padding=30)
        self.main_frame.pack(expand=True, fill='both')

        self._crear_encabezado()
        self._crear_formulario()
        self._crear_botones()

    # --- SECCIÓN VISUAL (WIDGETS) ---

    def _crear_encabezado(self):
        lbl_titulo = tb.Label(
            self.main_frame, 
            text="Viajes Aventura", 
            font=("Helvetica", 22, "bold"), 
            bootstyle="primary"
        )
        lbl_titulo.pack(pady=(10, 30))

    def _crear_formulario(self):
        # Campo Correo
        tb.Label(self.main_frame, text="Correo Electrónico:", font=("Helvetica", 10)).pack(fill='x', pady=5)
        self.user_entry = tb.Entry(self.main_frame)
        self.user_entry.pack(fill='x', pady=5)
        self.user_entry.focus() # Poner el cursor aquí automáticamente

        # Campo Contraseña
        tb.Label(self.main_frame, text="Contraseña:", font=("Helvetica", 10)).pack(fill='x', pady=5)
        self.pass_entry = tb.Entry(self.main_frame, show="*")
        self.pass_entry.pack(fill='x', pady=5)

        # Permitir login presionando la tecla Enter
        self.pass_entry.bind('<Return>', lambda event: self.accion_login())

    def _crear_botones(self):
        btn_frame = tb.Frame(self.main_frame)
        btn_frame.pack(pady=30, fill='x')

        btn_login = tb.Button(
            btn_frame, 
            text="Iniciar Sesión", 
            bootstyle="success", 
            command=self.accion_login, 
            width=15
        )
        btn_login.pack(side="left", padx=5, expand=True)

        btn_registro = tb.Button(
            btn_frame, 
            text="Crear Cuenta", 
            bootstyle="outline-primary", 
            command=self.accion_registro, 
            width=15
        )
        btn_registro.pack(side="right", padx=5, expand=True)

    # --- LÓGICA DE NEGOCIO ---

    def accion_login(self):
        correo = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()

        if not correo or not password:
            messagebox.showwarning("Atención", "Por favor ingresa ambos campos.")
            return

        try:
            usuario = buscar_usuario(correo) # Retorna tupla o None

            if usuario is None:
                messagebox.showerror("Error", "El correo no está registrado.")
                return

            #Indices en BD
            # 0:id, 1:nombre, 2:apellido, 3:direc, 4:tel, 5:mail, 6:pass_hash, 7:rut, 8:rol
            contrasena_almacenada = usuario[6]
            rol_usuario = usuario[8]

            if validar_contrasena(password, contrasena_almacenada):
                datos_usuario = {
                    'id_usuario': usuario[0],
                    'nombre': usuario[1],
                    'apellido': usuario[2],
                    'direccion': usuario[3],
                    'telefono': usuario[4],
                    'correo': usuario[5],
                    'rut': usuario[7],
                    'rol': rol_usuario
                }
                
                self.destroy()
                self.master.mostrar_ventana_principal(datos_usuario)
            else:
                messagebox.showerror("Error", "Contraseña incorrecta.")

        except Exception as e:
            print(f"Error en login: {e}")
            messagebox.showerror("Error del Sistema", f"Ocurrió un error inesperado: {e}")

    def accion_registro(self):
        UsuarioForm(self)


# =============================
# CLASE PRINCIPAL (CONTROLADOR)
# =============================
class AppGestionEmpresarial(tb.Window):
    
    def __init__(self):
        super().__init__(themename=THEME_NAME)
        self.configurar_app()
        self.current_window = None
        
        # Iniciar flujo mostrando el Login
        self.mostrar_login()

    def configurar_app(self):
        self.title(APP_TITLE)
        self.geometry(MAIN_SIZE)
        self.withdraw() # Ocultar ventana raíz al inicio

    def mostrar_login(self):
        self.login_window = LoginWindow(self)

    def mostrar_ventana_principal(self, datos_usuario):
        """Router: Decide qué Dashboard mostrar según el rol"""
        self.deiconify() # Mostrar ventana raíz
        
        # Limpiar ventana anterior si existe
        if self.current_window:
            self.current_window.destroy()

        rol = datos_usuario.get('rol')
        nombre = datos_usuario.get('nombre')

        # Lógica de enrutamiento
        if rol in ["admin", "superadmin"]:
            self.current_window = AdminDashboard_(self, usuario_data=datos_usuario)
        
        elif rol in ["usuario", "cliente"]:
            self.current_window = UsuarioDashboard(self, usuario_data=datos_usuario)
        
        else:
            messagebox.showerror("Acceso Denegado", "Tu rol no tiene permisos para acceder.")
            self.destroy()
            return

        self.title(f"{APP_TITLE} - {nombre}")

    def on_closing(self):
        self.destroy()

if __name__ == "__main__":
    app = AppGestionEmpresarial()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()