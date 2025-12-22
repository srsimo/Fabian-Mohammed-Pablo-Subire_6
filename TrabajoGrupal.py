# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 17:57:50 2025
<<<<<<< HEAD
@author: Pablo, Adrian Subire, Mohammed, Fabian
>>>>>>> 3ef513525c0a4c72ed2d644575e08bf105a20951
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

# TABLA CATEGORIA
frame_categoria = tkinter.Frame(notebook)
notebook.add(frame_categoria, text="Categoría")

tree_categoria = ttk.Treeview(frame_categoria, columns=("ID", "Nombre"), show="headings")
tree_categoria.heading("ID", text="ID Categoría")
tree_categoria.heading("Nombre", text="Nombre Categoría")
tree_categoria.pack(fill="both", expand=True)

cursor.execute("SELECT * FROM categoria")
for row in cursor.fetchall():
    tree_categoria.insert("", "end", values=row)

# TABLA CLIENTE
frame_cliente = tkinter.Frame(notebook)
notebook.add(frame_cliente, text="Cliente")

tree_cliente = ttk.Treeview(frame_cliente, columns=("ID", "Nombre", "Apellido", "Dirección", "Correo"), show="headings")
tree_cliente.heading("ID", text="ID Cliente")
tree_cliente.heading("Nombre", text="Nombre")
tree_cliente.heading("Apellido", text="Apellido")
tree_cliente.heading("Dirección", text="Dirección")
tree_cliente.heading("Correo", text="Correo")
tree_cliente.pack(fill="both", expand=True)

cursor.execute("SELECT * FROM cliente")
for row in cursor.fetchall():
    tree_cliente.insert("", "end", values=row)

# TABLA PRODUCTO
frame_producto = tkinter.Frame(notebook)
notebook.add(frame_producto, text="Producto")

tree_producto = ttk.Treeview(frame_producto, columns=("ID", "ID Categoría", "Precio", "Stock"), show="headings")
tree_producto.heading("ID", text="ID Producto")
tree_producto.heading("ID Categoría", text="ID Categoría")
tree_producto.heading("Precio", text="Precio")
tree_producto.heading("Stock", text="Stock")
tree_producto.pack(fill="both", expand=True)

cursor.execute("SELECT * FROM producto")
for row in cursor.fetchall():
    tree_producto.insert("", "end", values=row)

# TABLA PEDIDO
frame_pedido = tkinter.Frame(notebook)
notebook.add(frame_pedido, text="Pedido")

tree_pedido = ttk.Treeview(frame_pedido, columns=("ID", "ID Cliente", "ID Producto", "Fecha", "Cantidad", "Precio Total"), show="headings")
tree_pedido.heading("ID", text="ID Pedido")
tree_pedido.heading("ID Cliente", text="ID Cliente")
tree_pedido.heading("ID Producto", text="ID Producto")
tree_pedido.heading("Fecha", text="Fecha")
tree_pedido.heading("Cantidad", text="Cantidad")
tree_pedido.heading("Precio Total", text="Precio Total")
tree_pedido.pack(fill="both", expand=True)

cursor.execute("SELECT * FROM pedido")
for row in cursor.fetchall():
    tree_pedido.insert("", "end", values=row)

raiz.mainloop()

# Cerrar conexión al finalizar
conexion.close()