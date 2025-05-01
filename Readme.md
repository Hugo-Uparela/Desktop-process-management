# Laboratorio de Gestión de Procesos – Parte 1
**Generador de Catálogos de Procesos**

---
## 📋 Objetivo de la Primera Aplicación
Desarrollar una aplicación de escritorio en Python que:
1. Capture un número de procesos activos definido por el usuario.  
2. Permita seleccionar los procesos por mayor uso de **CPU** o **Memoria**.  
3. Genere un **ID de Catálogo** automático (p.ej. `cpu-01`, `memoria-02`) y asigne un **Nombre de Catálogo** (descriptivo) ingresado por el usuario.  
4. Registre para cada proceso: `PID`, `Nombre`, `Usuario` y `Prioridad` (0=Expulsivo, 1=No expulsivo).  
5. Almacene toda la información (en nuestro caso una base de datos SQLite (`procesos.db`) con dos tablas: `cpu` y `memoria`).

---

## 🔧 Tecnologías y Librerías
- **Python 3.8+**  
- **CustomTkinter** (interfaz moderna)  
- **Tkinter** (widgets básicos)  
- **psutil** (lectura de procesos)  
- **SQLite** (persistencia local de catálogos)

---

## 🚀 Instalación y Ejecución
1. Clonar el repositorio:
   ```bash
   git clone https://github.com/Hugo-Uparela/Desktop-process-management.git
   cd Desktop-process-management
   ```

2. Ejecutar la aplicación:
   ```bash
   python init.py
   ```

La primera vez se creará automáticamente `procesos.db` en la raíz.

---

## 📂 Estructura de Carpetas
```
Desktop-process-management
├─ assets
│   └─ icono.ico            ← Ícono para el ejecutable
├─ procesos                
│   ├─ proceso.py           ← Clase Proceso (modelo de datos)
│   └─ manager.py           ← Lógica de captura y persistencia en SQLite
├─ UI
│   ├─ app.py               ← Interfaz principal y captura de procesos
│   └─ splash.py            ← Pantalla de carga y centrado de ventana
├─ ver_catalogos
│   ├─ utilidades.py        ← Acceso a la base de datos y consultas
│   └─ mostrar_catalogos.py ← Ventana para visualizar catálogos guardados
├─ init.py                 ← Launcher (splash + App().mainloop())
├─ requisitos.txt          ← Listado de librerías necesarias
└─ procesos.db             ← Base de datos (se crea dinámicamente)
```

---

## 🛠 Empaquetado
Para generar un ejecutable standalone.
```bash
pyinstaller --name gestor_procesos --onefile --windowed --icon "assets/icono.ico" init.py
```

---

## 📖 Descripción del Taller completo
En la siguiente fase (Parte 2), se implementará un simulador de planificación ROUND ROBIN que:
- Lea los catálogos generados en esta aplicación.  
- Modele estados de proceso (Listo, Ejecución, Terminado).  
- Genere archivos de descripción por proceso y mantenga contadores de ráfaga.  
- Permita reiniciar o interrumpir la simulación.  


