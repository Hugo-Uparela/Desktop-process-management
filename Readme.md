# Laboratorio de Gestión de Procesos – Parte 1  
**Generador de Catálogos de Procesos**

---

## 📋 Objetivo  
Crear una aplicación de escritorio que capture procesos activos del sistema, los catalogue por uso de CPU o memoria y permita guardarlos con nombre por defecto o personalizado.

---

## 🔧 Tecnologías  
- **Python 3.8+**  
- **CustomTkinter**  
- **psutil** 
- **Tkinter** 

---

## 🚀 Instalación y Ejecución

1. **Clonar repositorio**  
   ```bash
   git clone https://github.com/Hugo-Uparela/Desktop-process-management.git
   cd Desktop-process-management

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Ejecutar**
```
python init.py
```


## 📂 Estructura de Carpetas
```
Desktop-process-management
├─ assets
│   ├─ icono.ico        ← Icono para el .exe
├─ catalogos
│   ├─ cpu
│   │   ├─ cpu-01-<nombre>.json
│   │   └─ …
│   └─ memoria
│       ├─ memoria-01-<nombre>.json
│       └─ …
├─ procesos
│   ├─ __init__.py
│   ├─ proceso.py       ← Clase Proceso
│   └─ manager.py       ← Lógica de captura y guardado
├─ UI
│   ├─ __init__.py
│   ├─ app.py           ← Clase App (interfaz principal)
│   └─ splash.py        ← Splash screen y utilidades de centrado
├─ ver_catalogos
│   ├─ __init__.py
│   ├─ utilidades.py    ← Funciones de carga y listado
│   ├─ interfaz.py      ← Construcción de la ventana de catálogos
│   └─ mostrar_catalogos.py ← Orquestador para mostrar catálogos
├─ init.py              ← Launcher con splash + App().mainloop()
├─ requirements.txt
└─ Readme.md
```

## 🛠 Empaquetado
Para generar un .exe standalone con ícono y todas las dependencias:

```
pyinstaller --name gestor_procesos 
--onefile 
--windowed 
--icon "assets/icono.ico" 
--add-data "catalogos;catalogos" 
--add-data "ver_catalogos;ver_catalogos" init.py
