# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 17:57:50 2025
@author: Pablo, Adrian Subire, Mohammed, Fabian
"""
import sqlite3
import tkinter as tkinter
from tkinter import ttk

raiz = tkinter.Tk()
raiz.title("UDUU")
raiz.geometry("800x600")

# Configurar que las columnas se expandan proporcionalmente
raiz.grid_columnconfigure(0, weight=1)
raiz.grid_columnconfigure(1, weight=1)
raiz.grid_columnconfigure(2, weight=1)
raiz.grid_columnconfigure(3, weight=1)
raiz.grid_columnconfigure(4, weight=1)

textoCrear = "Crear"
botonCrear = tkinter.Button(raiz, text=textoCrear, relief="solid", bd=1, highlightbackground="black", highlightthickness=1)
botonCrear.grid(row=0, column=0, sticky="ew")
botonCrear.config(fg="white", bg="dodgerblue", font=('arial',15))

textoBorrar = "Eliminar"
botonBorrar = tkinter.Button(raiz, text=textoBorrar, relief="solid", bd=1, highlightbackground="black", highlightthickness=1)
botonBorrar.grid(row=0, column=1, sticky="ew")
botonBorrar.config(fg="white", bg="dodgerblue", font=('arial',15))

textoEditar = "Editar"
botonEditar = tkinter.Button(raiz, text=textoEditar, relief="solid", bd=1, highlightbackground="black", highlightthickness=1)
botonEditar.grid(row=0, column=2, sticky="ew")
botonEditar.config(fg="white", bg="dodgerblue", font=('arial',15))

textoBuscar = "Buscar"
botonBuscar = tkinter.Button(raiz, text=textoBuscar, relief="solid", bd=1, highlightbackground="black", highlightthickness=1)
botonBuscar.grid(row=0, column=3, sticky="ew")
botonBuscar.config(fg="white", bg="dodgerblue", font=('arial',15))

textoGrafico = "Grafico"
botonGrafico = tkinter.Button(raiz, text=textoGrafico, relief="solid", bd=1, highlightbackground="black", highlightthickness=1)
botonGrafico.grid(row=0, column=4, sticky="ew")
botonGrafico.config(fg="white", bg="dodgerblue", font=('arial',15))

# Conexión a la base de datos
conexion = sqlite3.connect("supermercado.db")
cursor = conexion.cursor()

# Activar claves foráneas en SQLite
cursor.execute("PRAGMA foreign_keys = ON")

# Crear tabla categoria (debe ir primero porque producto la referencia)
cursor.execute("CREATE TABLE IF NOT EXISTS categoria(id_Categoria INTEGER PRIMARY KEY AUTOINCREMENT, nombre_Categoria VARCHAR(20))")

# Crear tabla cliente (debe ir antes de pedido porque pedido la referencia)
cursor.execute("CREATE TABLE IF NOT EXISTS cliente(id_Cliente INTEGER PRIMARY KEY AUTOINCREMENT, nombre_Cliente VARCHAR(20), apellido_Cliente VARCHAR(20), direccion VARCHAR(50), correo VARCHAR(50))")

# Crear tabla producto
cursor.execute("""CREATE TABLE IF NOT EXISTS producto(
    id_Producto INTEGER PRIMARY KEY AUTOINCREMENT, 
    id_Categoria INTEGER,
    precio FLOAT,
    stock INTEGER,
    FOREIGN KEY (id_Categoria) REFERENCES categoria(id_Categoria)
)""")

# Crear tabla pedido (debe ir al final porque referencia a cliente y producto)
cursor.execute("""CREATE TABLE IF NOT EXISTS pedido(
    id_Pedido INTEGER PRIMARY KEY AUTOINCREMENT, 
    id_Cliente INTEGER,
    id_Producto INTEGER,
    fecha_Pedido DATE,
    cantidad INTEGER,
    precio_Total FLOAT,
    FOREIGN KEY (id_Cliente) REFERENCES cliente(id_Cliente),
    FOREIGN KEY (id_Producto) REFERENCES producto(id_Producto)
)""")

cursor.execute("SELECT COUNT(*) FROM categoria")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO categoria (nombre_Categoria) VALUES ('Frutas')")
    cursor.execute("INSERT INTO categoria (nombre_Categoria) VALUES ('Lacteos')")
    cursor.execute("INSERT INTO categoria (nombre_Categoria) VALUES ('Carnes')")
    
    cursor.execute("INSERT INTO cliente (nombre_Cliente, apellido_Cliente, direccion, correo) VALUES ('Juan', 'Perez', 'Calle Mayor 10', 'juan@email.com')")
    cursor.execute("INSERT INTO cliente (nombre_Cliente, apellido_Cliente, direccion, correo) VALUES ('Maria', 'Garcia', 'Avenida Sol 25', 'maria@email.com')")
    cursor.execute("INSERT INTO cliente (nombre_Cliente, apellido_Cliente, direccion, correo) VALUES ('Carlos', 'Lopez', 'Plaza Luna 5', 'carlos@email.com')")
    
    cursor.execute("INSERT INTO producto (id_Categoria, precio, stock) VALUES (1, 2.50, 100)")
    cursor.execute("INSERT INTO producto (id_Categoria, precio, stock) VALUES (2, 1.80, 50)")
    cursor.execute("INSERT INTO producto (id_Categoria, precio, stock) VALUES (3, 8.99, 30)")
    
    cursor.execute("INSERT INTO pedido (id_Cliente, id_Producto, fecha_Pedido, cantidad, precio_Total) VALUES (1, 1, '2025-12-11', 5, 12.50)")
    cursor.execute("INSERT INTO pedido (id_Cliente, id_Producto, fecha_Pedido, cantidad, precio_Total) VALUES (2, 2, '2025-12-11', 3, 5.40)")
    cursor.execute("INSERT INTO pedido (id_Cliente, id_Producto, fecha_Pedido, cantidad, precio_Total) VALUES (3, 3, '2025-12-10', 2, 17.98)")

# Guardar cambios
conexion.commit()

# Crear Notebook para pestañas (tabs)
notebook = ttk.Notebook(raiz)
notebook.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=10, pady=10)

# Configurar que la fila 1 se expanda
raiz.grid_rowconfigure(1, weight=1)


def LeerBaseDatos():
    # ============================================================================
    # PARTE DINÁMICA: Obtener todas las tablas y mostrarlas automáticamente
    # ============================================================================

    # 1. Obtener todas las tablas de la base de datos (excepto las tablas del sistema de SQLite)
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)
    tablas = cursor.fetchall()  # Devuelve una lista de tuplas: [('categoria',), ('cliente',), ...]

    # 2. Para cada tabla encontrada, crear una pestaña con su Treeview
    for tabla_tupla in tablas:
        nombre_tabla = tabla_tupla[0]  # Extraer el nombre de la tabla de la tupla
        
        # 3. Obtener las columnas de esta tabla usando PRAGMA
        cursor.execute(f"PRAGMA table_info({nombre_tabla})")
        info_columnas = cursor.fetchall()  # Devuelve info de cada columna
        # info_columnas es algo como: [(0, 'id_Categoria', 'INTEGER', 0, None, 1), (1, 'nombre_Categoria', 'VARCHAR(20)', 0, None, 0)]
        
        # Extraer solo los nombres de las columnas (índice 1 de cada tupla)
        nombres_columnas = [col[1] for col in info_columnas]
        
        # 4. Crear el frame para esta tabla
        frame = tkinter.Frame(notebook)
        notebook.add(frame, text=nombre_tabla.capitalize())  # Añadir pestaña con nombre de tabla
        
        # 5. Crear el Treeview con las columnas dinámicas
        tree = ttk.Treeview(frame, columns=nombres_columnas, show="headings")
        
        # 6. Configurar los encabezados de las columnas
        for columna in nombres_columnas:
            tree.heading(columna, text=columna)  # Poner el nombre de la columna como encabezado
            tree.column(columna, width=100)  # Opcional: ajustar ancho
        
        tree.pack(fill="both", expand=True)
        
        # 7. Cargar los datos de la tabla
        cursor.execute(f"SELECT * FROM {nombre_tabla}")
        filas = cursor.fetchall()
        
        for fila in filas:
            tree.insert("", "end", values=fila)





LeerBaseDatos()
raiz.mainloop()

# Cerrar conexión al finalizar
conexion.close()