# Import required libraries
import sqlite3
  
# Connect to SQLite database
# New file created if it doesn't already exist
conn = sqlite3.connect('db1.db')
  
# Create cursor object
cursor = conn.cursor()
  
# Create and populate tables
cursor.executescript('''
CREATE TABLE Usuarios(
IDUsuario INTEGER PRIMARY KEY AUTOINCREMENT,
NombreUsuario TEXT NOT NULL,
Usuario TEXT NOT NULL,
Password TEXT NOT NULL
);
  
CREATE TABLE Predicciones(
IDPrediccion INTEGER PRIMARY KEY AUTOINCREMENT,
FechaDeteccion EXT NOT NULL,
Prediccion TEXT NOT NULL,
IDUsuario INTEGER,
FOREIGN KEY(IDUsuario) REFERENCES Usuarios(IDUsuario)
);
  
INSERT INTO Usuarios(NombreUsuario, Usuario, Password) VALUES
("Daniel Giraldo","Danielgi95","daniel1234");
  
''')
  
#Commit changes to database
conn.commit()
  
# Closing the connection
conn.close()