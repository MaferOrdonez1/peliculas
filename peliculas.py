import pyodbc
import tkinter as tk
from tkinter import messagebox, ttk

class Regla:
    def __init__(self, condicion, conclusion):
        self.condicion = condicion.split(", ")
        self.conclusion = conclusion

    def aplica(self, preferencias_actuales):
        if all(preferencia in preferencias_actuales for preferencia in self.condicion):
            return self.conclusion
        return None

# Cargar reglas desde la base de datos SQL Server
def cargar_reglas():
    conn = pyodbc.connect(
        r'DRIVER=SQL Server;'
        r'SERVER=DESKTOP-J9H4PGR\MSSQLSERVER01;'  # Cambia por el nombre de tu servidor o instancia
        r'DATABASE=SistemasExpertosDB;'  # Cambia por el nombre de tu base de datos
        r'UID=sa;'  # Cambia por tu usuario de SQL Server
        r'PWD=Everise$2024.;'  # Cambia por tu contraseña de SQL Server
    )
    cursor = conn.cursor()
    cursor.execute('SELECT condicion, conclusion FROM Reglas')
    reglas_db = cursor.fetchall()
    conn.close()
    reglas = [Regla(condicion, conclusion) for condicion, conclusion in reglas_db]
    return reglas

# Inicializar las reglas globalmente
reglas = cargar_reglas()

def obtener_recomendaciones(genero, duracion):
    preferencias_actuales = set()
    if genero == "acción":
        preferencias_actuales.add("le gustan las películas de acción") #corregir para que tome lo de la base de datos
    elif genero == "drama":
        preferencias_actuales.add("le gustan las películas de drama") 
    elif genero == "comedia":
        preferencias_actuales.add("le gustan las películas de comedia")

    if duracion == "largas":
        preferencias_actuales.add("prefiere películas largas")
    elif duracion == "cortas":
        preferencias_actuales.add("prefiere películas cortas")

    recomendaciones = []
    for regla in reglas:
        resultado = regla.aplica(preferencias_actuales)
        if resultado:
            recomendaciones.append(resultado)

    return recomendaciones

def mostrar_recomendaciones():
    genero = genero_var.get().lower()
    duracion = duracion_var.get().lower()
    if not genero or not duracion:
        messagebox.showwarning("Advertencia", "Por favor, selecciona un género y una duración.")
        return

    recomendaciones = obtener_recomendaciones(genero, duracion)
    
    if recomendaciones:
        recomendaciones_texto = "\n".join(recomendaciones)
        messagebox.showinfo("Recomendaciones", f"Recomendaciones:\n{recomendaciones_texto}")
    else:
        messagebox.showinfo("Recomendaciones", "No se encontraron recomendaciones que coincidan con tus preferencias.")



ventana = tk.Tk()
ventana.title("Sistema de Recomendaciones de Películas")
ventana.geometry("400x300")
ventana.resizable(False, False)


genero_var = tk.StringVar()
duracion_var = tk.StringVar()

frame = ttk.Frame(ventana, padding="10")
frame.pack(fill=tk.BOTH, expand=True)

ttk.Label(frame, text="Consultar recomendaciones", font=("Arial", 14)).pack(pady=10)

ttk.Label(frame, text="Género:").pack()
ttk.Entry(frame, textvariable=genero_var).pack()

ttk.Label(frame, text="Duración (largas/cortas):").pack()
ttk.Entry(frame, textvariable=duracion_var).pack()

ttk.Button(frame, text="Obtener recomendaciones", command=mostrar_recomendaciones).pack(pady=10)

# Iniciar la interfaz gráfica
ventana.mainloop()
