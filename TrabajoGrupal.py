# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 17:57:50 2025
<<<<<<< HEAD
@author: pablo, subire, Mohammed, Fabian
>>>>>>> 3ef513525c0a4c72ed2d644575e08bf105a20951
"""
import sqlite3
import tkinter as tkinter

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

# Guardar cambios
conexion.commit()

raiz.mainloop()

# Cerrar conexión al finalizar
conexion.close()