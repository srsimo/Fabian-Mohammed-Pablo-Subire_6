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
    # Función interna para insertar datos (VENTANA 3)
    def abrir_ventana_insertar_datos(nombre_tabla, campos_info, ventana_anterior):
        ventana_anterior.destroy()
        
        ventana_datos = tkinter.Toplevel(raiz)
        ventana_datos.title(f"Insertar datos en {nombre_tabla}")
        ventana_datos.geometry("500x600")
        
        titulo = tkinter.Label(ventana_datos, text=f"Insertar datos en: {nombre_tabla}", font=('arial', 14, 'bold'))
        titulo.pack(pady=10)
        
        frame_scroll = tkinter.Frame(ventana_datos)
        frame_scroll.pack(fill="both", expand=True, padx=20, pady=10)
        
        canvas = tkinter.Canvas(frame_scroll)
        scrollbar = tkinter.Scrollbar(frame_scroll, orient="vertical", command=canvas.yview)
        frame_datos = tkinter.Frame(canvas)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=frame_datos, anchor="nw")
        
        datos_entries = []
        
        # Crear inputs para cada campo (excepto el ID que es autoincremental)
        for i, campo_info in enumerate(campos_info):
            frame_dato = tkinter.Frame(frame_datos, relief="groove", bd=2)
            frame_dato.pack(fill="x", padx=10, pady=5)
            
            tkinter.Label(frame_dato, text=f"{campo_info['nombre']} ({campo_info['tipo']}):", font=('arial', 11, 'bold')).pack(pady=5)
            
            entry_dato = tkinter.Entry(frame_dato, width=40, font=('arial', 10))
            entry_dato.pack(pady=5, padx=10)
            
            datos_entries.append(entry_dato)
        
        frame_datos.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        
        def insertar_datos():
            valores = []
            for i, entry in enumerate(datos_entries):
                valor = entry.get().strip()
                # Permitir campos vacíos para tipos que lo permitan
                valores.append(valor if valor else None)
            
            # Construir INSERT
            columnas = ", ".join([c['nombre'] for c in campos_info])
            placeholders = ", ".join(["?" for _ in valores])
            sql = f"INSERT INTO {nombre_tabla} ({columnas}) VALUES ({placeholders})"
            
            try:
                cursor.execute(sql, valores)
                conexion.commit()
                print(f"Datos insertados en '{nombre_tabla}' exitosamente")
                
                # Limpiar los campos para permitir insertar más registros
                for entry in datos_entries:
                    entry.delete(0, 'end')
                
                print("Puedes insertar otro registro o cerrar la ventana")
            except Exception as e:
                print(f"Error al insertar: {e}")
        
        def finalizar():
            ventana_datos.destroy()
            LeerBaseDatos()
        
        # Botones
        frame_botones = tkinter.Frame(ventana_datos)
        frame_botones.pack(pady=10)
        
        btn_insertar = tkinter.Button(frame_botones, text="Insertar Registro", command=insertar_datos, bg="green", fg="white", font=('arial', 12))
        btn_insertar.pack(side="left", padx=5)
        
        btn_finalizar = tkinter.Button(frame_botones, text="Finalizar", command=finalizar, bg="blue", fg="white", font=('arial', 12))
        btn_finalizar.pack(side="left", padx=5)
    
    # Función interna para la segunda ventana (VENTANA 2)
    def abrir_ventana_campos(nombre_tabla, num_campos, ventana_anterior):
        ventana_anterior.destroy()  
        
        ventana_campos = tkinter.Toplevel(raiz)
        ventana_campos.title(f"Configurar campos para {nombre_tabla}")
        ventana_campos.geometry("500x600")
        
        titulo = tkinter.Label(ventana_campos, text=f"Tabla: {nombre_tabla} - {num_campos} campos", font=('arial', 14, 'bold'))
        titulo.pack(pady=10)
        
        frame_scroll = tkinter.Frame(ventana_campos)
        frame_scroll.pack(fill="both", expand=True, padx=20, pady=10)
        
        canvas = tkinter.Canvas(frame_scroll)
        scrollbar = tkinter.Scrollbar(frame_scroll, orient="vertical", command=canvas.yview)
        frame_campos = tkinter.Frame(canvas)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=frame_campos, anchor="nw")
        
        campos_entries = []
        
        for i in range(num_campos):
            frame_campo = tkinter.Frame(frame_campos, relief="groove", bd=2)
            frame_campo.pack(fill="x", padx=10, pady=5)
            
            tkinter.Label(frame_campo, text=f"Campo {i+1}:", font=('arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=5)
            
            tkinter.Label(frame_campo, text="Nombre del campo:").grid(row=1, column=0, sticky="e", padx=5, pady=2)
            entry_nombre = tkinter.Entry(frame_campo, width=30)
            entry_nombre.grid(row=1, column=1, padx=5, pady=2)
            
            tkinter.Label(frame_campo, text="Tipo del campo:").grid(row=2, column=0, sticky="e", padx=5, pady=2)
            combo_tipo = ttk.Combobox(frame_campo, width=28, state="readonly")
            combo_tipo['values'] = ('INTEGER', 'TEXT', 'REAL', 'BLOB', 'VARCHAR(50)', 'DATE', 'FLOAT')
            combo_tipo.current(0)
            combo_tipo.grid(row=2, column=1, padx=5, pady=2)
            
            campos_entries.append({'nombre': entry_nombre, 'tipo': combo_tipo})
        
        frame_campos.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        
        def crear_tabla_bd():
            campos_sql = [f"id_{nombre_tabla} INTEGER PRIMARY KEY AUTOINCREMENT"]
            campos_info = []  # Guardar info de campos para la siguiente ventana
            
            for i, campo in enumerate(campos_entries):
                nombre = campo['nombre'].get().strip()
                tipo = campo['tipo'].get()
                
                if not nombre:
                    print(f"Error: Campo {i+1} sin nombre")
                    return
                
                palabras_reservadas = ['as', 'select', 'from', 'where', 'table', 'order', 'group', 'by', 'create', 'insert', 'update', 'delete']
                if nombre.lower() in palabras_reservadas:
                    print(f"Error: '{nombre}' es una palabra reservada")
                    return
                
                campos_sql.append(f"{nombre} {tipo}")
                campos_info.append({'nombre': nombre, 'tipo': tipo})
            
            # CAMBIAR: usar CREATE TABLE (sin IF NOT EXISTS para evitar conflictos)
            sql = f"CREATE TABLE {nombre_tabla} ({', '.join(campos_sql)})"
            
            try:
                cursor.execute(sql)
                conexion.commit()
                print(f"Tabla '{nombre_tabla}' creada exitosamente")
                # Abrir ventana para insertar datos
                abrir_ventana_insertar_datos(nombre_tabla, campos_info, ventana_campos)
            except Exception as e:
                print(f"Error al crear tabla: {e}")
                if "already exists" in str(e):
                    print(f"La tabla '{nombre_tabla}' ya existe. Usa otro nombre.")
        
        # BOTÓN CREAR TABLA
        btn_crear = tkinter.Button(ventana_campos, text="Crear Tabla", command=crear_tabla_bd, bg="green", fg="white", font=('arial', 12))
        btn_crear.pack(pady=10)
    
    # PRIMERA VENTANA
    ventana_inicial = tkinter.Toplevel(raiz)
    ventana_inicial.title("Crear Nueva Tabla")
    ventana_inicial.geometry("400x300")
    
    titulo = tkinter.Label(ventana_inicial, text="Crear Nueva Tabla", font=('arial', 16, 'bold'))
    titulo.pack(pady=20)
    
    frame_inputs = tkinter.Frame(ventana_inicial)
    frame_inputs.pack(pady=20)
    
    tkinter.Label(frame_inputs, text="Nombre de la tabla:", font=('arial', 12)).grid(row=0, column=0, sticky="e", padx=10, pady=10)
    entry_nombre_tabla = tkinter.Entry(frame_inputs, width=20, font=('arial', 12))
    entry_nombre_tabla.grid(row=0, column=1, padx=10, pady=10)
    
    tkinter.Label(frame_inputs, text="Cantidad de campos:", font=('arial', 12)).grid(row=1, column=0, sticky="e", padx=10, pady=10)
    entry_num_campos = tkinter.Entry(frame_inputs, width=20, font=('arial', 12))
    entry_num_campos.grid(row=1, column=1, padx=10, pady=10)
    
    def continuar():
        nombre_tabla = entry_nombre_tabla.get().strip()
        num_campos_str = entry_num_campos.get().strip()
        
        if not nombre_tabla:
            print("Error: Ingresa un nombre para la tabla")
            return
        
        if not num_campos_str.isdigit() or int(num_campos_str) <= 0:
            print("Error: Cantidad debe ser un número mayor a 0")
            return
        
        abrir_ventana_campos(nombre_tabla, int(num_campos_str), ventana_inicial)
    
    # BOTÓN CONTINUAR
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
    # LIMPIAR PESTAÑAS EXISTENTES ANTES DE CARGAR
    for tab in notebook.tabs():
        notebook.forget(tab)
    
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