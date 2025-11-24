import tkinter as tk
from tkinter import ttk, messagebox
from usuarios.formularioRegistroUsuario import UsuarioForm
from cruds.cruds_usuarios import buscar_usuario, validar_contrasena, hashear_contrasena
from admins.admin_dashboard import AdminDashboard
from usuarios.usuarios_dashboard import UsuarioDashboard

class LoginWindow(tk.Toplevel):

    def __init__(self, master):
        super().__init__(master)
        self.pass_entry = None
        self.user_entry = None
        self.master = master
        self.title("Inicio de Sesión")
        self.geometry("400x250")
        self.resizable(False, False)
        self.id_usuario = None

        style = ttk.Style()
        style.configure('TLabel', font=('Helvetica', 10))
        style.configure('TEntry', font=('Helvetica', 10))

        self.crear_widgets()

    def crear_widgets(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill='both')

        # Título
        lbl_titulo = ttk.Label(main_frame, text="Viajes Aventura - Login", font=("Helvetica", 16, "bold"),
                               foreground='#48BB78')
        lbl_titulo.grid(row=0, column=0, columnspan=2, pady=15)

        # Usuario
        ttk.Label(main_frame, text="Correo:").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.user_entry = ttk.Entry(main_frame, width=35)
        self.user_entry.grid(row=1, column=1, pady=5)

        # Contraseña
        ttk.Label(main_frame, text="Contraseña:").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        self.pass_entry = ttk.Entry(main_frame, width=35, show="*")
        self.pass_entry.grid(row=2, column=1, pady=5)

        # Botón de Login
        btn_login = ttk.Button(main_frame, text="Iniciar Sesión", command=self.handle_login,
                               style='Accent.TButton')  # Estilo de botón principal
        btn_login.grid(row=3, column=1, pady=20)

        btn_login = ttk.Button(main_frame, text="Registrarse", command=self.handle_register,
                               style='Accent.TButton')  # E
        # stilo de botón principal
        btn_login.grid(row=3, column=2, pady=20)

        # Configuraciones para centrar
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Añadir un tema para el botón principal
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Accent.TButton', background='#48BB78', foreground='white', font=('Helvetica', 10, 'bold'))
        style.map('Accent.TButton', background=[('active', '#38A169')])

    def  handle_login(self):
        correo = self.user_entry.get()
        password = self.pass_entry.get()

        try:
            usuario = buscar_usuario(correo)
            if usuario == None:
                messagebox.showerror("Error de usuario", "El correo ingresado no es valido.")
                return
            else:
                contrasena_almacenada = usuario[6]

                respuesta = validar_contrasena(password, contrasena_almacenada)
                rol = usuario[8]
                if respuesta:
                    messagebox.showinfo("Exito", f"Bienvenido {usuario[1]}")
                    self.destroy()
                    self.master.mostrar_ventana_principal(rol, usuario[1], usuario[0])
                else:
                    messagebox.showinfo("Error", "Contraseña incorrecta.")

        except Exception as e:
            messagebox.showerror("Error de usuario", "El correo ingresado no es valido.")

    def handle_register(self):
        #Formulario para registrarse en el sistema
        UsuarioForm(self)



class AppGestionEmpresarial(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Viajes Aventura")
        self.geometry("1200x700")

        self.withdraw()  # Oculta la ventana principal hasta que el login sea exitoso
        self.current_window = None

        # Iniciar el flujo con la ventana de Login
        self.login_window = LoginWindow(self)

    def mostrar_ventana_principal(self, rol: str, nombre: str, id_usuario: int):
        self.deiconify()

        if self.current_window:
            self.current_window.destroy()

        if rol == "admin" or rol == "superadmin":
            self.title(f"Viajes Aventura - ({nombre})")
            self.current_window = AdminDashboard(self, empleado_id= id_usuario )
        elif rol == "usuario":
            # Vista de Empleado (pendiente de desarrollo)
            self.current_window = UsuarioDashboard(self, empleado_id=id_usuario)
            self.title(f"Viajes Aventura - ({nombre})")

    def on_closing(self):
        self.destroy()



if __name__ == "__main__":
    app = AppGestionEmpresarial()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()

