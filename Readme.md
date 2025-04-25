# Laboratorio de Gestión de Procesos – Parte 1  
**Generador de Catálogos de Procesos**

---

## 📋 Objetivo  
Implementar una aplicación de escritorio que permita capturar procesos activos del sistema, catalogarlos según criterios de CPU o memoria, y guardar cada catálogo.

---

## 📚 Requerimientos Funcionales  
1. **Captura de Procesos**  
   - El usuario ingresa un número **N** de procesos a capturar.  
   - Selección por **mayor uso de CPU** o **mayor uso de Memoria**.  
2. **Datos a Obtener por Proceso**  
   - **Catálogo:** número consecutivo dentro del criterio.  
   - **Nombre de Catálogo:** texto descriptivo dado por el usuario.  
   - **PID:** identificador del proceso.  
   - **Nombre:** nombre del ejecutable.  
   - **Usuario:** quien lanzó el proceso.  
   - **Prioridad:**  
     - `1` (no expulsivo) si el usuario es “system” (o equivalente).  
     - `0` (expulsivo) para el resto.  
3. **Almacenamiento**  
   - Guardar cada catálogo en  
     ```
     catalogos/<criterio>/<ID>-<Nombre>.json
     ```
   - El ID se genera automáticamente (`cpu-01`, `cpu-02`, … / `memoria-01`, …).  
   - Al guardar, el diálogo sugiere por defecto el “Nombre de Catálogo” actual.

---

## ✅ Desarrollo Realizado

### 1. Interfaz de Usuario  
- Basada en **CustomTkinter** para un look-and-feel moderno (dark mode, esquinas redondeadas, acentos verdes).  
- **Entradas**:  
  - Campo de texto para cantidad de procesos.  
  - RadioButtons para CPU / Memoria.  
  - Botón “🔍 Capturar”.  
- **Treeview estilizado** con fuente aumentada, filas más altas y scrollbar integrado.  
- **Status bar** fija abajo mostrando el estado (`Listo` / `🖥️ Capturados: N procesos`).  
- **Botones** “💾 Guardar” y “📚 Catálogos” con iconografía y hover effects.

### 2. Lógica de Captura y Guarda  
- Uso de **psutil** para iterar procesos (`pid`, `name`, `username`, `memory_info`, `cpu_percent`).  
- Ordena y selecciona los top-N procesos según el criterio.  
- Construye instancias de `Proceso` con los campos requeridos.  
- Inserta datos en la grilla y mantiene `current_catalog_name`.  
- `save_processes()` abre un diálogo `simpledialog.askstring()` con `initialvalue` pre-llenado.  
- Archivos JSON generados en carpetas `catalogos/cpu` y `catalogos/memoria`, sin sobrescribir IDs previos.

### 3. Gestión de Catálogos Guardados  
- Módulo **`ver_catalogos`** con:  
  - **`utilidades.py`**  
    ```python
    def cargar_procesos_desde_archivo(ruta) -> list
    def listar_catalogos_por_categoria() -> dict
    ```  
  - **`interfaz.py`**  
    ```python
    def crear_ventana_catalogos(cats: dict, parent=None) -> CTkToplevel
    ```  
  - **`mostrar_catalogos.py`**  
    ```python
    def mostrar_catalogos()
    ```  
- La ventana de catálogos usa CTkToplevel y comparte el mismo tema oscuro, sin bloquear la ventana principal.

### 4. Launcher con Splash Screen  
- Archivo **`launcher_ctk.py`** que:  
  - Muestra un splash moderno (CTkToplevel, título, progress bar indeterminate).  
  - Centra automáticamente el splash y luego la ventana principal.  
  - Usa la misma configuración de **CustomTkinter** para consistencia visual.

---

## 🚀 Instalación y Ejecución

```bash
# 1. Clonar el repositorio
git clone https://github.com/Hugo-Uparela/Desktop-process-management.git
cd Desktop-process-management

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar el launcher
python init.py

```

## 📂 Estructura de Carpetas
```
Desktop-process-management
├─ catalogos
│  ├─ cpu
│  │  ├─ cpu-01-Catalogo CPU 1.json
│  │  ├─ cpu-02-Catalogo CPU 2.json
│  │  ├─ cpu-03-Catalogo CPU 3.json
│  │  ├─ cpu-04-Catalogo CPU 4.json
│  │  └─ cpu-05-Catalogo CPU 5.json
│  └─ memoria
│     ├─ memoria-01-Catalogo MEMORIA 1.json
│     ├─ memoria-02-Catalogo MEMORIA 2.json
│     ├─ memoria-03-Catalogo MEMORIA 3.json
│     ├─ memoria-04-Catalogo MEMORIA 4.json
│     └─ memoria-05-Catalogo MEMORIA 5.json
├─ gestor_procesos.py           # Código principal de la app de captura
├─ init.py                      # Launcher/Splash (inicia gestor_procesos)
├─ Readme.md                    # Documentación y guía de uso
├─ requirements.txt             # Lista de dependencias (psutil, customtkinter…)
└─ ver_catalogos
   ├─ interfaz.py               # UI para mostrar los catálogos guardados
   ├─ mostrar_catalogos.py      # Orquesta listar+mostrar catálogos
   └─ utilidades.py             # Funciones de carga/listado de archivos JSON
