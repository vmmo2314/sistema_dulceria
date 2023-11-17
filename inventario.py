import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import psycopg2

class delInventario:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.geometry("1280x720")
        self.root.title("Inventario")

        self.treeInventario = ttk.Treeview(self.root, columns=("Codigo","Producto", "Descripcion", "Cantidad", "Precio"), show="headings")

        # Establecer el tema del estilo
        self.style = ttk.Style()
        self.style.theme_use("xpnative")  # Puedes cambiar "clam" a otros temas como "default", "alt", "classic", etc.
        self.style.configure("TButton", relief="flat", font=("Helvetica", 16))
        # Estilo para el encabezado
        self.style.configure("Treeview.Heading", font=("Helvetica", 18, "bold"))

        self.style.configure("BotonListo.TButton", font=("Helvetica", 25), width=10, background="green")

        # Estilo para las filas
        self.style.configure("Treeview", font=("Helvetica", 12), rowheight=55, background="#f5f5f5")
        self.style.map("Treeview", background=[("selected", "#347083")])

        # Establecer la conexión a la base de datos
        try:
            # Parámetros de conexión
            self.connection = psycopg2.connect(
                user="postgres",
                password="usuario",
                host="localhost",
                port="5432",
                database="dulceria_sistema"
            )
            # Crear un cursor para ejecutar consultas
            self.cursor = self.connection.cursor()
        except Exception as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {str(e)}")
            self.root.destroy()


    def pantallaPrincipal(self):
        self.treeInventario.heading("Codigo", text="Codigo")
        self.treeInventario.heading("Producto", text="Producto")
        self.treeInventario.heading("Descripcion", text="Descripcion")
        self.treeInventario.heading("Cantidad", text="Cantidad")
        self.treeInventario.heading("Precio", text="Precio")

        self.treeInventario.place(relx=0.5, rely=0.5, width=1100, height=400, anchor=tk.CENTER)
        self.cargarProductos()
        self.botones()

    def cargarProductos(self):
        # Obtener datos de la base de datos en lugar de usar una lista estática
        try:
            self.cursor.execute("SELECT id_producto, nombre, descripcion, cantidad, precio FROM productos")
            productos = self.cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error al cargar productos", f"No se pudieron cargar los productos: {str(e)}")
            return

        # Limpiar el Treeview antes de cargar los nuevos datos
        for item in self.treeInventario.get_children():
            self.treeInventario.delete(item)

        # Insertar datos en el Treeview desde la base de datos
        for producto in productos:
            self.treeInventario.insert("", "end", values=producto)


    def botones(self):
        self.style.configure("TButton", relief="flat", font=("Helvetica", 16))
        self.aniadir = ttk.Button(self.root, text="Añadir producto", style="TButton", width=20, command=self.nuevoProducto)
        self.aniadir.place(relx=0.3, rely=0.9, anchor=tk.CENTER)

        self.modificar = ttk.Button(self.root, text="Modificar producto", style="TButton", width=20, command=self.modificarProducto)
        self.modificar.place(relx=0.6, rely=0.9, anchor=tk.CENTER)

    def nuevoProducto(self):
        nuevo_producto_window = tk.Toplevel(self.root)
        nuevo_producto_window.geometry("400x300")
        nuevo_producto_window.title("Nuevo Producto")

        # Entry widgets for product details
        codigo_label = tk.Label(nuevo_producto_window, text="Código:")
        codigo_label.pack()

        codigo_entry = tk.Entry(nuevo_producto_window)
        codigo_entry.pack()

        nombre_label = tk.Label(nuevo_producto_window, text="Nombre:")
        nombre_label.pack()

        nombre_entry = tk.Entry(nuevo_producto_window)
        nombre_entry.pack()

        descripcion_Label = tk.Label(nuevo_producto_window, text="Descripcion:")
        descripcion_Label.pack()

        descripcion_Label_entry = tk.Entry(nuevo_producto_window)
        descripcion_Label_entry.pack()

        cantidad_label = tk.Label(nuevo_producto_window, text="Cantidad:")
        cantidad_label.pack()

        cantidad_entry = tk.Entry(nuevo_producto_window)
        cantidad_entry.pack()

        precio_label = tk.Label(nuevo_producto_window, text="Precio:")
        precio_label.pack()

        precio_entry = tk.Entry(nuevo_producto_window)
        precio_entry.pack()

        # Button to save the new product
        guardar_button = tk.Button(nuevo_producto_window, text="Guardar", command=lambda: self.guardarNuevoProducto(
            codigo_entry.get(), nombre_entry.get(), descripcion_Label_entry.get(), cantidad_entry.get(), precio_entry.get(), nuevo_producto_window))
        guardar_button.pack()

    def modificarProducto(self):
        selected_item = self.treeInventario.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un producto para modificar.")
            return

        # Extract data from the selected item
        values = self.treeInventario.item(selected_item, 'values')

        # Set default values in case they are not available
        codigo = values[0] if values and len(values) > 0 else ""
        nombre = values[1] if values and len(values) > 1 else ""
        descripcion = values[2] if values and len(values) > 2 else ""
        cantidad = values[3] if values and len(values) > 3 else ""
        precio = values[4] if values and len(values) > 4 else ""


        # Consultar el código del producto basándose en el nombre
        try:
            self.cursor.execute("SELECT id_producto FROM productos WHERE id_producto = %s", (codigo,))
            codigo_result = self.cursor.fetchone()
            codigo = codigo_result[0] if codigo_result else ""
        except Exception as e:
            messagebox.showerror("Error al obtener código", f"No se pudo obtener el código del producto: {str(e)}")
            return

        # Create a new window or dialog for modifying product details
        modificar_producto_window = tk.Toplevel(self.root)
        modificar_producto_window.geometry("400x300")
        modificar_producto_window.title("Modificar Producto")

        # Entry widgets for product details
        codigo_label = tk.Label(modificar_producto_window, text="Código:")
        codigo_label.pack()

        codigo_entry = tk.Entry(modificar_producto_window)
        codigo_entry.insert(0, codigo)
        codigo_entry.pack()

        nombre_label = tk.Label(modificar_producto_window, text="Nombre:")
        nombre_label.pack()

        nombre_entry = tk.Entry(modificar_producto_window)
        nombre_entry.insert(0, nombre)
        nombre_entry.pack()

        descripcion_Label = tk.Label(modificar_producto_window, text="Descripcion:")
        descripcion_Label.pack()

        descripcion_entry = tk.Entry(modificar_producto_window)
        descripcion_entry.insert(0, descripcion)
        descripcion_entry.pack()

        cantidad_label = tk.Label(modificar_producto_window, text="Cantidad:")
        cantidad_label.pack()

        cantidad_entry = tk.Entry(modificar_producto_window)
        cantidad_entry.insert(0, cantidad)
        cantidad_entry.pack()

        precio_label = tk.Label(modificar_producto_window, text="Precio:")
        precio_label.pack()

        precio_entry = tk.Entry(modificar_producto_window)
        precio_entry.insert(0, precio)
        precio_entry.pack()

        # Button to save the modified product
        guardar_button = tk.Button(modificar_producto_window, text="Guardar",
                                   command=lambda: self.guardarProductoModificado(
                                       selected_item, codigo_entry.get(), nombre_entry.get(), descripcion_entry.get(),cantidad_entry.get(),
                                       precio_entry.get(), modificar_producto_window))
        guardar_button.pack()

    def guardarProductoModificado(self, selected_item, codigo, nombre, descripcion, cantidad, precio, window):
        try:
            # Verificar si el nuevo nombre ya existe para otro producto
            self.cursor.execute(
                "SELECT COUNT(*) FROM productos WHERE nombre = %s AND id_producto != %s",
                (nombre, codigo))
            producto_existente = self.cursor.fetchone()[0]

            if producto_existente > 0:
                messagebox.showwarning("Nombre de Producto Existente",
                                       f"El nombre '{nombre}' ya está en uso por otro producto.")
                return
            else:
                # Actualizar el producto en la base de datos
                self.cursor.execute(
                    "UPDATE productos SET nombre = %s, descripcion = %s, cantidad = %s, precio = %s WHERE id_producto = %s",
                    (nombre, descripcion, cantidad, precio, codigo))
                self.connection.commit()

                # Imprimir la información (puedes eliminar esto en la versión final)
                print(
                    f"Producto modificado: Código: {codigo}, Nombre: {nombre}, Descripcion: {descripcion}, Cantidad: {cantidad}, Precio: {precio}")

                # Actualizar el Treeview con la información modificada
                self.treeInventario.item(selected_item, values=(codigo, nombre, descripcion, cantidad, precio))

        except Exception as e:
            messagebox.showerror("Error al modificar producto", f"No se pudo modificar el producto: {str(e)}")

        # Cerrar la ventana de modificar producto
        window.destroy()

    def guardarNuevoProducto(self, codigo, nombre, descripcion, cantidad, precio, window):
        try:
            # Verificar si el producto ya existe en la base de datos
            #se verifica el id
            self.cursor.execute("SELECT COUNT(*) FROM productos WHERE id_producto = %s", (codigo,))
            producto_existente = self.cursor.fetchone()[0]

            if producto_existente > 0:
                messagebox.showwarning("Producto Existente", f"El producto '{nombre}' ya existe en el inventario.")
                return
            else:
                # Insertar el nuevo producto en la base de datos
                self.cursor.execute(
                    "INSERT INTO productos (id_producto, nombre, descripcion ,cantidad, precio) VALUES (%s, %s, %s, %s, %s)",
                    (codigo, nombre, descripcion, cantidad, precio))
                self.connection.commit()

                # Imprimir la información (puedes eliminar esto en la versión final)
                print(f"Producto añadido: Código: {codigo}, Nombre: {nombre}, Descripcion: {descripcion}, Cantidad: {cantidad}, Precio: {precio}")

                # Actualizar el Treeview con el nuevo producto
                self.treeInventario.insert("", "end", values=(codigo, nombre, descripcion, cantidad, precio))

        except Exception as e:
            messagebox.showerror("Error al guardar producto", f"No se pudo guardar el producto: {str(e)}")

        # Cerrar la ventana de nuevo producto
        window.destroy()

