# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 17:57:50 2025
@author: Pablo, Adrian Subire, Mohammed, Fabian
"""
import sqlite3
import tkinter as tkinter
from tkinter import ttk, messagebox

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
    """
    Función principal que inicia el proceso de edición de registros
    """
    # Ventana 1: Seleccionar tabla
    ventana_tabla = tkinter.Toplevel(raiz)
    ventana_tabla.title("Editar - Seleccionar Tabla")
    ventana_tabla.geometry("400x250")
    ventana_tabla.grab_set()  # Hacer la ventana modal
    
    # Obtener lista de tablas
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)
    tablas = [tabla[0] for tabla in cursor.fetchall()]
    
    label_titulo = tkinter.Label(ventana_tabla, text="Seleccione la tabla a editar:", font=('Arial', 12))
    label_titulo.pack(pady=20)
    
    combo_tabla = ttk.Combobox(ventana_tabla, values=tablas, state="readonly", font=('Arial', 11), width=25)
    combo_tabla.pack(pady=10)
    if tablas:
        combo_tabla.current(0)
    
    def continuar_con_id():
        if not combo_tabla.get():
            messagebox.showerror("Error", "Debe seleccionar una tabla")
            return
        
        tabla_seleccionada = combo_tabla.get()
        ventana_tabla.destroy()
        solicitar_primary_key(tabla_seleccionada)
    
    boton_siguiente = tkinter.Button(ventana_tabla, text="Siguiente", command=continuar_con_id, 
                   bg="dodgerblue", fg="white", font=('Arial', 12), width=15, height=2)
    boton_siguiente.pack(pady=30)
    
    ventana_tabla.bind('<Return>', lambda event: continuar_con_id())


def solicitar_primary_key(tabla):
    """
    Ventana 2: Solicita el ID (Primary Key) del registro a editar
    """
    ventana_id = tkinter.Toplevel(raiz)
    ventana_id.title("Editar - Ingresar ID")
    ventana_id.geometry("400x250")
    ventana_id.grab_set()
    
    # Obtener el nombre de la columna primary key
    cursor.execute(f"PRAGMA table_info({tabla})")
    columnas_info = cursor.fetchall()
    pk_columna = None
    for col in columnas_info:
        if col[5] == 1:  # El índice 5 indica si es primary key
            pk_columna = col[1]
            break
    
    label_instruccion = tkinter.Label(ventana_id, text=f"Ingrese el {pk_columna} del registro a editar:", 
                  font=('Arial', 12))
    label_instruccion.pack(pady=20)
    
    entrada_id = tkinter.Entry(ventana_id, font=('Arial', 11), width=20)
    entrada_id.pack(pady=10)
    entrada_id.focus()
    
    def verificar_y_continuar():
        id_valor = entrada_id.get().strip()
        
        # Validar que se ingresó algo
        if not id_valor:
            messagebox.showerror("Error", "Debe ingresar un ID")
            return
        
        # Validar que sea un número entero
        try:
            id_int = int(id_valor)
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número entero")
            return
        
        # Verificar que el registro existe
        cursor.execute(f"SELECT * FROM {tabla} WHERE {pk_columna} = ?", (id_int,))
        registro = cursor.fetchone()
        
        if registro is None:
            messagebox.showerror("Error", f"No existe ningún registro con {pk_columna} = {id_int}")
            return
        
        # Si todo está bien, continuar
        ventana_id.destroy()
        seleccionar_campo(tabla, pk_columna, id_int, registro)
    
    boton_siguiente = tkinter.Button(ventana_id, text="Siguiente", command=verificar_y_continuar,
                   bg="dodgerblue", fg="white", font=('Arial', 12), width=15, height=2)
    boton_siguiente.pack(pady=30)
    
    ventana_id.bind('<Return>', lambda event: verificar_y_continuar())


def seleccionar_campo(tabla, pk_columna, pk_valor, registro):
    """
    Ventana 3: Permite seleccionar qué campo se desea editar
    """
    ventana_campo = tkinter.Toplevel(raiz)
    ventana_campo.title("Editar - Seleccionar Campo")
    ventana_campo.geometry("500x400")
    ventana_campo.grab_set()
    
    # Obtener información de las columnas
    cursor.execute(f"PRAGMA table_info({tabla})")
    columnas_info = cursor.fetchall()
    
    # Filtrar para no permitir editar la primary key
    campos_editables = []
    valores_actuales = {}
    
    for i, col in enumerate(columnas_info):
        nombre_col = col[1]
        if col[5] != 1:  # No es primary key
            campos_editables.append(nombre_col)
            valores_actuales[nombre_col] = registro[i]
    
    label_registro = tkinter.Label(ventana_campo, text=f"Registro actual ({pk_columna} = {pk_valor}):", 
                  font=('Arial', 12, 'bold'))
    label_registro.pack(pady=10)
    
    # Mostrar valores actuales
    frame_valores = tkinter.Frame(ventana_campo)
    frame_valores.pack(pady=10)
    
    for campo in campos_editables:
        label_campo = tkinter.Label(frame_valores, text=f"{campo}: {valores_actuales[campo]}", 
                     font=('Arial', 10))
        label_campo.pack(anchor='w', padx=20)
    
    label_seleccion = tkinter.Label(ventana_campo, text="Seleccione el campo a editar:", 
                  font=('Arial', 11))
    label_seleccion.pack(pady=15)
    
    combo_campo = ttk.Combobox(ventana_campo, values=campos_editables, 
                               state="readonly", font=('Arial', 11), width=25)
    combo_campo.pack(pady=10)
    if campos_editables:
        combo_campo.current(0)
    
    def continuar_con_campo():
        if not combo_campo.get():
            messagebox.showerror("Error", "Debe seleccionar un campo")
            return
        
        campo_seleccionado = combo_campo.get()
        
        # Obtener el tipo de dato del campo
        tipo_dato = None
        for col in columnas_info:
            if col[1] == campo_seleccionado:
                tipo_dato = col[2]
                break
        
        ventana_campo.destroy()
        ingresar_nuevo_valor(tabla, pk_columna, pk_valor, campo_seleccionado, 
                            valores_actuales[campo_seleccionado], tipo_dato)
    
    boton_siguiente = tkinter.Button(ventana_campo, text="Siguiente", command=continuar_con_campo,
                   bg="dodgerblue", fg="white", font=('Arial', 12), width=15, height=2)
    boton_siguiente.pack(pady=30)
    
    ventana_campo.bind('<Return>', lambda event: continuar_con_campo())


def ingresar_nuevo_valor(tabla, pk_columna, pk_valor, campo, valor_actual, tipo_dato):
    """
    Ventana 4: Permite ingresar el nuevo valor para el campo seleccionado
    """
    ventana_valor = tkinter.Toplevel(raiz)
    ventana_valor.title("Editar - Nuevo Valor")
    ventana_valor.geometry("450x300")
    ventana_valor.grab_set()
    
    label_campo = tkinter.Label(ventana_valor, text=f"Campo: {campo}", 
                  font=('Arial', 11, 'bold'))
    label_campo.pack(pady=10)
    
    label_actual = tkinter.Label(ventana_valor, text=f"Valor actual: {valor_actual}", 
                  font=('Arial', 10))
    label_actual.pack(pady=5)
    
    label_tipo = tkinter.Label(ventana_valor, text=f"Tipo de dato: {tipo_dato}", 
                  font=('Arial', 9, 'italic'))
    label_tipo.pack(pady=5)
    
    label_instruccion = tkinter.Label(ventana_valor, text="Ingrese el nuevo valor:", 
                  font=('Arial', 11))
    label_instruccion.pack(pady=10)
    
    entrada_valor = tkinter.Entry(ventana_valor, font=('Arial', 11), width=30)
    entrada_valor.pack(pady=10)
    entrada_valor.focus()
    
    def guardar_cambio():
        nuevo_valor = entrada_valor.get().strip()
        
        if not nuevo_valor:
            messagebox.showerror("Error", "Debe ingresar un valor")
            return
        
        # Validar según el tipo de dato
        try:
            if 'INT' in tipo_dato.upper():
                nuevo_valor = int(nuevo_valor)
            elif 'FLOAT' in tipo_dato.upper() or 'REAL' in tipo_dato.upper():
                nuevo_valor = float(nuevo_valor)
            # Para VARCHAR, DATE, etc., mantener como string
            
            # Realizar la actualización en la base de datos
            cursor.execute(f"UPDATE {tabla} SET {campo} = ? WHERE {pk_columna} = ?", 
                          (nuevo_valor, pk_valor))
            conexion.commit()
            
            ventana_valor.destroy()
            mostrar_exito(tabla)
            
        except ValueError:
            messagebox.showerror("Error", 
                f"El valor ingresado no es válido para el tipo {tipo_dato}")
        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", 
                f"No se pudo realizar la actualización: {str(e)}")
    
    boton_guardar = tkinter.Button(ventana_valor, text="Guardar", command=guardar_cambio,
                   bg="green", fg="white", font=('Arial', 12), width=15, height=2)
    boton_guardar.pack(pady=30)
    
    ventana_valor.bind('<Return>', lambda event: guardar_cambio())


def mostrar_exito(tabla):
    """
    Ventana 5: Muestra mensaje de éxito y actualiza la vista
    """
    ventana_exito = tkinter.Toplevel(raiz)
    ventana_exito.title("Éxito")
    ventana_exito.geometry("350x200")
    ventana_exito.grab_set()
    
    label_exito = tkinter.Label(ventana_exito, text="✓ Modificación realizada con éxito", 
                  font=('Arial', 12, 'bold'), fg="green")
    label_exito.pack(pady=40)
    
    def cerrar_y_actualizar():
        ventana_exito.destroy()
        LeerBaseDatos()  # Actualizar la vista de datos
    
    boton_aceptar = tkinter.Button(ventana_exito, text="Aceptar", command=cerrar_y_actualizar,
                   bg="dodgerblue", fg="white", font=('Arial', 12), width=15, height=2)
    boton_aceptar.pack(pady=20)
    
    ventana_exito.bind('<Return>', lambda event: cerrar_y_actualizar())
    
    
    
    
    
    
    
    
    
def BuscarTabla():
    print("Ejemplo")


textoCrear = "Crear"
botonCrear = tkinter.Button(raiz, text=textoCrear, command=CrearTabla, relief="solid", bd=1, highlightbackground="black", highlightthickness=1)
botonCrear.grid(row=0, column=0, sticky="ew")
botonCrear.config(fg="white", bg="dodgerblue", font=('arial',15))

textoBorrar = "Eliminar"
botonBorrar = tkinter.Button(raiz, text=textoBorrar,  command=BorrarTabla,relief="solid", bd=1, highlightbackground="black", highlightthickness=1)
botonBorrar.grid(row=0, column=1, sticky="ew")
botonBorrar.config(fg="white", bg="dodgerblue", font=('arial',15))

textoEditar = "Editar"
botonEditar = tkinter.Button(raiz, text=textoEditar, command=EditarTabla, relief="solid", bd=1, highlightbackground="black", highlightthickness=1)
botonEditar.grid(row=0, column=2, sticky="ew")
botonEditar.config(fg="white", bg="dodgerblue", font=('arial',15))

textoBuscar = "Buscar"
botonBuscar = tkinter.Button(raiz, text=textoBuscar,  command=BuscarTabla,relief="solid", bd=1, highlightbackground="black", highlightthickness=1)
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