import customtkinter as ctk
from UI.app import App
from UI.splash import center_window, show_splash

# Configuración global de CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

if __name__ == "__main__":
    app = App()
    app.withdraw() 

    def start_app():
        app.update_idletasks()
        w = app.winfo_reqwidth()
        h = app.winfo_reqheight()
        center_window(app, w, h)
        app.deiconify()

    show_splash(app, start_app)
    app.mainloop()