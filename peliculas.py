class Regla:
    def __init__(self, condicion, conclusion):
        self.condicion = condicion
        self.conclusion = conclusion

    def aplica(self, preferencias_actuales):
        if all(preferencia in preferencias_actuales for preferencia in self.condicion):
            return self.conclusion
        return None

# Definir reglas para recomendaciones de películas
reglas = [
    Regla(["le gustan las películas de acción", "prefiere películas largas"], "Recomendamos 'El señor de los anillos'"),
    Regla(["le gustan las películas de acción", "prefiere películas cortas"], "Recomendamos 'Black Panther'"),
    Regla(["le gustan las películas de drama", "prefiere películas largas"], "Recomendamos 'Hachiko'"),
    Regla(["le gustan las películas de drama", "prefiere películas cortas"], "Recomendamos 'Her'"),
    Regla(["le gustan las películas de comedia", "prefiere películas largas"], "Recomendamos 'Click'"),
    Regla(["le gustan las películas de comedia", "prefiere películas cortas"], "Recomendamos 'Shrek 2'")
]

def obtener_preferencia():
    genero = input("¿Qué género te gusta? (acción, drama, comedia): ").strip().lower()
    duracion = input("¿Prefieres películas largas o cortas?: ").strip().lower()
    
    preferencias_actuales.clear()  # Limpiar las preferencias para cada nueva consulta

    if genero == "acción":
        preferencias_actuales.add("le gustan las películas de acción")
    elif genero == "drama":
        preferencias_actuales.add("le gustan las películas de drama")
    elif genero == "comedia":
        preferencias_actuales.add("le gustan las películas de comedia")
    
    if duracion == "largas":
        preferencias_actuales.add("prefiere películas largas")
    elif duracion == "cortas":
        preferencias_actuales.add("prefiere películas cortas")

# Definir las preferencias iniciales (vacías al inicio)
preferencias_actuales = set()

while True:
    obtener_preferencia()

    # Evaluar reglas
    recomendaciones = []
    for regla in reglas:
        resultado = regla.aplica(preferencias_actuales)
        if resultado:
            recomendaciones.append(resultado)
    
    # Mostrar recomendaciones
    if recomendaciones:
        print("Recomendaciones de películas:")
        for recomendacion in recomendaciones:
            print(f"- {recomendacion}")
    else:
        print("No se encontraron recomendaciones que coincidan con tus preferencias.")

    # Preguntar si el usuario quiere hacer otra consulta
    continuar = input("¿Quieres hacer otra consulta? (sí/no): ").strip().lower()
    if continuar == "no":
        print("¡Feliz día!")
        break
    elif continuar == "sí":
        # Limpiar preferencias para nueva consulta
        preferencias_actuales.clear()