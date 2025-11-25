import tkinter as tk
from tkinter import ttk, messagebox
from cruds.cruds_paquetes import buscar_paquete, obtener_destinos_de_paquete
from cruds.cruds_destinos import ver_los_destinos
from clases.Paquetes import Paquetes
from tkcalendar import DateEntry
from datetime import datetime


class PaquetesForm(tk.Toplevel):
    def __init__(self, master, callback=None, id_paquete=None):
        super().__init__(master)
        self.master = master
        self.callback = callback
        self.id_paquete = id_paquete

        # Lista lógica donde guardaremos diccionarios: {'id': 1, 'nombre': 'Paris'}
        self.destinos_seleccionados_lista = []

        self.title_text = "Actualizar Paquete" if id_paquete else "Crear Nuevo Paquete"
        self.title(self.title_text)
        self.geometry("700x650")
        self.transient(master)
        self.grab_set()
        self.resizable(False, False)

        self.crear_widgets()

        if self.id_paquete:
            self.cargar_datos_simulados(self.id_paquete)

    def crear_widgets(self):
        # --- 1. DATOS GENERALES (Parte Superior) ---
        frame_datos = ttk.LabelFrame(self, text="Información General", padding="15")
        frame_datos.pack(fill='x', padx=10, pady=5)

        campos = [
            ("Nombre:", "nombre"),
            ("Fecha Inicio:", "fecha_inicio"),
            ("Fecha Fin:", "fecha_fin"),
            ("Precio:", "precio"),
            ("Capacidad:", "cupos_disponibles")  # Corregido nombre clave
        ]

        self.entries = {}
        row_num = 0

        # Usamos GRID dentro de este frame
        frame_datos.columnconfigure(1, weight=1)

        for label_text, key in campos:
            ttk.Label(frame_datos, text=label_text).grid(row=row_num, column=0, sticky="w", pady=5)
            if key in ["fecha_inicio", "fecha_fin"]:
                entry = DateEntry(frame_datos, width=12, background="darkblue", foreground="black",
                                  borderwidth=2, date_pattern='yyyy-mm-dd')
            else:
                entry = ttk.Entry(frame_datos)

            entry.grid(row=row_num, column=1, sticky="ew", pady=5, padx=5)
            self.entries[key] = entry
            row_num += 1

        # --- 2. SELECCIÓN DE DESTINOS (Parte Media) ---
        frame_destinos = ttk.LabelFrame(self, text="Gestionar Destinos del Paquete", padding="15")
        frame_destinos.pack(fill='both', expand=True, padx=10, pady=5)

        # Cargar destinos disponibles desde la BD
        todos_los_destinos = ver_los_destinos()
        nombres_combo = [f"{d[0]} - {d[1]}" for d in todos_los_destinos]

        # Frame interno para el buscador
        frame_buscador = ttk.Frame(frame_destinos)
        frame_buscador.pack(fill='x', pady=(0, 10))

        ttk.Label(frame_buscador, text="Seleccionar Destino:").pack(side='left')
        self.combo_destinos = ttk.Combobox(frame_buscador, values=nombres_combo, state="readonly", width=40)
        self.combo_destinos.pack(side='left', padx=5)

        ttk.Button(frame_buscador, text="⬇ Agregar a la lista",
                   command=self.agregar_destino_visual).pack(side='left')

        # Treeview de destinos agregados
        cols = ("id", "nombre")
        self.tree_destinos = ttk.Treeview(frame_destinos, columns=cols, show="headings", height=6)
        self.tree_destinos.heading("id", text="ID")
        self.tree_destinos.heading("nombre", text="Destino")
        self.tree_destinos.column("id", width=50, anchor="center")
        self.tree_destinos.column("nombre", width=300)

        self.tree_destinos.pack(fill='both', expand=True)

        # Botón para quitar destinos (Opcional pero útil)
        ttk.Button(frame_destinos, text="Quitar Seleccionado",
                   command=self.quitar_destino_visual).pack(anchor='e', pady=5)

        # --- 3. BOTÓN GUARDAR (Parte Inferior) ---
        btn_text = "Guardar Cambios" if self.id_paquete else "Crear Paquete"
        ttk.Button(self, text=btn_text, style='Accent.TButton',
                   command=self.guardar_paquete).pack(pady=15, fill='x', padx=20)

    def agregar_destino_visual(self):
        seleccion = self.combo_destinos.get()
        if not seleccion:
            return

        id_dest = int(seleccion.split(" - ")[0])
        nom_dest = seleccion.split(" - ")[1]

        # Verificar duplicados en nuestra lista lógica
        for d in self.destinos_seleccionados_lista:
            if d['id'] == id_dest:
                messagebox.showwarning("Atención", "Este destino ya está agregado.")
                return

        # Agregar a lista lógica
        self.destinos_seleccionados_lista.append({'id': id_dest, 'nombre': nom_dest})

        # Agregar a lista visual (Treeview)
        self.tree_destinos.insert('', 'end', values=(id_dest, nom_dest))

    def quitar_destino_visual(self):
        seleccion = self.tree_destinos.selection()
        if not seleccion:
            return

        item = self.tree_destinos.item(seleccion[0])
        id_a_borrar = item['values'][0]

        # Borrar del Treeview
        self.tree_destinos.delete(seleccion[0])

        # Borrar de la lista lógica
        self.destinos_seleccionados_lista = [d for d in self.destinos_seleccionados_lista if d['id'] != id_a_borrar]

    def guardar_paquete(self):
        # 1. Recoger datos del formulario
        data = {key: entry.get() for key, entry in self.entries.items()}

        # 2. Recoger IDs de los destinos
        lista_ids_destinos = [d['id'] for d in self.destinos_seleccionados_lista]

        # Validaciones
        if not all(data.values()):
            messagebox.showerror("Error", "Todos los campos de texto son obligatorios.")
            return

        if not lista_ids_destinos:
            messagebox.showerror("Error", "Debes agregar al menos un destino al paquete.")
            return

        try:
            nuevo_paquete = Paquetes(
                data['nombre'],
                data['fecha_inicio'],
                data['fecha_fin'],
                lista_ids_destinos,  # Pasamos la lista de IDs [1, 5, etc]
                data['precio'],
                data['cupos_disponibles']
            )
            if self.id_paquete is None:
                # CREAR

                nuevo_paquete.insertar_paquetes()
                messagebox.showinfo("Éxito", "Paquete creado correctamente.")
            else:
                # ACTUALIZAR
                nuevo_paquete.actualizar_paquetes(self.id_paquete)
                messagebox.showinfo("Éxito", "Paquete actualizado correctamente.")

            if self.callback:
                self.callback()
            self.destroy()

        except Exception as e:
            messagebox.showerror("Error crítico", f"{e}")
    def cargar_datos_simulados(self, id_paquete: int):
        paquete = buscar_paquete(id_paquete)
        if paquete:
            datos_paquete = {
                "nombre": paquete[1],
                "fecha_inicio": paquete[2],
                "fecha_fin": paquete[3],
                "precio": paquete[4],
                "cupos_disponibles": paquete[5]
            }

            for key, value in datos_paquete.items():
                if key in self.entries:
                    widget = self.entries[key]
                    if isinstance(widget, DateEntry):
                        # 1. Verificamos si es None o la fecha cero de SQL
                        # Convertimos a string para comparar seguramente
                        valor_str = str(value)

                        if value is None or valor_str == '0000-00-00':
                            # Si la fecha es inválida, ponemos HOY para evitar el error
                            widget.set_date(datetime.now())
                        else:
                            try:
                                # Intentamos poner la fecha de la base de datos
                                widget.set_date(value)
                            except Exception:
                                # Si falla por formato desconocido, ponemos HOY como respaldo
                                widget.set_date(datetime.now())
                    # --- FIN DE LA CORRECCIÓN ---
                    else:
                        widget.delete(0, tk.END)
                        widget.insert(0, str(value))

        destinos_actuales = obtener_destinos_de_paquete(id_paquete)
        self.destinos_seleccionados_lista = []
        self.tree_destinos.delete(*self.tree_destinos.get_children())

        for d_id, d_nombre in destinos_actuales:
            # Agregamos a la lista lógica
            self.destinos_seleccionados_lista.append({'id': d_id, 'nombre': d_nombre})
            # Agregamos a la lista visual
            self.tree_destinos.insert('', 'end', values=(d_id, d_nombre))