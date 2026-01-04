# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 17:57:50 2025
@author: Pablo, Adrian Subire, Mohammed, Fabian
"""

trees_por_tabla = {}
import sqlite3
import tkinter as tkinter
from tkinter import ttk, messagebox, PhotoImage

raiz = tkinter.Tk()
raiz.title("UDUU")
raiz.geometry("800x600")


import os

try:
    ruta_logo = os.path.join(os.path.dirname(__file__), "logo.png")
    icono = PhotoImage(file=ruta_logo)
    raiz.iconphoto(True, icono)
except Exception as e:
    print("No se pudo cargar el icono:", e)

# Configurar que las columnas se expandan proporcionalmente
raiz.grid_columnconfigure(0, weight=1)
raiz.grid_columnconfigure(1, weight=1)
raiz.grid_columnconfigure(2, weight=1)
raiz.grid_columnconfigure(3, weight=1)
raiz.grid_columnconfigure(4, weight=1)


def CrearTabla():
    # VENTANA INICIAL: Elegir entre crear tabla, añadir registro o añadir campo
    ventana_seleccion = tkinter.Toplevel(raiz)
    ventana_seleccion.title("Crear")
    ventana_seleccion.geometry("450x400")
    ventana_seleccion.grab_set()
    
    
    titulo = tkinter.Label(ventana_seleccion, text="¿Qué desea crear?", font=('arial', 16, 'bold'))
    titulo.pack(pady=30)
    
    def crear_nueva_tabla():
        ventana_seleccion.destroy()
        ventana_crear_tabla()
    
    def añadir_registro():
        ventana_seleccion.destroy()
        ventana_seleccionar_tabla_registro()
    
    def añadir_campo():
        ventana_seleccion.destroy()
        ventana_seleccionar_tabla_campo()
    
    # Botones
    frame_botones = tkinter.Frame(ventana_seleccion)
    frame_botones.pack(pady=10)
    
    btn_tabla = tkinter.Button(frame_botones, text="Crear Nueva Tabla", 
                               command=crear_nueva_tabla,
                               bg="green", fg="white", 
                               font=('arial', 12), width=25, height=2)
    btn_tabla.pack(pady=8)
    
    btn_registro = tkinter.Button(frame_botones, text="Añadir Registro", 
                                  command=añadir_registro,
                                  bg="blue", fg="white", 
                                  font=('arial', 12), width=25, height=2)
    btn_registro.pack(pady=8)
    
    btn_campo = tkinter.Button(frame_botones, text="Añadir Campo a Tabla", 
                               command=añadir_campo,
                               bg="orange", fg="white", 
                               font=('arial', 12), width=25, height=2)
    btn_campo.pack(pady=8)
    
    # ============================================================================
    # OPCIÓN 1: CREAR NUEVA TABLA
    # ============================================================================
    
    def ventana_crear_tabla():
        """Primera ventana para crear tabla"""
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
                messagebox.showerror("Error", "Ingresa un nombre para la tabla")
                return
            
            if not num_campos_str.isdigit() or int(num_campos_str) <= 0:
                messagebox.showerror("Error", "La cantidad debe ser un número mayor a 0")
                return
            
            abrir_ventana_campos(nombre_tabla, int(num_campos_str), ventana_inicial)
        
        btn_continuar = tkinter.Button(ventana_inicial, text="Continuar", command=continuar, bg="dodgerblue", fg="white", font=('arial', 12))
        btn_continuar.pack(pady=10)
    
    def abrir_ventana_campos(nombre_tabla, num_campos, ventana_anterior):
        """Segunda ventana: configurar campos"""
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
            campos_info = []
            
            for i, campo in enumerate(campos_entries):
                nombre = campo['nombre'].get().strip()
                tipo = campo['tipo'].get()
                
                if not nombre:
                    messagebox.showerror("Error", f"Campo {i+1} sin nombre")
                    return
                
                palabras_reservadas = ['as', 'select', 'from', 'where', 'table', 'order', 'group', 'by', 'create', 'insert', 'update', 'delete']
                if nombre.lower() in palabras_reservadas:
                    messagebox.showerror("Error", f"'{nombre}' es una palabra reservada")
                    return
                
                campos_sql.append(f"{nombre} {tipo}")
                campos_info.append({'nombre': nombre, 'tipo': tipo})
            
            sql = f"CREATE TABLE {nombre_tabla} ({', '.join(campos_sql)})"
            
            try:
                cursor.execute(sql)
                conexion.commit()
                messagebox.showinfo("Éxito", f"Tabla '{nombre_tabla}' creada exitosamente")
                ventana_campos.destroy()
                LeerBaseDatos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear la tabla: {e}")
        
        btn_crear = tkinter.Button(ventana_campos, text="Crear Tabla", command=crear_tabla_bd, bg="green", fg="white", font=('arial', 12))
        btn_crear.pack(pady=10)
    
    # ============================================================================
    # OPCIÓN 2: AÑADIR REGISTRO A TABLA EXISTENTE
    # ============================================================================
    
    def ventana_seleccionar_tabla_registro():
        """Primera ventana: seleccionar tabla para añadir registro"""
        ventana_tabla = tkinter.Toplevel(raiz)
        ventana_tabla.title("Añadir Registro - Seleccionar Tabla")
        ventana_tabla.geometry("400x300")
        ventana_tabla.grab_set()
        
        titulo = tkinter.Label(ventana_tabla, text="Seleccione la tabla:", font=('arial', 14, 'bold'))
        titulo.pack(pady=20)
        
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        tablas = [tabla[0] for tabla in cursor.fetchall()]
        
        if not tablas:
            messagebox.showwarning("Sin tablas", "No hay tablas disponibles. Crea una primero.")
            ventana_tabla.destroy()
            return
        
        combo_tabla = ttk.Combobox(ventana_tabla, values=tablas, state="readonly", font=('arial', 11), width=25)
        combo_tabla.pack(pady=10)
        combo_tabla.current(0)
        
        def continuar():
            if not combo_tabla.get():
                messagebox.showerror("Error", "Debe seleccionar una tabla")
                return
            
            tabla_seleccionada = combo_tabla.get()
            ventana_tabla.destroy()
            abrir_ventana_insertar_registro(tabla_seleccionada)
        
        btn_continuar = tkinter.Button(ventana_tabla, text="Continuar", command=continuar,
                                       bg="dodgerblue", fg="white", font=('arial', 12), width=15, height=2)
        btn_continuar.pack(pady=20)
    
    def abrir_ventana_insertar_registro(nombre_tabla):
        """Segunda ventana: formulario para insertar registro"""
        cursor.execute(f"PRAGMA table_info({nombre_tabla})")
        info_columnas = cursor.fetchall()
        
        campos_info = []
        for col in info_columnas:
            if col[5] != 1:
                campos_info.append({'nombre': col[1], 'tipo': col[2]})
        
        ventana_datos = tkinter.Toplevel(raiz)
        ventana_datos.title(f"Añadir registro en {nombre_tabla}")
        ventana_datos.geometry("500x650")
        
        titulo = tkinter.Label(ventana_datos, text=f"Añadir registro en: {nombre_tabla}", font=('arial', 14, 'bold'))
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
        
        for i, campo_info in enumerate(campos_info):
            frame_dato = tkinter.Frame(frame_datos, relief="groove", bd=2)
            frame_dato.pack(fill="x", padx=10, pady=5)
            
            tkinter.Label(frame_dato, text=f"{campo_info['nombre']} ({campo_info['tipo']}):", font=('arial', 11, 'bold')).pack(pady=5)
            
            entry_dato = tkinter.Entry(frame_dato, width=40, font=('arial', 10))
            entry_dato.pack(pady=5, padx=10)
            
            datos_entries.append(entry_dato)
        
        frame_datos.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        
        def insertar_datos(cerrar=False):
            valores = []
            for entry in datos_entries:
                valor = entry.get().strip()
                valores.append(valor if valor else None)
            
            if all(v is None for v in valores):
                messagebox.showwarning("Advertencia", "Debe ingresar al menos un dato")
                return
            
            columnas = ", ".join([c['nombre'] for c in campos_info])
            placeholders = ", ".join(["?" for _ in valores])
            sql = f"INSERT INTO {nombre_tabla} ({columnas}) VALUES ({placeholders})"
            
            try:
                cursor.execute(sql, valores)
                conexion.commit()
                messagebox.showinfo("Éxito", f"Registro insertado exitosamente")
                
                if cerrar:
                    ventana_datos.destroy()
                    LeerBaseDatos()
                else:
                    for entry in datos_entries:
                        entry.delete(0, 'end')
                    datos_entries[0].focus()
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error al insertar: {e}")
        
        frame_botones = tkinter.Frame(ventana_datos)
        frame_botones.pack(pady=15)
        
        btn_insertar_otro = tkinter.Button(frame_botones, text="Insertar y Añadir Otro", 
                                           command=lambda: insertar_datos(cerrar=False),
                                           bg="green", fg="white", font=('arial', 11), 
                                           width=20, height=2)
        btn_insertar_otro.pack(side="left", padx=5)
        
        btn_insertar_cerrar = tkinter.Button(frame_botones, text="Insertar y Finalizar", 
                                             command=lambda: insertar_datos(cerrar=True),
                                             bg="blue", fg="white", font=('arial', 11), 
                                             width=20, height=2)
        btn_insertar_cerrar.pack(side="left", padx=5)
    
    # ============================================================================
    # OPCIÓN 3: AÑADIR CAMPO A TABLA EXISTENTE
    # ============================================================================
    
    def ventana_seleccionar_tabla_campo():
        """Primera ventana: seleccionar tabla para añadir campo"""
        ventana_tabla = tkinter.Toplevel(raiz)
        ventana_tabla.title("Añadir Campo - Seleccionar Tabla")
        ventana_tabla.geometry("400x300")
        ventana_tabla.grab_set()
        
        titulo = tkinter.Label(ventana_tabla, text="Seleccione la tabla:", font=('arial', 14, 'bold'))
        titulo.pack(pady=20)
        
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        tablas = [tabla[0] for tabla in cursor.fetchall()]
        
        if not tablas:
            messagebox.showwarning("Sin tablas", "No hay tablas disponibles. Crea una primero.")
            ventana_tabla.destroy()
            return
        
        combo_tabla = ttk.Combobox(ventana_tabla, values=tablas, state="readonly", font=('arial', 11), width=25)
        combo_tabla.pack(pady=10)
        combo_tabla.current(0)
        
        def continuar():
            if not combo_tabla.get():
                messagebox.showerror("Error", "Debe seleccionar una tabla")
                return
            
            tabla_seleccionada = combo_tabla.get()
            ventana_tabla.destroy()
            ventana_añadir_campo(tabla_seleccionada)
        
        btn_continuar = tkinter.Button(ventana_tabla, text="Continuar", command=continuar,
                                       bg="dodgerblue", fg="white", font=('arial', 12), width=15, height=2)
        btn_continuar.pack(pady=20)
    
    def ventana_añadir_campo(nombre_tabla):
        """Segunda ventana: configurar nuevo campo"""
        ventana_campo = tkinter.Toplevel(raiz)
        ventana_campo.title(f"Añadir campo a {nombre_tabla}")
        ventana_campo.geometry("450x400")
        ventana_campo.grab_set()
        
        titulo = tkinter.Label(ventana_campo, text=f"Añadir campo a tabla: {nombre_tabla}", 
                              font=('arial', 14, 'bold'))
        titulo.pack(pady=20)
        
        # Mostrar campos existentes
        cursor.execute(f"PRAGMA table_info({nombre_tabla})")
        columnas_existentes = cursor.fetchall()
        
        label_existentes = tkinter.Label(ventana_campo, text="Campos existentes:", 
                                         font=('arial', 11, 'bold'))
        label_existentes.pack(pady=10)
        
        frame_existentes = tkinter.Frame(ventana_campo, relief="groove", bd=2)
        frame_existentes.pack(padx=20, pady=5)
        
        for col in columnas_existentes:
            tkinter.Label(frame_existentes, text=f"• {col[1]} ({col[2]})", 
                         font=('arial', 9)).pack(anchor='w', padx=10, pady=2)
        
        # Nuevo campo
        frame_nuevo = tkinter.LabelFrame(ventana_campo, text="Nuevo Campo", font=('arial', 11))
        frame_nuevo.pack(padx=20, pady=20, fill="x")
        
        tkinter.Label(frame_nuevo, text="Nombre del campo:", font=('arial', 10)).grid(row=0, column=0, sticky="e", padx=10, pady=10)
        entry_nombre = tkinter.Entry(frame_nuevo, width=25, font=('arial', 10))
        entry_nombre.grid(row=0, column=1, padx=10, pady=10)
        
        tkinter.Label(frame_nuevo, text="Tipo del campo:", font=('arial', 10)).grid(row=1, column=0, sticky="e", padx=10, pady=10)
        combo_tipo = ttk.Combobox(frame_nuevo, width=23, state="readonly", font=('arial', 10))
        combo_tipo['values'] = ('INTEGER', 'TEXT', 'REAL', 'BLOB', 'VARCHAR(50)', 'DATE', 'FLOAT')
        combo_tipo.current(1)  # TEXT por defecto
        combo_tipo.grid(row=1, column=1, padx=10, pady=10)
        
        def añadir_campo_bd():
            nombre_campo = entry_nombre.get().strip()
            tipo_campo = combo_tipo.get()
            
            if not nombre_campo:
                messagebox.showerror("Error", "Debe ingresar un nombre para el campo")
                return
            
            palabras_reservadas = ['as', 'select', 'from', 'where', 'table', 'order', 'group', 'by', 'create', 'insert', 'update', 'delete']
            if nombre_campo.lower() in palabras_reservadas:
                messagebox.showerror("Error", f"'{nombre_campo}' es una palabra reservada")
                return
            
            # Verificar que no exista ya
            if any(col[1].lower() == nombre_campo.lower() for col in columnas_existentes):
                messagebox.showerror("Error", f"El campo '{nombre_campo}' ya existe en la tabla")
                return
            
            sql = f"ALTER TABLE {nombre_tabla} ADD COLUMN {nombre_campo} {tipo_campo}"
            
            try:
                cursor.execute(sql)
                conexion.commit()
                messagebox.showinfo("Éxito", f"Campo '{nombre_campo}' añadido exitosamente a '{nombre_tabla}'")
                ventana_campo.destroy()
                LeerBaseDatos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo añadir el campo: {e}")
        
        btn_añadir = tkinter.Button(ventana_campo, text="Añadir Campo", command=añadir_campo_bd,
                                    bg="orange", fg="white", font=('arial', 12), width=18, height=2)
        btn_añadir.pack(pady=20)

def BorrarTabla():
    # VENTANA INICIAL: Elegir qué borrar
    ventana_seleccion = tkinter.Toplevel(raiz)
    ventana_seleccion.title("Eliminar")
    ventana_seleccion.geometry("450x400")
    ventana_seleccion.grab_set()
    
    titulo = tkinter.Label(ventana_seleccion, text="¿Qué desea eliminar?", font=('arial', 16, 'bold'))
    titulo.pack(pady=30)
    
    def borrar_tabla():
        ventana_seleccion.destroy()
        ventana_borrar_tabla()
    
    def borrar_registro():
        ventana_seleccion.destroy()
        ventana_seleccionar_tabla_registro()
    
    def borrar_campo():
        ventana_seleccion.destroy()
        ventana_seleccionar_tabla_campo()
    
    # Botones
    frame_botones = tkinter.Frame(ventana_seleccion)
    frame_botones.pack(pady=10)
    
    btn_tabla = tkinter.Button(frame_botones, text="Eliminar Tabla Completa", 
                               command=borrar_tabla,
                               bg="red", fg="white", 
                               font=('arial', 12), width=25, height=2)
    btn_tabla.pack(pady=8)
    
    btn_registro = tkinter.Button(frame_botones, text="Eliminar Registro", 
                                  command=borrar_registro,
                                  bg="orange", fg="white", 
                                  font=('arial', 12), width=25, height=2)
    btn_registro.pack(pady=8)
    
    btn_campo = tkinter.Button(frame_botones, text="Eliminar Campo de Tabla", 
                               command=borrar_campo,
                               bg="dodgerblue", fg="white", 
                               font=('arial', 12), width=25, height=2)
    btn_campo.pack(pady=8)
    
    # ============================================================================
    # OPCIÓN 1: ELIMINAR TABLA COMPLETA
    # ============================================================================
    
    def ventana_borrar_tabla():
        """Primera ventana: seleccionar tabla a eliminar"""
        ventana_inicial = tkinter.Toplevel(raiz)
        ventana_inicial.title("Eliminar Tabla")
        ventana_inicial.geometry("400x300")
        ventana_inicial.grab_set()
        
        titulo = tkinter.Label(ventana_inicial, text="Eliminar Tabla", 
                              font=('arial', 16, 'bold'))
        titulo.pack(pady=20)
        
        # Obtener lista de tablas
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        tablas = [tabla[0] for tabla in cursor.fetchall()]
        
        if not tablas:
            mensaje_error = tkinter.Label(ventana_inicial, 
                                         text="No hay tablas disponibles para eliminar", 
                                         font=('arial', 11), fg="red")
            mensaje_error.pack(pady=20)
            
            btn_cerrar = tkinter.Button(ventana_inicial, text="Cerrar", 
                                       command=ventana_inicial.destroy, 
                                       bg="gray", fg="white", 
                                       font=('arial', 12))
            btn_cerrar.pack(pady=20)
            return
        
        frame_seleccion = tkinter.Frame(ventana_inicial)
        frame_seleccion.pack(pady=20)
        
        tkinter.Label(frame_seleccion, text="Seleccione la tabla a eliminar:", 
                     font=('arial', 12)).pack(pady=10)
        
        combo_tabla = ttk.Combobox(frame_seleccion, values=tablas, 
                                   state="readonly", font=('arial', 11), width=25)
        combo_tabla.pack(pady=10)
        if tablas:
            combo_tabla.current(0)
        
        def continuar():
            tabla_seleccionada = combo_tabla.get()
            
            if not tabla_seleccionada:
                messagebox.showerror("Error", "Debe seleccionar una tabla")
                return
            
            abrir_ventana_confirmacion_tabla(tabla_seleccionada, ventana_inicial)
        
        btn_continuar = tkinter.Button(ventana_inicial, text="Continuar", 
                                       command=continuar, 
                                       bg="dodgerblue", fg="white", 
                                       font=('arial', 12), width=15, height=2)
        btn_continuar.pack(pady=20)
        
        ventana_inicial.bind('<Return>', lambda event: continuar())
        ventana_inicial.bind('<Escape>', lambda event: ventana_inicial.destroy())
    
    def abrir_ventana_confirmacion_tabla(nombre_tabla, ventana_anterior):
        """Segunda ventana: confirmar eliminación de tabla"""
        ventana_anterior.destroy()
        
        ventana_confirmacion = tkinter.Toplevel(raiz)
        ventana_confirmacion.title("Confirmar Eliminación")
        ventana_confirmacion.geometry("500x300")
        ventana_confirmacion.grab_set()
        
        mensaje1 = tkinter.Label(ventana_confirmacion, 
                                text=f"¿Está seguro que desea eliminar la tabla '{nombre_tabla}'?", 
                                font=('arial', 12, 'bold'))
        mensaje1.pack(pady=20)
        
        mensaje2 = tkinter.Label(ventana_confirmacion, 
                                text="Esta acción eliminará TODOS los datos de la tabla", 
                                font=('arial', 11), fg="red")
        mensaje2.pack(pady=5)
        
        mensaje3 = tkinter.Label(ventana_confirmacion, 
                                text="y NO se puede deshacer.", 
                                font=('arial', 11), fg="red")
        mensaje3.pack(pady=5)
        
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {nombre_tabla}")
            num_registros = cursor.fetchone()[0]
            
            info = tkinter.Label(ventana_confirmacion, 
                               text=f"La tabla contiene {num_registros} registro(s)", 
                               font=('arial', 10, 'italic'))
            info.pack(pady=15)
        except:
            pass
        
        def eliminar_tabla():
            try:
                cursor.execute(f"DROP TABLE {nombre_tabla}")
                conexion.commit()
                messagebox.showinfo("Éxito", f"Tabla '{nombre_tabla}' eliminada exitosamente")
                ventana_confirmacion.destroy()
                LeerBaseDatos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la tabla: {e}")
        
        def cancelar():
            ventana_confirmacion.destroy()
        
        frame_botones = tkinter.Frame(ventana_confirmacion)
        frame_botones.pack(pady=30)
        
        btn_cancelar = tkinter.Button(frame_botones, text="Cancelar", 
                                      command=cancelar, 
                                      bg="gray", fg="white", 
                                      font=('arial', 12), width=15, height=2)
        btn_cancelar.pack(side="left", padx=10)
        
        btn_eliminar = tkinter.Button(frame_botones, text="Eliminar Tabla", 
                                     command=eliminar_tabla, 
                                     bg="red", fg="white", 
                                     font=('arial', 12), width=15, height=2)
        btn_eliminar.pack(side="left", padx=10)
        
        ventana_confirmacion.bind('<Escape>', lambda event: cancelar())
    
    # ============================================================================
    # OPCIÓN 2: ELIMINAR REGISTRO
    # ============================================================================
    
    def ventana_seleccionar_tabla_registro():
        """Primera ventana: seleccionar tabla para eliminar registro"""
        ventana_tabla = tkinter.Toplevel(raiz)
        ventana_tabla.title("Eliminar Registro - Seleccionar Tabla")
        ventana_tabla.geometry("400x300")
        ventana_tabla.grab_set()
        
        titulo = tkinter.Label(ventana_tabla, text="Seleccione la tabla:", font=('arial', 14, 'bold'))
        titulo.pack(pady=20)
        
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        tablas = [tabla[0] for tabla in cursor.fetchall()]
        
        if not tablas:
            messagebox.showwarning("Sin tablas", "No hay tablas disponibles.")
            ventana_tabla.destroy()
            return
        
        combo_tabla = ttk.Combobox(ventana_tabla, values=tablas, state="readonly", font=('arial', 11), width=25)
        combo_tabla.pack(pady=10)
        combo_tabla.current(0)
        
        def continuar():
            if not combo_tabla.get():
                messagebox.showerror("Error", "Debe seleccionar una tabla")
                return
            
            tabla_seleccionada = combo_tabla.get()
            ventana_tabla.destroy()
            ventana_seleccionar_id_registro(tabla_seleccionada)
        
        btn_continuar = tkinter.Button(ventana_tabla, text="Continuar", command=continuar,
                                       bg="dodgerblue", fg="white", font=('arial', 12), width=15, height=2)
        btn_continuar.pack(pady=20)
        
        ventana_tabla.bind('<Return>', lambda event: continuar())
    
    def ventana_seleccionar_id_registro(nombre_tabla):
        """Segunda ventana: ingresar ID del registro a eliminar y eliminarlo directamente"""
        ventana_id = tkinter.Toplevel(raiz)
        ventana_id.title("Eliminar Registro - Ingresar ID")
        ventana_id.geometry("450x400")
        ventana_id.grab_set()
        
        # Obtener primary key
        cursor.execute(f"PRAGMA table_info({nombre_tabla})")
        columnas_info = cursor.fetchall()
        pk_columna = None
        for col in columnas_info:
            if col[5] == 1:  # pk flag
                pk_columna = col[1]
                break
        
        # Si no se encuentra primary key, usar la primera columna
        if pk_columna is None and columnas_info:
            pk_columna = columnas_info[0][1]
        
        titulo = tkinter.Label(ventana_id, text=f"Eliminar registro de: {nombre_tabla}", 
                              font=('arial', 14, 'bold'))
        titulo.pack(pady=20)
        
        # Mostrar registros existentes
        label_existentes = tkinter.Label(ventana_id, text="Registros existentes:", 
                                         font=('arial', 11, 'bold'))
        label_existentes.pack(pady=10)
        
        frame_scroll = tkinter.Frame(ventana_id, relief="groove", bd=2)
        frame_scroll.pack(padx=20, pady=5, fill="both", expand=True)
        
        text_registros = tkinter.Text(frame_scroll, height=8, width=50, font=('arial', 9))
        scrollbar = tkinter.Scrollbar(frame_scroll, command=text_registros.yview)
        text_registros.config(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        text_registros.pack(side="left", fill="both", expand=True)
        
        # Cargar registros
        cursor.execute(f"SELECT * FROM {nombre_tabla}")
        registros = cursor.fetchall()
        
        nombres_columnas = [col[1] for col in columnas_info]
        for reg in registros:
            text_registros.insert("end", f"{pk_columna}={reg[0]}: {dict(zip(nombres_columnas, reg))}\n")
        
        text_registros.config(state="disabled")
        
        # Input para ID
        frame_input = tkinter.Frame(ventana_id)
        frame_input.pack(pady=15)
        
        tkinter.Label(frame_input, text=f"Ingrese el {pk_columna} a eliminar:", 
                     font=('arial', 11)).pack(side="left", padx=5)
        entry_id = tkinter.Entry(frame_input, font=('arial', 11), width=15)
        entry_id.pack(side="left", padx=5)
        entry_id.focus()
        
        def eliminar_directamente():
            id_valor = entry_id.get().strip()
            
            if not id_valor:
                messagebox.showerror("Error", "Debe ingresar un ID")
                return
            
            try:
                id_int = int(id_valor)
            except ValueError:
                messagebox.showerror("Error", "El ID debe ser un número entero")
                return
            
            # Verificar que existe
            cursor.execute(f"SELECT * FROM {nombre_tabla} WHERE {pk_columna} = ?", (id_int,))
            registro = cursor.fetchone()
            
            if registro is None:
                messagebox.showerror("Error", f"No existe ningún registro con {pk_columna} = {id_int}")
                return
            
            # ELIMINAR DIRECTAMENTE SIN CONFIRMACIÓN
            try:
                cursor.execute(f"DELETE FROM {nombre_tabla} WHERE {pk_columna} = ?", (id_int,))
                conexion.commit()
                messagebox.showinfo("Éxito", f"Registro con {pk_columna} = {id_int} eliminado exitosamente")
                ventana_id.destroy()
                LeerBaseDatos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {e}")
        
        btn_eliminar = tkinter.Button(ventana_id, text="Eliminar Registro", command=eliminar_directamente,
                                       bg="red", fg="white", font=('arial', 12), width=20, height=2)
        btn_eliminar.pack(pady=10)
        
        ventana_id.bind('<Return>', lambda event: eliminar_directamente())
    
    # ============================================================================
    # OPCIÓN 3: ELIMINAR CAMPO
    # ============================================================================
    
    def ventana_seleccionar_tabla_campo():
        """Primera ventana: seleccionar tabla para eliminar campo"""
        ventana_tabla = tkinter.Toplevel(raiz)
        ventana_tabla.title("Eliminar Campo - Seleccionar Tabla")
        ventana_tabla.geometry("400x300")
        ventana_tabla.grab_set()
        
        titulo = tkinter.Label(ventana_tabla, text="Seleccione la tabla:", font=('arial', 14, 'bold'))
        titulo.pack(pady=20)
        
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        tablas = [tabla[0] for tabla in cursor.fetchall()]
        
        if not tablas:
            messagebox.showwarning("Sin tablas", "No hay tablas disponibles.")
            ventana_tabla.destroy()
            return
        
        combo_tabla = ttk.Combobox(ventana_tabla, values=tablas, state="readonly", font=('arial', 11), width=25)
        combo_tabla.pack(pady=10)
        combo_tabla.current(0)
        
        def continuar():
            if not combo_tabla.get():
                messagebox.showerror("Error", "Debe seleccionar una tabla")
                return
            
            tabla_seleccionada = combo_tabla.get()
            ventana_tabla.destroy()
            ventana_seleccionar_campo_eliminar(tabla_seleccionada)
        
        btn_continuar = tkinter.Button(ventana_tabla, text="Continuar", command=continuar,
                                       bg="dodgerblue", fg="white", font=('arial', 12), width=15, height=2)
        btn_continuar.pack(pady=20)
        
        ventana_tabla.bind('<Return>', lambda event: continuar())
    
    def ventana_seleccionar_campo_eliminar(nombre_tabla):
        """Segunda ventana: seleccionar campo a eliminar"""
        ventana_campo = tkinter.Toplevel(raiz)
        ventana_campo.title(f"Eliminar Campo de {nombre_tabla}")
        ventana_campo.geometry("450x400")
        ventana_campo.grab_set()
        
        titulo = tkinter.Label(ventana_campo, 
                              text=f"Eliminar campo de: {nombre_tabla}", 
                              font=('arial', 14, 'bold'))
        titulo.pack(pady=20)
        
        # Obtener campos
        cursor.execute(f"PRAGMA table_info({nombre_tabla})")
        columnas_info = cursor.fetchall()
        
        # No permitir eliminar la primary key
        campos_eliminables = []
        for col in columnas_info:
            if col[5] != 1:  # No es primary key
                campos_eliminables.append(f"{col[1]} ({col[2]})")
        
        if not campos_eliminables:
            messagebox.showwarning("Sin campos", "No hay campos eliminables (solo hay primary key)")
            ventana_campo.destroy()
            return
        
        label_info = tkinter.Label(ventana_campo, 
                                   text="NOTA: SQLite no permite eliminar campos directamente.\nSe creará una nueva tabla sin el campo seleccionado.", 
                                   font=('arial', 9, 'italic'), fg="blue")
        label_info.pack(pady=10)
        
        tkinter.Label(ventana_campo, text="Seleccione el campo a eliminar:", 
                     font=('arial', 11, 'bold')).pack(pady=10)
        
        combo_campo = ttk.Combobox(ventana_campo, values=campos_eliminables, 
                                   state="readonly", font=('arial', 11), width=30)
        combo_campo.pack(pady=10)
        combo_campo.current(0)
        
        def continuar():
            if not combo_campo.get():
                messagebox.showerror("Error", "Debe seleccionar un campo")
                return
            
            campo_seleccionado = combo_campo.get().split(" (")[0]  # Extraer solo el nombre
            ventana_campo.destroy()
            ventana_confirmar_eliminar_campo(nombre_tabla, campo_seleccionado, columnas_info)
        
        btn_confirmar = tkinter.Button(ventana_campo, text="Continuar", command=continuar,
                                       bg="dodgerblue", fg="white", font=('arial', 12), width=15, height=2)
        btn_confirmar.pack(pady=20)
    
    def ventana_confirmar_eliminar_campo(nombre_tabla, campo, columnas_info):
        """Tercera ventana: confirmar eliminación del campo"""
        ventana_conf = tkinter.Toplevel(raiz)
        ventana_conf.title("Confirmar Eliminación")
        ventana_conf.geometry("450x350")
        ventana_conf.grab_set()
        
        titulo = tkinter.Label(ventana_conf, 
                              text=f"¿Está seguro de eliminar el campo '{campo}'?", 
                              font=('arial', 12, 'bold'))
        titulo.pack(pady=20)
        
        mensaje1 = tkinter.Label(ventana_conf, 
                                text=f"Tabla: {nombre_tabla}", 
                                font=('arial', 10))
        mensaje1.pack(pady=5)
        
        mensaje2 = tkinter.Label(ventana_conf, 
                                text="Se eliminarán TODOS los datos de esta columna", 
                                font=('arial', 10), fg="red")
        mensaje2.pack(pady=5)
        
        mensaje3 = tkinter.Label(ventana_conf, 
                                text="Esta acción NO se puede deshacer", 
                                font=('arial', 10), fg="red")
        mensaje3.pack(pady=5)
        
        def eliminar():
            try:
                # SQLite no permite DROP COLUMN directamente
                # Hay que recrear la tabla sin ese campo
                
                # 1. Obtener todas las columnas excepto la que se va a eliminar
                columnas_nuevas = [f"{col[1]} {col[2]}" for col in columnas_info if col[1] != campo]
                nombres_columnas = [col[1] for col in columnas_info if col[1] != campo]
                
                # 2. Crear tabla temporal
                sql_create = f"CREATE TABLE temp_table ({', '.join(columnas_nuevas)})"
                cursor.execute(sql_create)
                
                # 3. Copiar datos (sin el campo eliminado)
                columnas_str = ', '.join(nombres_columnas)
                cursor.execute(f"INSERT INTO temp_table SELECT {columnas_str} FROM {nombre_tabla}")
                
                # 4. Eliminar tabla original
                cursor.execute(f"DROP TABLE {nombre_tabla}")
                
                # 5. Renombrar tabla temporal
                cursor.execute(f"ALTER TABLE temp_table RENAME TO {nombre_tabla}")
                
                conexion.commit()
                messagebox.showinfo("Éxito", f"Campo '{campo}' eliminado exitosamente")
                ventana_conf.destroy()
                LeerBaseDatos()
                
            except Exception as e:
                conexion.rollback()
                messagebox.showerror("Error", f"No se pudo eliminar el campo: {e}")
        
        def cancelar():
            ventana_conf.destroy()
        
        frame_botones = tkinter.Frame(ventana_conf)
        frame_botones.pack(pady=30)
        
        btn_cancelar = tkinter.Button(frame_botones, text="Cancelar", 
                                      command=cancelar, 
                                      bg="gray", fg="white", 
                                      font=('arial', 12), width=15, height=2)
        btn_cancelar.pack(side="left", padx=10)
        
        btn_eliminar = tkinter.Button(frame_botones, text="Eliminar Campo", 
                                     command=eliminar, 
                                     bg="red", fg="white", 
                                     font=('arial', 12), width=15, height=2)
        btn_eliminar.pack(side="left", padx=10)

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
    # 1) Ventana principal (Buscar / Ordenar / Filtrar)
    ventana = tkinter.Toplevel(raiz)
    ventana.title("Buscar / Ordenar / Filtrar")
    ventana.geometry("560x320")
    ventana.grab_set()

    # 2) Obtener tablas
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)
    tablas = [t[0] for t in cursor.fetchall()]

    tkinter.Label(ventana, text="Tabla:", font=("Arial", 11, "bold")).pack(pady=(10, 0))
    combo_tabla = ttk.Combobox(ventana, state="readonly", values=tablas)
    combo_tabla.pack(fill="x", padx=12, pady=6)

    tkinter.Label(ventana, text="Columna (opcional):", font=("Arial", 11, "bold")).pack(pady=(10, 0))
    combo_columna = ttk.Combobox(ventana, state="readonly")
    combo_columna.pack(fill="x", padx=12, pady=6)

    tkinter.Label(ventana, text="Texto a buscar:", font=("Arial", 11, "bold")).pack(pady=(10, 0))
    entry_texto = tkinter.Entry(ventana)
    entry_texto.pack(fill="x", padx=12, pady=6)

    info = tkinter.Label(ventana, text="", fg="gray")
    info.pack(pady=5)

    # -------- helpers ----------
    def cargar_columnas(event=None):
        tabla = combo_tabla.get().strip()
        if not tabla:
            return
        cursor.execute(f"PRAGMA table_info({tabla})")
        cols = [c[1] for c in cursor.fetchall()]
        combo_columna["values"] = ["(Todas)"] + cols
        combo_columna.current(0)

    def limpiar_tree(tree):
        for item in tree.get_children():
            tree.delete(item)

    def seleccionar_pestana_y_mostrar(tabla, filas):
        tree = trees_por_tabla.get(tabla)
        if tree is None:
            messagebox.showerror("Error", f"No encuentro el Treeview de la tabla '{tabla}'.")
            return

        limpiar_tree(tree)
        for fila in filas:
            tree.insert("", "end", values=fila)

        # Seleccionar la pestaña correcta
        for tab_id in notebook.tabs():
            if notebook.tab(tab_id, "text").lower() == tabla.lower():
                notebook.select(tab_id)
                break

    # -------- Buscar (texto) ----------
    def buscar():
        tabla = combo_tabla.get().strip()
        col = combo_columna.get().strip()
        texto = entry_texto.get().strip()

        if not tabla:
            messagebox.showerror("Error", "Selecciona una tabla.")
            return

        # Si texto vacío, mostrar todo
        if texto == "":
            cursor.execute(f"SELECT * FROM {tabla}")
            filas = cursor.fetchall()
            seleccionar_pestana_y_mostrar(tabla, filas)
            info.config(text=f"Mostrando todo: {len(filas)} filas")
            return

        cursor.execute(f"PRAGMA table_info({tabla})")
        cols = [c[1] for c in cursor.fetchall()]

        if col and col != "(Todas)":
            sql = f"SELECT * FROM {tabla} WHERE CAST({col} AS TEXT) LIKE ?"
            params = (f"%{texto}%",)
        else:
            condiciones = " OR ".join([f"CAST({c} AS TEXT) LIKE ?" for c in cols])
            sql = f"SELECT * FROM {tabla} WHERE {condiciones}"
            params = tuple([f"%{texto}%"] * len(cols))

        try:
            cursor.execute(sql, params)
            filas = cursor.fetchall()
            seleccionar_pestana_y_mostrar(tabla, filas)
            info.config(text=f"Resultados: {len(filas)}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo buscar:\n{e}")

    # -------- Ordenar / Filtrar ----------
    def abrir_ordenar_filtrar():
        tabla = combo_tabla.get().strip()
        if not tabla:
            messagebox.showerror("Error", "Selecciona una tabla primero.")
            return

        win = tkinter.Toplevel(ventana)
        win.title("Ordenar / Filtrar")
        win.geometry("600x420")
        win.grab_set()

        # Columnas y tipos
        cursor.execute(f"PRAGMA table_info({tabla})")
        info_cols = cursor.fetchall()
        columnas = [c[1] for c in info_cols]
        tipos = {c[1]: (c[2] or "").upper() for c in info_cols}

        tkinter.Label(win, text=f"Tabla: {tabla}", font=("Arial", 12, "bold")).pack(pady=(10, 0))

        # Columna orden
        tkinter.Label(win, text="Ordenar por:", font=("Arial", 11, "bold")).pack(pady=(10, 0))
        combo_col_orden = ttk.Combobox(win, state="readonly", values=columnas)
        combo_col_orden.pack(fill="x", padx=12, pady=6)
        combo_col_orden.current(0)

        tkinter.Label(win, text="Tipo de orden:", font=("Arial", 11, "bold")).pack(pady=(10, 0))
        combo_orden = ttk.Combobox(win, state="readonly",
                                  values=["ASC", "DESC"])
        combo_orden.pack(fill="x", padx=12, pady=6)
        combo_orden.current(0)

        # --- filtro opcional ---
        tkinter.Label(win, text="Filtro (opcional):", font=("Arial", 11, "bold")).pack(pady=(10, 0))
        frame_filtro = tkinter.Frame(win)
        frame_filtro.pack(fill="x", padx=12, pady=6)

        combo_col_filtro = ttk.Combobox(frame_filtro, state="readonly", values=["(Sin filtro)"] + columnas, width=18)
        combo_col_filtro.pack(side="left", padx=5)
        combo_col_filtro.current(0)

        combo_op = ttk.Combobox(frame_filtro, state="readonly",
                                values=["=", "!=", ">", "<", ">=", "<=", "contiene"], width=10)
        combo_op.pack(side="left", padx=5)
        combo_op.current(0)

        entry_valor = tkinter.Entry(frame_filtro)
        entry_valor.pack(side="left", fill="x", expand=True, padx=5)

        info2 = tkinter.Label(win, text="", fg="gray")
        info2.pack(pady=5)

        def aplicar():
            col_orden = combo_col_orden.get().strip()
            orden = combo_orden.get().strip()  # ASC o DESC

            col_fil = combo_col_filtro.get().strip()
            op = combo_op.get().strip()
            val = entry_valor.get().strip()

            sql = f"SELECT * FROM {tabla}"
            params = []

            # Si hay filtro
            if col_fil != "(Sin filtro)" and val != "":
                tipo_col = tipos.get(col_fil, "")

                # contiene => LIKE
                if op == "contiene":
                    sql += f" WHERE CAST({col_fil} AS TEXT) LIKE ?"
                    params.append(f"%{val}%")
                else:
                    # decidir si numérico
                    es_num = any(t in tipo_col for t in ["INT", "REAL", "FLOAT", "DOUBLE", "NUM"])
                    if es_num:
                        try:
                            val_num = float(val) if "." in val else int(val)
                        except ValueError:
                            messagebox.showerror("Error", f"'{val}' no es un número válido para {col_fil} ({tipo_col})")
                            return
                        sql += f" WHERE {col_fil} {op} ?"
                        params.append(val_num)
                    else:
                        # texto: comparar como texto
                        sql += f" WHERE CAST({col_fil} AS TEXT) {op} ?"
                        params.append(val)

            sql += f" ORDER BY {col_orden} {orden}"

            try:
                cursor.execute(sql, tuple(params))
                filas = cursor.fetchall()
                seleccionar_pestana_y_mostrar(tabla, filas)
                info2.config(text=f"Mostrando {len(filas)} filas | ORDER BY {col_orden} {orden}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo aplicar ordenar/filtrar:\n{e}")

        def resetear():
            cursor.execute(f"SELECT * FROM {tabla}")
            filas = cursor.fetchall()
            seleccionar_pestana_y_mostrar(tabla, filas)
            info2.config(text=f"Mostrando todo: {len(filas)} filas")

        frame_btn2 = tkinter.Frame(win)
        frame_btn2.pack(pady=14)

        tkinter.Button(frame_btn2, text="Aplicar", command=aplicar, bg="green", fg="white", width=12).pack(side="left", padx=6)
        tkinter.Button(frame_btn2, text="Reset", command=resetear, bg="dodgerblue", fg="white", width=12).pack(side="left", padx=6)
        tkinter.Button(frame_btn2, text="Cerrar", command=win.destroy, bg="gray", fg="white", width=12).pack(side="left", padx=6)

        win.bind("<Return>", lambda e: aplicar())

    # Selección inicial
    if tablas:
        combo_tabla.current(0)
        cargar_columnas()
    combo_tabla.bind("<<ComboboxSelected>>", cargar_columnas)

    # Botones
    frame_btn = tkinter.Frame(ventana)
    frame_btn.pack(pady=10)

    tkinter.Button(frame_btn, text="Buscar", command=buscar, bg="green", fg="white").pack(side="left", padx=6)
    tkinter.Button(frame_btn, text="Ordenar/Filtrar", command=abrir_ordenar_filtrar, bg="orange", fg="white").pack(side="left", padx=6)
    tkinter.Button(frame_btn, text="Cerrar", command=ventana.destroy).pack(side="left", padx=6)

    entry_texto.focus()
    ventana.bind("<Return>", lambda e: buscar())

def MostrarGrafico():
    """
    Función principal para crear gráficos desde las tablas
    """
    # Ventana 1: Seleccionar tabla
    ventana_tabla = tkinter.Toplevel(raiz)
    ventana_tabla.title("Gráfico - Seleccionar Tabla")
    ventana_tabla.geometry("400x250")
    ventana_tabla.grab_set()
    
    # Obtener lista de tablas
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)
    tablas = [tabla[0] for tabla in cursor.fetchall()]
    
    label_titulo = tkinter.Label(ventana_tabla, text="Seleccione la tabla:", font=('Arial', 12, 'bold'))
    label_titulo.pack(pady=20)
    
    combo_tabla = ttk.Combobox(ventana_tabla, values=tablas, state="readonly", font=('Arial', 11), width=25)
    combo_tabla.pack(pady=10)
    if tablas:
        combo_tabla.current(0)
    
    def continuar():
        if not combo_tabla.get():
            messagebox.showerror("Error", "Debe seleccionar una tabla")
            return
        
        tabla_seleccionada = combo_tabla.get()
        ventana_tabla.destroy()
        ventana_configurar_grafico(tabla_seleccionada)
    
    boton_siguiente = tkinter.Button(ventana_tabla, text="Siguiente", command=continuar, 
                   bg="dodgerblue", fg="white", font=('Arial', 12), width=15, height=2)
    boton_siguiente.pack(pady=30)
    
    ventana_tabla.bind('<Return>', lambda event: continuar())

def ventana_configurar_grafico(tabla):
    """
    Ventana 2: Configurar tipo de gráfico y campos
    """
    ventana_config = tkinter.Toplevel(raiz)
    ventana_config.title("Gráfico - Configuración")
    ventana_config.geometry("550x650")  # Reducido un poco
    ventana_config.grab_set()
    
    # Obtener columnas de la tabla
    cursor.execute(f"PRAGMA table_info({tabla})")
    columnas_info = cursor.fetchall()
    campos = [col[1] for col in columnas_info]
    tipos = {col[1]: col[2] for col in columnas_info}
    
    # Campos numéricos (para eje Y)
    campos_numericos = [campo for campo in campos if 'INT' in tipos[campo].upper() 
                       or 'FLOAT' in tipos[campo].upper() or 'REAL' in tipos[campo].upper()]
    
    label_titulo = tkinter.Label(ventana_config, text=f"Configurar gráfico de: {tabla}", 
                                 font=('Arial', 13, 'bold'))
    label_titulo.pack(pady=10)
    
    # Tipo de gráfico
    frame_tipo = tkinter.LabelFrame(ventana_config, text="Tipo de Gráfico", font=('Arial', 11))
    frame_tipo.pack(pady=5, padx=20, fill="x")
    
    tipo_grafico = tkinter.StringVar(value="barras")
    
    tkinter.Radiobutton(frame_tipo, text="📊 Gráfico de Barras", variable=tipo_grafico, 
                       value="barras", font=('Arial', 10)).pack(anchor='w', padx=10, pady=3)
    tkinter.Radiobutton(frame_tipo, text="📈 Gráfico de Líneas", variable=tipo_grafico, 
                       value="lineas", font=('Arial', 10)).pack(anchor='w', padx=10, pady=3)
    tkinter.Radiobutton(frame_tipo, text="🥧 Gráfico Circular (Pie)", variable=tipo_grafico, 
                       value="circular", font=('Arial', 10)).pack(anchor='w', padx=10, pady=3)
    tkinter.Radiobutton(frame_tipo, text="📉 Gráfico de Dispersión", variable=tipo_grafico, 
                       value="dispersion", font=('Arial', 10)).pack(anchor='w', padx=10, pady=3)
    
    # Campo para eje X (etiquetas)
    frame_x = tkinter.LabelFrame(ventana_config, text="Eje X (Etiquetas/Categorías)", font=('Arial', 11))
    frame_x.pack(pady=5, padx=20, fill="x")
    
    label_x = tkinter.Label(frame_x, text="Seleccione el campo:", font=('Arial', 10))
    label_x.pack(pady=3)
    
    combo_x = ttk.Combobox(frame_x, values=campos, state="readonly", font=('Arial', 10), width=30)
    combo_x.pack(pady=3)
    if campos:
        combo_x.current(0)
    
    # Campo para eje Y (valores numéricos)
    frame_y = tkinter.LabelFrame(ventana_config, text="Eje Y (Valores numéricos)", font=('Arial', 11))
    frame_y.pack(pady=5, padx=20, fill="x")
    
    label_y = tkinter.Label(frame_y, text="Seleccione el campo:", font=('Arial', 10))
    label_y.pack(pady=3)
    
    combo_y = ttk.Combobox(frame_y, values=campos_numericos, state="readonly", font=('Arial', 10), width=30)
    combo_y.pack(pady=3)
    if campos_numericos:
        combo_y.current(0)
    
    # Opciones adicionales (SOLO ORDENAR)
    frame_opciones = tkinter.LabelFrame(ventana_config, text="Opciones", font=('Arial', 11))
    frame_opciones.pack(pady=5, padx=20, fill="x")
    
    var_ordenar = tkinter.IntVar()
    check_ordenar = tkinter.Checkbutton(frame_opciones, text="Ordenar por valores (mayor a menor)", 
                                        variable=var_ordenar, font=('Arial', 10))
    check_ordenar.pack(pady=8, padx=10, anchor='w')
    
    # FUNCIÓN INTERNA: generar_grafico
    def generar_grafico():
        campo_x = combo_x.get()
        campo_y = combo_y.get()
        tipo = tipo_grafico.get()
        
        if not campo_x or not campo_y:
            messagebox.showerror("Error", "Debe seleccionar ambos campos")
            return
        
        ventana_config.destroy()
        crear_y_mostrar_grafico(tabla, campo_x, campo_y, tipo, var_ordenar.get())
    
    boton_generar = tkinter.Button(ventana_config, text="Generar Gráfico", command=generar_grafico,
                                   bg="green", fg="white", font=('Arial', 12), width=18, height=2)
    boton_generar.pack(pady=20)
    
    ventana_config.bind('<Return>', lambda event: generar_grafico())


def crear_y_mostrar_grafico(tabla, campo_x, campo_y, tipo_grafico, ordenar):
    """
    Crea el gráfico usando matplotlib y lo muestra en una ventana
    """
    try:
        import matplotlib
        matplotlib.use('Agg')  # IMPORTANTE: Backend sin ventana
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    except ImportError:
        messagebox.showerror("Error", "Necesitas instalar matplotlib:\npip install matplotlib")
        return
    
    # Obtener datos
    sql = f"SELECT {campo_x}, {campo_y} FROM {tabla} WHERE {campo_y} IS NOT NULL"
    
    if ordenar:
        sql += f" ORDER BY {campo_y} DESC"
    
    try:
        cursor.execute(sql)
        datos = cursor.fetchall()
        
        if not datos:
            messagebox.showwarning("Sin datos", "No hay datos para generar el gráfico")
            return
        
        # Separar en listas
        etiquetas = [str(fila[0]) for fila in datos]
        valores = [float(fila[1]) if fila[1] is not None else 0 for fila in datos]
        
        # Crear ventana para el gráfico
        ventana_grafico = tkinter.Toplevel(raiz)
        ventana_grafico.title(f"Gráfico - {tabla}")
        
        # Maximizar según el sistema operativo
        try:
            ventana_grafico.state('zoomed')  # Windows
        except:
            ventana_grafico.attributes('-zoomed', True)  # Linux
        
        # Frame superior con información
        frame_info = tkinter.Frame(ventana_grafico)
        frame_info.pack(fill="x", padx=10, pady=10)
        
        label_info = tkinter.Label(frame_info, 
                                   text=f"Tabla: {tabla} | X: {campo_x} | Y: {campo_y}", 
                                   font=('Arial', 11, 'bold'))
        label_info.pack()
        
        # Crear figura de matplotlib
        plt.close('all')  # Cerrar todas las figuras anteriores
        fig = plt.figure(figsize=(14, 8))
        ax = fig.add_subplot(111)
        
        # Generar el gráfico según el tipo
        if tipo_grafico == "barras":
            colores = plt.cm.viridis(range(len(valores)))
            ax.bar(etiquetas, valores, color=colores, edgecolor='black', linewidth=0.5)
            ax.set_xlabel(campo_x, fontsize=12, fontweight='bold')
            ax.set_ylabel(campo_y, fontsize=12, fontweight='bold')
            ax.set_title(f'Gráfico de Barras: {campo_y} por {campo_x}', fontsize=14, fontweight='bold')
            plt.xticks(rotation=45, ha='right')
            
        elif tipo_grafico == "lineas":
            ax.plot(etiquetas, valores, marker='o', linewidth=2, markersize=8, color='#2E86AB')
            ax.set_xlabel(campo_x, fontsize=12, fontweight='bold')
            ax.set_ylabel(campo_y, fontsize=12, fontweight='bold')
            ax.set_title(f'Gráfico de Líneas: {campo_y} por {campo_x}', fontsize=14, fontweight='bold')
            plt.xticks(rotation=45, ha='right')
            ax.grid(True, alpha=0.3)
            
        elif tipo_grafico == "circular":
            colores = plt.cm.Set3(range(len(valores)))
            ax.pie(valores, labels=etiquetas, autopct='%1.1f%%', startangle=90, colors=colores)
            ax.set_title(f'Gráfico Circular: {campo_y} por {campo_x}', fontsize=14, fontweight='bold')
            
        elif tipo_grafico == "dispersion":
            indices = range(len(valores))
            scatter = ax.scatter(indices, valores, s=150, alpha=0.6, c=valores, cmap='plasma', edgecolors='black')
            ax.set_xticks(indices)
            ax.set_xticklabels(etiquetas, rotation=45, ha='right')
            ax.set_xlabel(campo_x, fontsize=12, fontweight='bold')
            ax.set_ylabel(campo_y, fontsize=12, fontweight='bold')
            ax.set_title(f'Gráfico de Dispersión: {campo_y} por {campo_x}', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            plt.colorbar(scatter, ax=ax)
        
        plt.tight_layout()
        
        # Integrar matplotlib con tkinter
        canvas = FigureCanvasTkAgg(fig, master=ventana_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame con botones
        frame_botones = tkinter.Frame(ventana_grafico)
        frame_botones.pack(pady=10)
        
        def guardar_grafico():
            from tkinter import filedialog
            archivo = filedialog.asksaveasfilename(defaultextension=".png",
                                           filetypes=[("PNG", "*.png"), ("PDF", "*.pdf"), 
                                                     ("SVG", "*.svg"), ("Todos", "*.*")])
            if archivo:
                fig.savefig(archivo, dpi=300, bbox_inches='tight')
                messagebox.showinfo("Éxito", f"Gráfico guardado en:\n{archivo}")
        
        btn_guardar = tkinter.Button(frame_botones, text="💾 Guardar Gráfico", 
                                     command=guardar_grafico, bg="blue", fg="white", 
                                     font=('Arial', 11), width=20, height=2)
        btn_guardar.pack(side="left", padx=5)
        
        btn_cerrar = tkinter.Button(frame_botones, text="✖ Cerrar", 
                                    command=ventana_grafico.destroy, bg="red", fg="white", 
                                    font=('Arial', 11), width=20, height=2)
        btn_cerrar.pack(side="left", padx=5)
        
    except sqlite3.Error as e:
        messagebox.showerror("Error de consulta", f"Error al obtener datos: {str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al crear gráfico: {str(e)}")



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
botonGrafico = tkinter.Button(raiz, text=textoGrafico, command= MostrarGrafico, relief="solid", bd=1, highlightbackground="black", highlightthickness=1)
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
    nombre VARCHAR(50),
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
    
    cursor.execute("INSERT INTO producto (id_Categoria, nombre, precio, stock) VALUES (1, 'Almendras', 2.50, 100)")
    cursor.execute("INSERT INTO producto (id_Categoria, nombre, precio, stock) VALUES (2, 'Pelotas', 1.80, 50)")
    cursor.execute("INSERT INTO producto (id_Categoria, nombre, precio, stock) VALUES (3, 'Toallitas', 8.99, 30)")
    
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
        trees_por_tabla[nombre_tabla] = tree
        
        # 7. Cargar los datos de la tabla
        cursor.execute(f"SELECT * FROM {nombre_tabla}")
        filas = cursor.fetchall()
        
        for fila in filas:
            tree.insert("", "end", values=fila)


LeerBaseDatos()
raiz.mainloop()

# Cerrar conexión al finalizar
conexion.close()