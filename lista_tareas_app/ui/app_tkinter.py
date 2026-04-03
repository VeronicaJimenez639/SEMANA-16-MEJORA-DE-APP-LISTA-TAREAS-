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





