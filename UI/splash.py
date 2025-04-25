import customtkinter as ctk

def center_window(win, width, height):
    """
    Centra la ventana `win` con tamaño width×height en pantalla.
    """
    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()
    x = (screen_w - width) // 2
    y = (screen_h - height) // 2
    win.geometry(f"{width}x{height}+{x}+{y}")

def show_splash(parent, on_close):
    splash = ctk.CTkToplevel(parent)
    splash.overrideredirect(True)

    w, h = 420, 260
    center_window(splash, w, h)

    splash.configure(fg_color="#242424", corner_radius=12)

    frame = ctk.CTkFrame(
        splash,
        fg_color="#1f1f1f",
        corner_radius=12,
        border_width=2,
        border_color="#3b8ed0"
    )
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    ctk.CTkLabel(
        frame,
        text="🛠️ Gestor de Procesos",
        font=ctk.CTkFont(size=29, weight="bold"),
        text_color="white"
    ).pack(pady=(20, 5))

    ctk.CTkLabel(
        frame,
        text="Cargando aplicación...",
        font=ctk.CTkFont(size=14),
        text_color="#a1a1a1"
    ).pack(pady=(0, 20))

    progress = ctk.CTkProgressBar(
        frame,
        orientation="horizontal",
        mode="indeterminate",
        width=300
    )
    progress.pack(pady=10)
    progress.start()

    def close():
        splash.destroy()
        on_close()

    splash.after(2500, close)