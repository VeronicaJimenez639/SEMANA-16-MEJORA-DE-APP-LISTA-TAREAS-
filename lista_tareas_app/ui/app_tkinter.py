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

    # ==========================================================
    # REGISTRO DE EVENTOS
    # ==========================================================
    def _registrar_eventos(self):
        """
        Registra los eventos de teclado y ratón.
        """
        # Enter en el Entry
        self.entry_descripcion.bind("<Return>", self._evento_enter_anadir)

        # Selección y doble clic en la tabla
        self.treeview_tareas.bind("<<TreeviewSelect>>", self._evento_seleccionar_tarea)
        self.treeview_tareas.bind("<Double-1>", self._evento_doble_click_marcar)

        # Atajos globales
        self.root.bind_all("<KeyPress-c>", self._evento_tecla_c_marcar)
        self.root.bind_all("<KeyPress-C>", self._evento_tecla_c_marcar)

        self.root.bind_all("<Control-d>", self._evento_ctrl_d_eliminar)
        self.root.bind_all("<Control-D>", self._evento_ctrl_d_eliminar)

        self.root.bind_all("<Escape>", self._evento_escape_cerrar)

        # Confirmar cierre con la X
        self.root.protocol("WM_DELETE_WINDOW", self._cerrar_aplicacion)

    # ==========================================================
    # MÉTODOS PRINCIPALES
    # ==========================================================
    def _anadir_tarea(self):
        """
        Crea una nueva tarea con el texto ingresado.
        """
        descripcion_ingresada = self.descripcion_var.get().strip()

        if not descripcion_ingresada:
            self.lbl_estado.config(text="Debe escribir una descripción para la tarea.")
            messagebox.showwarning("Aviso", "Debe escribir una descripción para la tarea.")
            self.entry_descripcion.focus()
            return

        try:
            tarea_nueva = self.tarea_servicio.agregar_tarea(descripcion_ingresada)
            self._insertar_tarea_en_treeview(tarea_nueva)
            self.descripcion_var.set("")
            self.entry_descripcion.focus()
            self.lbl_estado.config(text="Tarea añadida correctamente.")
        except ValueError as error:
            self.lbl_estado.config(text=f"Error: {error}")
            messagebox.showerror("Error", str(error))

    def _insertar_tarea_en_treeview(self, tarea):
        """
        Inserta una tarea en el Treeview.
        """
        estado_texto = "Pendiente"
        etiquetas = ("pendiente",)

        if tarea.estado_completado:
            estado_texto = "[Hecho]"
            etiquetas = ("completada",)

        self.treeview_tareas.insert(
            "",
            "end",
            iid=str(tarea.identificador),
            values=(tarea.descripcion, estado_texto),
            tags=etiquetas
        )

    def _obtener_identificador_seleccionado(self):
        """
        Obtiene el identificador de la tarea seleccionada.
        Retorna None si no hay ninguna seleccionada.
        """
        seleccion = self.treeview_tareas.selection()

        if not seleccion:
            return None

        return int(seleccion[0])

    def _marcar_tarea_completada(self):
        """
        Marca como completada la tarea seleccionada.
        """
        identificador_seleccionado = self._obtener_identificador_seleccionado()

        if identificador_seleccionado is None:
            self.lbl_estado.config(text="Seleccione una tarea para marcarla como completada.")
            messagebox.showwarning("Aviso", "Seleccione una tarea para marcarla como completada.")
            return

        fue_marcada = self.tarea_servicio.marcar_tarea_completada(identificador_seleccionado)

        if fue_marcada:
            tarea_encontrada = self.tarea_servicio.buscar_tarea_por_identificador(
                identificador_seleccionado
            )

            self.treeview_tareas.item(
                str(identificador_seleccionado),
                values=(tarea_encontrada.descripcion, "[Hecho]"),
                tags=("completada",)
            )

            self.treeview_tareas.selection_remove(self.treeview_tareas.selection())
            self.lbl_estado.config(text="Tarea marcada como completada.")
        else:
            self.lbl_estado.config(text="No se pudo marcar la tarea seleccionada.")
            messagebox.showerror("Error", "No se pudo marcar la tarea seleccionada.")

    def _desmarcar_tarea(self):
        """
        Devuelve una tarea completada nuevamente al estado pendiente.
        """
        identificador_seleccionado = self._obtener_identificador_seleccionado()

        if identificador_seleccionado is None:
            self.lbl_estado.config(text="Seleccione una tarea para desmarcarla.")
            messagebox.showwarning("Aviso", "Seleccione una tarea para desmarcarla.")
            return

        fue_desmarcada = self.tarea_servicio.desmarcar_tarea(identificador_seleccionado)

        if fue_desmarcada:
            tarea_encontrada = self.tarea_servicio.buscar_tarea_por_identificador(
                identificador_seleccionado
            )

            self.treeview_tareas.item(
                str(identificador_seleccionado),
                values=(tarea_encontrada.descripcion, "Pendiente"),
                tags=("pendiente",)
            )

            self.treeview_tareas.selection_remove(self.treeview_tareas.selection())
            self.lbl_estado.config(text="Tarea desmarcada correctamente.")
        else:
            self.lbl_estado.config(text="No se pudo desmarcar la tarea seleccionada.")
            messagebox.showerror("Error", "No se pudo desmarcar la tarea seleccionada.")

    def _eliminar_tarea(self):
        """
        Elimina la tarea seleccionada.
        """
        identificador_seleccionado = self._obtener_identificador_seleccionado()

        if identificador_seleccionado is None:
            self.lbl_estado.config(text="Seleccione una tarea para eliminarla.")
            messagebox.showwarning("Aviso", "Seleccione una tarea para eliminarla.")
            return

        respuesta = messagebox.askyesno(
            "Confirmar",
            "¿Está seguro de que desea eliminar la tarea seleccionada?"
        )

        if respuesta:
            fue_eliminada = self.tarea_servicio.eliminar_tarea(identificador_seleccionado)

            if fue_eliminada:
                self.treeview_tareas.delete(str(identificador_seleccionado))
                self.lbl_estado.config(text="Tarea eliminada correctamente.")
            else:
                self.lbl_estado.config(text="No se pudo eliminar la tarea seleccionada.")
                messagebox.showerror("Error", "No se pudo eliminar la tarea seleccionada.")

    def _cerrar_aplicacion(self):
        """
        Solicita confirmación antes de cerrar la aplicación.
        """
        respuesta = messagebox.askyesno(
            "Salir",
            "¿Está seguro de que desea cerrar la aplicación?"
        )

        if respuesta:
            self.root.destroy()





