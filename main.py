import pyodbc
import tkinter as tk
from tkinter import messagebox

class Regla:
    def __init__(self, genero: str, condiciones: set, conclusion: str):
        self.genero = genero
        self.condiciones = condiciones
        self.conclusion = conclusion

def conectar_base_datos():
    return pyodbc.connect(
        r'DRIVER=SQL Server;'
        r'SERVER=DESKTOP-J9H4PGR\MSSQLSERVER01;'
        r'DATABASE=SistemasExpertosDB;'
        r'UID=sa;'
        r'PWD=Everise$2024.;'
    )

def obtener_reglas():
    with conectar_base_datos() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT genero, condiciones, conclusion FROM Reglas")
        
        reglas = []
        generos_disponibles = set()
        
        for row in cursor.fetchall():
            genero = row.genero.strip().lower()
            generos_disponibles.add(genero)
            condiciones = set(row.condiciones.split(', '))
            conclusion = row.conclusion
            reglas.append(Regla(genero, condiciones, conclusion))
    
    return reglas, generos_disponibles

def agregar_regla(genero, condiciones, conclusion):
    with conectar_base_datos() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Reglas (genero, condiciones, conclusion) VALUES (?, ?, ?)",
                       genero, condiciones, conclusion)
        conn.commit()

    cargar_generos()

def encadenamiento_hacia_adelante(hechos: set, reglas: list, genero_seleccionado: str) -> set:
    conclusiones = set()
    nuevo_hecho_agregado = True

    while nuevo_hecho_agregado:
        nuevo_hecho_agregado = False
        for regla in reglas:
            if regla.genero == genero_seleccionado and regla.condiciones.issubset(hechos):
                if regla.conclusion not in hechos:
                    hechos.add(regla.conclusion)
                    conclusiones.add(regla.conclusion)
                    nuevo_hecho_agregado = True

    return conclusiones

def mostrar_recomendaciones():
    genero = listbox_generos.get(listbox_generos.curselection()).strip().lower() 
    duracion = duracion_var.get().strip().lower()

    hechos = {genero, duracion}
    reglas, _ = obtener_reglas()
    recomendaciones = encadenamiento_hacia_adelante(hechos.copy(), reglas, genero)

    text_area.delete("1.0", tk.END) 
    if recomendaciones:
        resultado = "\n".join(recomendaciones)
        text_area.insert(tk.END, f"Te recomendamos ver las siguientes películas:\n{resultado}")
    else:
        text_area.insert(tk.END, "No se encontraron recomendaciones basadas en tus preferencias.")

def agregar_nueva_regla():
    genero = genero_nuevo.get().strip().lower()
    condiciones = condiciones_nuevas.get().strip().lower()
    conclusion = conclusion_nueva.get().strip().lower()
    
    if genero and condiciones and conclusion:
        loading_label.grid(row=9, column=0, columnspan=2, pady=10)
        root.update()
        agregar_regla(genero, condiciones, conclusion)
        loading_label.grid_remove()
        messagebox.showinfo("Éxito", "Regla añadida exitosamente.")
    else:
        messagebox.showwarning("Advertencia", "Por favor, completa todos los campos.")

def cargar_generos():
    listbox_generos.delete(0, tk.END)
    _, generos_disponibles = obtener_reglas()
    for genero in generos_disponibles:
        listbox_generos.insert(tk.END, genero.capitalize())

def on_enter(event):
    event.widget['bg'] = '#1ABC9C' 

def on_leave(event):
    event.widget['bg'] = '#4CAF50' 

root = tk.Tk()
root.title("Sistema Experto de Recomendación de Películas")
root.geometry("600x600")
root.configure(bg="#2C3E50")

frame = tk.Frame(root, bg="#34495E")  
frame.pack(pady=20, padx=20)

duracion_var = tk.StringVar()

tk.Label(frame, text="Géneros disponibles:", bg="#34495E", fg="white", font=("Helvetica", 14)).grid(row=0, column=0, padx=10, pady=10)
listbox_generos = tk.Listbox(frame, height=5, width=30, font=("Helvetica", 12))
listbox_generos.grid(row=0, column=1, padx=10, pady=10)

tk.Label(frame, text="Duración (corta/larga):", bg="#34495E", fg="white", font=("Helvetica", 14)).grid(row=1, column=0, padx=10, pady=10)
tk.Entry(frame, textvariable=duracion_var, font=("Helvetica", 12)).grid(row=1, column=1, padx=10, pady=10)

button_recommend = tk.Button(frame, text="Mostrar Recomendaciones", command=mostrar_recomendaciones, bg="#2980B9", fg="white", font=("Helvetica", 12))
button_recommend.grid(row=2, column=0, columnspan=2, pady=10)
button_recommend.bind("<Enter>", on_enter)  
button_recommend.bind("<Leave>", on_leave)  

text_area = tk.Text(frame, height=10, width=50, font=("Helvetica", 12))
text_area.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

tk.Label(frame, text="Agregar nueva regla:", bg="#34495E", fg="white", font=("Helvetica", 14)).grid(row=4, column=0, columnspan=2, pady=10)

tk.Label(frame, text="Género:", bg="#34495E", fg="white").grid(row=5, column=0, padx=10, pady=5)
genero_nuevo = tk.Entry(frame, font=("Helvetica", 12))
genero_nuevo.grid(row=5, column=1, padx=10, pady=5)

tk.Label(frame, text="Condiciones (separadas por comas):", bg="#34495E", fg="white").grid(row=6, column=0, padx=10, pady=5)
condiciones_nuevas = tk.Entry(frame, font=("Helvetica", 12))
condiciones_nuevas.grid(row=6, column=1, padx=10, pady=5)

tk.Label(frame, text="Conclusión:", bg="#34495E", fg="white").grid(row=7, column=0, padx=10, pady=5)
conclusion_nueva = tk.Entry(frame, font=("Helvetica", 12))
conclusion_nueva.grid(row=7, column=1, padx=10, pady=5)

button_add_rule = tk.Button(frame, text="Agregar Regla", command=agregar_nueva_regla, bg="#4CAF50", fg="white", font=("Helvetica", 12))
button_add_rule.grid(row=8, column=0, columnspan=2, pady=10)
button_add_rule.bind("<Enter>", on_enter)  
button_add_rule.bind("<Leave>", on_leave)  


loading_label = tk.Label(frame, text="Actualizando reglas, por favor espere...", bg="#34495E", fg="orange")
loading_label.grid_remove()  

cargar_generos()


root.mainloop()
