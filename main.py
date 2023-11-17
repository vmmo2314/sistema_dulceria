import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import simpledialog
import psycopg2
from datetime import date

from inventario import delInventario


class interfaz:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1280x720")
        self.root.title("Dulceria de Caro :D")
        self.codigo_barras_entry = None
        self.treeview = ttk.Treeview(self.root, columns=('Producto', 'Cantidad', 'Precio'), show='headings', height=10)
        self.cargarTodo()

    def cargarTodo(self):
        # Establecer el tema del estilo
        self.style = ttk.Style()
        self.style.theme_use("xpnative")

        # Estilo para el encabezado
        self.style.configure("Treeview.Heading", font=("Helvetica", 18, "bold"))

        # Estilo para las filas alternas
        self.style.configure("Treeview", font=("Helvetica", 12), rowheight=35, background="#f5f5f5")
        self.style.map("Treeview", background=[("selected", "#347083")])

        ##Conexion a la base de datos
        self.records = []
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

            # Aquí iría tu consulta SQL, por ejemplo:
            # self.cursor.execute("SELECT * FROM tu_tabla")

            # Obtener los registros
            self.records = self.cursor.fetchall()

        except (Exception, psycopg2.Error) as error:
            print("Error al conectar a la base de datos:", error)

        finally:
            # Cerrar el cursor y la conexión si están definidos
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()

    def mainMenu(self):
        Menu_label = tk.Label(self.root, text="Dulcería", font=("Helvetica", 15))
        Menu_label.place(relx=0.5, rely=.05, anchor=tk.CENTER)
        self.clienteActual()
        self.cuadro_codigo_de_barras()
        self.botonesSuperiores()
        self.treeview.place(relx=0.70, rely=0.5, anchor=tk.CENTER)

        # Configurar las columnas
        self.treeview.heading('Producto', text='Producto')
        self.treeview.heading('Cantidad', text='Cantidad')
        self.treeview.heading('Precio', text='Precio')
        self.root.mainloop()

    def clienteActual(self):
        cliente_ = tk.Label(self.root, text="Atendiendo a cliente ", width=30, font=("Helvetica", 15))
        cliente_.place(relx=0.1, rely=.05, anchor=tk.CENTER)

    def cuadro_codigo_de_barras(self):
        cuadro_frame = ttk.Frame(self.root, padding=(5, 5, 5, 5), style="My.TFrame")
        cuadro_frame.place(relx=0.20, rely=0.5, anchor=tk.CENTER)

        codigo_barras_label = tk.Label(cuadro_frame, text="Código de Barras", font=("Helvetica", 18))
        codigo_barras_label.grid(row=2, column=1, padx=5, pady=5)

        self.codigo_barras_entry = tk.Entry(cuadro_frame, font=("Helvetica", 45), width=10)
        self.codigo_barras_entry.grid(row=0, column=1, padx=5, pady=5)

        # Vincular la tecla Enter al evento 'listo'
        self.codigo_barras_entry.bind('<Return>', self.listo)

    def listo(self, event):
        # Este método se ejecutará cuando se presiona Enter
        # Realizar la consulta a la base de datos para obtener nombre y precio
        producto_codigo_barras = self.codigo_barras_entry.get()
        nombre, precio = self.obtener_datos_producto(producto_codigo_barras)

        if nombre != "Producto no encontrado":
            # Si el producto existe, solicitar la cantidad
            cantidad_productos = simpledialog.askinteger("Cantidad de productos", f"Ingrese la cantidad de {nombre}s:",
                                                         initialvalue=1)

            if cantidad_productos is not None:
                print(f"Listo! Realizar acciones aquí. Cantidad de productos: {cantidad_productos}, "
                      f"Producto: {nombre}, Precio: {precio}")

                # Agregar el producto a la Treeview con la cantidad, nombre y precio
                self.treeview.insert('', 'end', values=(nombre, cantidad_productos, precio))

                # Limpiar el cuadro de entrada
                self.codigo_barras_entry.delete(0, 'end')
                self.subTotal()
        else:
            # Producto no encontrado, mostrar mensaje de error
            tk.messagebox.showerror("Error", "Producto no encontrado en la base de datos.")

    def obtener_datos_producto(self, codigo_barras):
        try:
            # Parámetros de conexión
            connection = psycopg2.connect(
                user="postgres",
                password="usuario",
                host="localhost",
                port="5432",
                database="dulceria_sistema"
            )

            # Crear un cursor para ejecutar consultas
            cursor = connection.cursor()

            # Realizar la consulta SQL para obtener el nombre y precio del producto
            consulta = f"SELECT nombre, precio FROM productos WHERE id_producto = '{codigo_barras}'"
            cursor.execute(consulta)
            resultado = cursor.fetchone()

            if resultado:
                nombre, precio = resultado
                return nombre, precio
            else:
                return "Producto no encontrado", 0

        except (Exception, psycopg2.Error) as error:
            print("Error al obtener datos del producto:", error)
            return "Error", 0

        finally:
            # Cerrar el cursor y la conexión si están definidos
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def botonesSuperiores(self):
        # Crear un botón redondo
        self.boton1 = tk.Button(self.root, text="Inventario", font=("Helvetica", 12), command=self.mostrarVentanaInventario, relief="solid")
        self.boton1.place(relx=0.90, rely=0.05, anchor=tk.CENTER)

    def mostrar_inventario(self):
        print("Mostrar inventario aquí.")

    def subTotal(self):
        # Calcular el subtotal sumando los valores de la columna 'Precio' en el treeview
        subtotal = 0
        for item in self.treeview.get_children():
            precio = float(self.treeview.item(item, 'values')[2])
            cantidad = float(self.treeview.item(item, 'values')[1])
            subtotal += precio * cantidad

        # Redondear el subtotal a dos decimales
        subtotal = round(subtotal, 2)

        # Mostrar el subtotal en un Label
        self.subtotal_label = tk.Label(self.root, text=f"Subtotal: {subtotal:.2f}", font=("Helvetica", 45))
        self.subtotal_label.place(relx=0.70, rely=0.85, anchor=tk.CENTER)
        self.cobrar()
    def cobrar(self):
        self.label_cobrar = tk.Button(self.root, text="Cobrar", font=("Helvetica", 20), command=self.limpiar_datos)
        self.label_cobrar.place(relx=0.95, rely=0.90, anchor=tk.CENTER)

    def limpiar_datos(self):
        # Obtener la fecha actual
        fecha_actual = date.today()

        # Insertar datos en la tabla Venta
        total_venta = self.calcular_total_venta()

        # Insertar datos en la tabla Detalle_Venta
        self.insertar_detalle_venta()

        # Limpiar la Treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        # Limpiar el cuadro de código de barras
        self.codigo_barras_entry.delete(0, 'end')

        # Limpiar el subtotal
        for widget in self.root.winfo_children():
            if "subtotal" in str(widget).lower():
                widget.destroy()
        self.subtotal_label.destroy()
        self.label_cobrar.destroy()

    def calcular_total_venta(self):
        subtotal = 0
        for item in self.treeview.get_children():
            precio = float(self.treeview.item(item, 'values')[2])
            cantidad = float(self.treeview.item(item, 'values')[1])
            subtotal += precio * cantidad
        return round(subtotal, 2)

    def insertar_venta(self, fecha_venta, total_venta):
        try:
            connection = psycopg2.connect(
                user="postgres",
                password="usuario",
                host="localhost",
                port="5432",
                database="dulceria_sistema"
            )
            cursor = connection.cursor()

            # Insertar en la tabla Venta
            cursor.execute("INSERT INTO Venta (fecha_venta, total_venta) VALUES (%s, %s) RETURNING id_venta",
                           (fecha_venta, total_venta))
            id_venta = cursor.fetchone()[0]
            connection.commit()

            return id_venta

        except (Exception, psycopg2.Error) as error:
            print("Error al insertar en la tabla Venta:", error)

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def insertar_detalle_venta(self):
        try:
            connection = psycopg2.connect(
                user="postgres",
                password="usuario",
                host="localhost",
                port="5432",
                database="dulceria_sistema"
            )
            cursor = connection.cursor()

            # Obtener el id_venta y el total_venta
            id_venta = self.insertar_venta(date.today(), self.calcular_total_venta())

            # Iterar sobre los elementos de self.treeview
            for item in self.treeview.get_children():
                nombre_producto = self.treeview.item(item, 'values')[0]
                cantidad = float(self.treeview.item(item, 'values')[1])
                precio_unitario = float(self.treeview.item(item, 'values')[2])
                subtotal = cantidad * precio_unitario

                # Obtener el id_producto correspondiente al nombre del producto
                cursor.execute("SELECT id_producto, cantidad FROM productos WHERE nombre = %s", (nombre_producto,))
                result = cursor.fetchone()

                if result:
                    id_producto, cantidad_actual = result

                    # Verificar si hay suficientes productos en stock
                    if cantidad_actual >= cantidad:
                        # Descontar la cantidad comprada de la cantidad en la tabla de productos
                        nueva_cantidad = cantidad_actual - cantidad
                        cursor.execute("UPDATE productos SET cantidad = %s WHERE id_producto = %s",
                                       (nueva_cantidad, id_producto))
                        connection.commit()

                        # Insertar en la tabla Detalle_Venta
                        cursor.execute("INSERT INTO Detalle_Venta (id_venta, id_producto, cantidad, subtotal) "
                                       "VALUES (%s, %s, %s, %s)", (id_venta, id_producto, cantidad, subtotal))
                        connection.commit()
                    else:
                        print(f"Error: No hay suficientes unidades de {nombre_producto} en stock.")
                else:
                    print(f"Error: No se encontró el id_producto para el producto {nombre_producto}")

        except (Exception, psycopg2.Error) as error:
            print("Error al insertar en la tabla Detalle_Venta:", error)

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def mostrarVentanaInventario(self):
        myVentana = delInventario()
        myVentana.pantallaPrincipal()



myInterfaz = interfaz()
myInterfaz.mainMenu()
