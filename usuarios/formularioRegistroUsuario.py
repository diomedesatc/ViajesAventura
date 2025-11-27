import tkinter as tk
from tkinter import ttk, messagebox
from clases.Usuarios import Usuarios
from validaciones.validar import validar_rut, validar_email


class UsuarioForm(tk.Toplevel):
    #Este es el formulario para crear un usuario en el sistema!

    def __init__(self, master, callback=None):
        super().__init__(master)
        self.entries = None
        self.master = master
        self.callback = callback

        self.title_text = "Crear Nuevo Usuario"
        self.title(self.title_text)
        self.geometry("650x600")
        self.transient(master)
        self.grab_set()
        self.resizable(False, False)

        # Estilo para la ventana Toplevel
        style = ttk.Style()
        style.configure('TLabel', font=('Helvetica', 10))
        style.configure('TEntry', font=('Helvetica', 10))
        style.configure('TButton', font=('Helvetica', 10, 'bold'))
        style.configure('Accent.TButton', background='#48BB78', foreground='white')
        style.map('Accent.TButton', background=[('active', '#38A169')])

        self.crear_widgets()

    def crear_widgets(self):
        main_frame = ttk.Frame(self, padding="30")  # Más padding
        main_frame.pack(fill='both', expand=True)

        ttk.Label(main_frame, text=self.title_text, font=("Helvetica", 16, "bold"),
                  foreground='#2D3748').grid(row=0, column=0, columnspan=2, pady=(0, 25), sticky="w")

        # Configuración de la cuadrícula
        main_frame.grid_columnconfigure(0, weight=0)  # Etiqueta fija
        main_frame.grid_columnconfigure(1, weight=1)  # Entrada expandible


        # Campos de texto y entrada
        campos = [
            ("Nombre:", "nombre"),
            ("Apellido:", "apellido"),
            ("Dirección:", "direccion"),
            ("Teléfono:", "telefono"),
            ("Correo:", "correo"),
            ("Contraseña:", "contrasena"),
            ("Rut: (Ej: 11111111-1)", "rut")
            ]

        self.entries = {}
        row_num = 1
        for label_text, key in campos:

            ttk.Label(main_frame, text=label_text, width=30).grid(row=row_num, column=0, sticky="w", pady=7)  # Más pady

            entry = ttk.Entry(main_frame, width=50)  # Mayor ancho
            entry.grid(row=row_num, column=1, sticky="ew", pady=7)
            self.entries[key] = entry

            if key == "contrasena":
                entry.config(show="*")

            row_num += 1

        btn_guardar = ttk.Button(main_frame, text="Registrarse",
                                 command=self.crear_usuario, style='Accent.TButton')
        btn_guardar.grid(row=row_num, column=0, columnspan=2, pady=30, sticky="n")

    def crear_usuario(self):
        #Validar y crear usuario
        data = {key: entry.get() for key, entry in self.entries.items()}


        try:
            # Requisito: Validación de Entradas Seguras
            if not all([data['nombre'], data['correo'], data['contrasena']]):
                messagebox.showerror("Error de Validación",
                                     "Los campos Nombre, Emaily Contraseña son obligatorios.")
                return

            #Validar el rut y correo
            es_rut_valido = validar_rut(data['rut'])
            es_correo_valido = validar_email(data['correo'])

            if es_correo_valido and es_rut_valido:

                #Insertar usuario
                nuevo_usuario = Usuarios(data['nombre'], data['apellido'],data['direccion'],data['telefono'],data['correo'],data['contrasena'],data['rut'], "usuario")
                nuevo_usuario.insertar_usuario()
                messagebox.showinfo("Correcto!", "Usuario registrado correctamente.")
                self.destroy()


        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")


        if self.callback:
            self.callback()  # Refresca el listado en el Dashboard
