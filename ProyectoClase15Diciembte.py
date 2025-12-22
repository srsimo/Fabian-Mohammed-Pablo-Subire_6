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


def CrearTabla():
    # Función para la segunda ventana: configurar los campos
    def abrir_ventana_campos(nombre_tabla, num_campos, ventana_anterior):
        ventana_anterior.destroy()  # Cerrar la ventana anterior
        
        # Crear ventana para configurar campos
        ventana_campos = tkinter.Toplevel(raiz)
        ventana_campos.title(f"Configurar campos para {nombre_tabla}")
        ventana_campos.geometry("500x600")
        
        # Título
        titulo = tkinter.Label(ventana_campos, text=f"Tabla: {nombre_tabla} - {num_campos} campos", font=('arial', 14, 'bold'))
        titulo.pack(pady=10)
        
        # Frame con scroll para los campos
        frame_scroll = tkinter.Frame(ventana_campos)
        frame_scroll.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Canvas y scrollbar
        canvas = tkinter.Canvas(frame_scroll)
        scrollbar = tkinter.Scrollbar(frame_scroll, orient="vertical", command=canvas.yview)
        frame_campos = tkinter.Frame(canvas)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=frame_campos, anchor="nw")
        
        # Lista para guardar los entries de cada campo
        campos_entries = []
        
        # Crear inputs para cada campo
        for i in range(num_campos):
            # Frame para cada campo
            frame_campo = tkinter.Frame(frame_campos, relief="groove", bd=2)
            frame_campo.pack(fill="x", padx=10, pady=5)
            
            # Etiqueta del número de campo
            tkinter.Label(frame_campo, text=f"Campo {i+1}:", font=('arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=5)
            
            # Nombre del campo
            tkinter.Label(frame_campo, text="Nombre del campo:").grid(row=1, column=0, sticky="e", padx=5, pady=2)
            entry_nombre = tkinter.Entry(frame_campo, width=30)
            entry_nombre.grid(row=1, column=1, padx=5, pady=2)
            
            # Tipo del campo
            tkinter.Label(frame_campo, text="Tipo del campo:").grid(row=2, column=0, sticky="e", padx=5, pady=2)
            combo_tipo = ttk.Combobox(frame_campo, width=28, state="readonly")
            combo_tipo['values'] = ('INTEGER', 'TEXT', 'REAL', 'BLOB', 'VARCHAR(50)', 'DATE', 'FLOAT')
            combo_tipo.current(0)
            combo_tipo.grid(row=2, column=1, padx=5, pady=2)
            
            # Guardar referencias
            campos_entries.append({
                'nombre': entry_nombre,
                'tipo': combo_tipo
            })
        
        # Actualizar scroll region
        frame_campos.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        
        # Función para crear la tabla en la BD
        def crear_tabla_bd():
            # Construir la sentencia SQL
            campos_sql = []
            for i, campo in enumerate(campos_entries):
                nombre = campo['nombre'].get().strip()
                tipo = campo['tipo'].get()
                
                if not nombre:
                    print(f"Error: Campo {i+1} sin nombre")
                    return
                
                campos_sql.append(f"{nombre} {tipo}")
            
            # Crear sentencia CREATE TABLE
            sql = f"CREATE TABLE IF NOT EXISTS {nombre_tabla} ({', '.join(campos_sql)})"
            
            try:
                cursor.execute(sql)
                conexion.commit()
                print(f"Tabla '{nombre_tabla}' creada exitosamente")
                ventana_campos.destroy()
                LeerBaseDatos()  # Actualizar la vista
            except Exception as e:
                print(f"Error al crear tabla: {e}")
        
        # Botón para crear la tabla
        btn_crear = tkinter.Button(ventana_campos, text="Crear Tabla", command=crear_tabla_bd, bg="green", fg="white", font=('arial', 12))
        btn_crear.pack(pady=10)
    
    # Crear ventana inicial
    ventana_inicial = tkinter.Toplevel(raiz)
    ventana_inicial.title("Crear Nueva Tabla")
    ventana_inicial.geometry("400x250")
    
    # Título
    titulo = tkinter.Label(ventana_inicial, text="Crear Nueva Tabla", font=('arial', 16, 'bold'))
    titulo.pack(pady=20)
    
    # Frame para los inputs
    frame_inputs = tkinter.Frame(ventana_inicial)
    frame_inputs.pack(pady=20)
    
    # Nombre de la tabla
    tkinter.Label(frame_inputs, text="Nombre de la tabla:", font=('arial', 12)).grid(row=0, column=0, sticky="e", padx=10, pady=10)
    entry_nombre_tabla = tkinter.Entry(frame_inputs, width=20, font=('arial', 12))
    entry_nombre_tabla.grid(row=0, column=1, padx=10, pady=10)
    
    # Cantidad de campos
    tkinter.Label(frame_inputs, text="Cantidad de campos:", font=('arial', 12)).grid(row=1, column=0, sticky="e", padx=10, pady=10)
    entry_num_campos = tkinter.Entry(frame_inputs, width=20, font=('arial', 12))
    entry_num_campos.grid(row=1, column=1, padx=10, pady=10)
    
    # Función para validar y continuar
    def continuar():
        nombre_tabla = entry_nombre_tabla.get().strip()
        num_campos_str = entry_num_campos.get().strip()
        
        if not nombre_tabla:
            print("Error: Debes ingresar un nombre para la tabla")
            return
        
        if not num_campos_str.isdigit() or int(num_campos_str) <= 0:
            print("Error: La cantidad de campos debe ser un número mayor a 0")
            return
        
        num_campos = int(num_campos_str)
        abrir_ventana_campos(nombre_tabla, num_campos, ventana_inicial)
    
    # Botón continuar
    btn_continuar = tkinter.Button(ventana_inicial, text="Continuar", command=continuar, bg="dodgerblue", fg="white", font=('arial', 12))
    btn_continuar.pack(pady=10)
    
    
    
    
    
    




def BorrarTabla():
    print("Ejemplo")





def EditarTabla():
    print("Ejemplo")
    
    
    
    
    
    
    
    
    
def BuscarTabla():
    print("Ejemplo")


textoCrear = "Crear"
botonCrear = tkinter.Button(raiz, text=textoCrear, command=CrearTabla, relief="solid", bd=1, highlightbackground="black", highlightthickness=1)
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