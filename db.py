
# db.py
import pyodbc

def obtener_reglas():
    # Conectar a la base de datos
    conn = pyodbc.connect(
        r'DRIVER=SQL Server;'
        r'SERVER=DESKTOP-J9H4PGR\MSSQLSERVER01;'
        r'DATABASE=SistemasExpertosDB;'
        r'UID=sa;'
        r'PWD=Everise$2024.;'
    )
    
    cursor = conn.cursor()
    
    # Obtener las reglas de la tabla
    cursor.execute("SELECT Condiciones, conclusion FROM Reglas")
    
    reglas = []
    for row in cursor.fetchall():
        condiciones = set(row.Condiciones.split(', '))  # Asegúrate de que el nombre de la columna sea correcto
        conclusion = row.conclusion
        reglas.append(Regla(condiciones, conclusion))
    
    conn.close()
    return reglas
