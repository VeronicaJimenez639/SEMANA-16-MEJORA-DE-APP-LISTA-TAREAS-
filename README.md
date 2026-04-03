# Lista de Tareas con Atajos de Teclado

## Descripción
Este proyecto corresponde a la mejora de la aplicación desarrollada en la Semana 15.  
Se reutiliza la base del sistema anterior, manteniendo la arquitectura modular por capas, e incorporando nuevas funciones de interacción mediante atajos de teclado en la interfaz gráfica desarrollada con Tkinter.

La aplicación permite registrar tareas, visualizarlas en una lista, marcarlas como completadas, desmarcarlas y eliminarlas. Además, en esta nueva versión, el usuario puede interactuar tanto con el mouse como con el teclado, facilitando el uso de la aplicación.

## Objetivo
Desarrollar una nueva versión del sistema trabajado en la Semana 15, incorporando atajos de teclado y manteniendo estrictamente la arquitectura modular por capas, sin alterar la separación de responsabilidades entre modelo, servicio, interfaz y punto de entrada.

## Estructura del proyecto
```bash
lista_tareas_app/
│
├── main.py
├── modelos/
│   └── tarea.py
├── servicios/
│   └── tarea_servicio.py
└── ui/
    └── app_tkinter.py
