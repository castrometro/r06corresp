import tkinter as tk
from tkinter import filedialog, messagebox
from options.crear_corresponsales import generar_corresponsales, status_generar_corresponsales
from options.crear_divisas import generar_divisas, status_generar_divisas

# Funciones para la interfaz de usuario
def crear_corresponsales():
    if not status_generar_corresponsales():
        messagebox.showinfo("Alerta", "Opcion Crear archivo Corresponsales no disponible.")
    else:
        try:
            error = generar_corresponsales()
            if error:
                messagebox.showerror("Error", f"Ocurrió un error al generar archivo corresponsales {error}")
            else:
                messagebox.showinfo("Información", "Archivo Corresponsales generado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al generar archivo corresponsales: {e}")

def crear_divisas():
    messagebox.showinfo("Información", "Funcionalidad en Desarrollo.")

def completar_informacion():
    # Lógica para completar información
    messagebox.showinfo("Información", "Funcionalidad en Desarrollo.")

def center_window(self, width=400, height=300):
    # Obtiene las dimensiones de la pantalla del usuario
    screen_width = self.top.winfo_screenwidth()
    screen_height = self.top.winfo_screenheight()

    # Calcula la posición x e y para centrar la ventana
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)

    self.top.geometry('%dx%d+%d+%d' % (width, height, x, y))

# Clase para la interfaz de usuario
class Aplicacion:
    def __init__(self, root):
        self.top = tk.Toplevel(root)  # Crear una ventana de nivel superior
        self.top.title('Generador R06')  # Título de la ventana

        # Centrar la ventana en la pantalla
        center_window(self, 400, 100) #ancho,altura

        # Configuración de botones en la ventana de nivel superior
        tk.Button(self.top, text='Generar Archivo Corresponsales', command=crear_corresponsales).pack(fill=tk.X)
        tk.Button(self.top, text='Generar Archivo Divisas Pendientes', command=crear_divisas).pack(fill=tk.X)
        tk.Button(self.top, text=':D', command=completar_informacion).pack(fill=tk.X)

        # Manejar el cierre de la ventana Toplevel
        self.top.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def on_close(self):
        self.top.quit()



# Configuración del entorno Tkinter
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    app = Aplicacion(root)
    root.mainloop()
