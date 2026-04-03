import tkinter as tk
from tkinter import ttk, messagebox

from servicios.tarea_servicio import TareaServicio


class AppTkinter:
    """
    Interfaz gráfica principal de la aplicación.
    Aquí se construyen los widgets y se capturan los eventos del usuario.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.tarea_servicio = TareaServicio()
        self.descripcion_var = tk.StringVar()

        self._configurar_ventana()
        self._aplicar_estilos()
        self._crear_componentes()
        self._registrar_eventos()

    # ==========================================================
    # CONFIGURACIÓN GENERAL
    # ==========================================================
    def _configurar_ventana(self):
        """
        Configura las propiedades principales de la ventana.
        """
        self.root.title("Lista de Tareas")
        self.root.geometry("700x480")
        self.root.resizable(False, False)

    def _aplicar_estilos(self):
        """
        Aplica estilos visuales para el Treeview.
        """
        self.estilo = ttk.Style()
        self.estilo.theme_use("clam")

        self.estilo.configure("Treeview", rowheight=26)
        self.estilo.configure("Treeview.Heading", font=("Arial", 10, "bold"))

    # ==========================================================
    # INTERFAZ
    # ==========================================================
    def _crear_componentes(self):
        """
        Crea todos los elementos visuales de la aplicación.
        """
        self._crear_area_superior()
        self._crear_botones()
        self._crear_etiqueta_estado()
        self._crear_lista_tareas()

    def _crear_area_superior(self):
        """
        Crea la parte superior con la etiqueta y el campo de entrada.
        """
        frame_superior = ttk.Frame(self.root, padding=10)
        frame_superior.pack(fill="x")

        etiqueta_descripcion = ttk.Label(
            frame_superior,
            text="Descripción de la tarea:"
        )
        etiqueta_descripcion.pack(anchor="w", pady=(0, 5))

        self.entry_descripcion = ttk.Entry(
            frame_superior,
            textvariable=self.descripcion_var,
            width=60
        )
        self.entry_descripcion.pack(fill="x", pady=(0, 10))
        self.entry_descripcion.focus()

        self.frame_botones = ttk.Frame(frame_superior)
        self.frame_botones.pack(fill="x", pady=(0, 10))

    def _crear_botones(self):
        """
        Crea los botones principales de la aplicación.
        """
        self.boton_anadir_tarea = ttk.Button(
            self.frame_botones,
            text="Añadir Tarea",
            command=self._anadir_tarea
        )
        self.boton_anadir_tarea.pack(side="left", padx=(0, 10))

        self.boton_marcar_completada = ttk.Button(
            self.frame_botones,
            text="Marcar Completada",
            command=self._marcar_tarea_completada
        )
        self.boton_marcar_completada.pack(side="left", padx=(0, 10))

        self.boton_desmarcar_tarea = ttk.Button(
            self.frame_botones,
            text="Desmarcar Tarea",
            command=self._desmarcar_tarea
        )
        self.boton_desmarcar_tarea.pack(side="left", padx=(0, 10))

        self.boton_eliminar_tarea = ttk.Button(
            self.frame_botones,
            text="Eliminar",
            command=self._eliminar_tarea
        )
        self.boton_eliminar_tarea.pack(side="left")

    def _crear_etiqueta_estado(self):
        """
        Crea una etiqueta para mostrar mensajes y atajos.
        """
        self.lbl_estado = ttk.Label(
            self.root,
            text="Listo. Use Enter para añadir, C para completar, Ctrl+D para eliminar y Esc para salir.",
            foreground="#1d3b6b"
        )
        self.lbl_estado.pack(anchor="w", padx=10, pady=(0, 10))

    def _crear_lista_tareas(self):
        """
        Crea el Treeview donde se mostrarán las tareas.
        """
        frame_lista = ttk.Frame(self.root, padding=(10, 0, 10, 10))
        frame_lista.pack(fill="both", expand=True)

        self.treeview_tareas = ttk.Treeview(
            frame_lista,
            columns=("descripcion", "estado"),
            show="headings",
            height=14
        )
        self.treeview_tareas.heading("descripcion", text="Descripción")
        self.treeview_tareas.heading("estado", text="Estado")

        self.treeview_tareas.column("descripcion", width=460)
        self.treeview_tareas.column("estado", width=180, anchor="center")
        self.treeview_tareas.pack(fill="both", expand=True)

        self.treeview_tareas.tag_configure(
            "pendiente",
            background="#FFF9C4",
            foreground="black"
        )
        self.treeview_tareas.tag_configure(
            "completada",
            background="#C8E6C9",
            foreground="black"
        )



