import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
from tkinter import filedialog
import psycopg2
from fpdf import FPDF
from pyzbar.pyzbar import decode
from PIL import Image, ImageTk

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Sistema de Asistencia")
ventana.geometry("1200x600")
ventana.resizable(False, False)

# Crear tabla si no existe
def conectar_postgresql():
    conn = psycopg2.connect(
        database="asistencias",
        user="postgres",
        password="postgresql",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()


    cursor.execute('''
            CREATE TABLE IF NOT EXISTS asistencias (
                id SERIAL PRIMARY KEY,
                nombre TEXT,
                apellido TEXT,
                cedula TEXT,
                materia TEXT,
                fecha DATE,
                hora_e TIME,
                hora_s TIME,
                hora_r TIME,
                hora_t TIME,
                diferencial TIME
            )
        ''')
    return conn, cursor
conn, cursor = conectar_postgresql()

def generar_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(20, 8, 'Reporte de Asistencias', ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 7)
    
    encabezados = ['Nombre', 'Apellido', 'Cedula', 'Materia', 'Fecha', 'H-Entrada','H-Salida','H_Registro_QR','H-trabajada', 'H-Diferencial']
    for encabezado in encabezados:
        pdf.cell(20, 10, encabezado, 1, 0, 'L')
    pdf.ln()
    
    pdf.set_font("Arial", '', 7)
    cursor.execute("SELECT * FROM asistencias")
    resultados = cursor.fetchall()
    for fila in resultados:
        Nombre = str(fila[1]) 
        Apellido = str(fila[2]) 
        Cedula = str(fila[3]) 
        Materia = str(fila[4]) 
        Fecha = str(fila[5]) 
        H_Entrada = str(fila[6]) 
        H_Salida = str(fila[7]) 
        H_Registro_QR = str(fila[8]) 
        H_Trabajo = str(fila[9]) 
        H_Diferencial = str(fila[10])

        pdf.cell(20, 10, Nombre, 1, 0, 'L') 
        pdf.cell(20, 10, Apellido, 1, 0, 'L') 
        pdf.cell(20, 10, Cedula, 1, 0, 'L') 
        pdf.cell(20, 10, Materia, 1, 0, 'L') 
        pdf.cell(20, 10, Fecha, 1, 0, 'L') 
        pdf.cell(20, 10, H_Entrada, 1, 0, 'L') 
        pdf.cell(20, 10, H_Salida, 1, 0, 'L') 
        pdf.cell(20, 10, H_Registro_QR, 1, 0, 'L') 
        pdf.cell(20, 10, H_Trabajo, 1, 0, 'L') 
        pdf.cell(20, 10, H_Diferencial, 1, 0, 'L')
        
    pdf.output("reporte_asistencias.pdf")
    actualizar_el_pdf()
    
def actualizar_el_pdf():
    now = datetime.now()
    formatted_date = now.strftime("%d-%m-%Y")
    nuevo_nombre = f"reporte_asistencias_{formatted_date}.pdf"
    try:
        os.rename("reporte_asistencias.pdf", nuevo_nombre)
        print("El archivo ha sido renombrado a:", nuevo_nombre)
    except OSError as error:
        print(f"Error al renombrar el archivo: {error}")

def mostrar_registros():
    registros.delete(*registros.get_children())
    cursor.execute("SELECT id,nombre,apellido,cedula,materia,fecha,hora_e,hora_s,hora_r,diferencial FROM asistencias")
    resultados = cursor.fetchall()
    for fila in resultados:
        registros.insert("", tk.END, values=fila)
        
def Limpiar():
    cursor.execute("DELETE FROM asistencias")
    conn.commit()

def buscar():
    # Obtener el término de búsqueda del usuario
    busqueda_texto = entry_busqueda.get()

    # Limpiar la tabla de resultados antes de mostrar los nuevos resultados
    busqueda.delete(*busqueda.get_children())

    # Construir la consulta con un marcador de posición
    consulta = "SELECT id,nombre,cedula,materia,fecha,hora_t FROM asistencias WHERE materia LIKE %s"

    # Ejecutar la consulta con el parámetro
    cursor.execute(consulta, (f"%{busqueda_texto}%",))
    resultados = cursor.fetchall()

        # Mostrar los resultados en la tabla
    for fila in resultados:
        busqueda.insert("", tk.END, values=fila)

    # Construir la consulta SQL
def mostrar_informacion(): 
    informacion = """ Bienvenido al Sistema de Gestión de Asistencias
------------------------------------------------------------
Este sistema ha sido diseñado para facilitar el seguimiento de asistencias y gestionar la información de los docentes de manera eficiente.
A continuación, se presentan algunas de las características principales del sistema:
- Registro y consulta de asistencias por materia. 
- Cálculo automático de las horas trabajadas. 
- Creacion de pdf para el registro de asistencia 
- Interfaz amigable y fácil de usar basada en Tkinter. 
- Integración con bases de datos PostgreSQL para almacenamiento seguro y confiable. 
- Funcionalidades de búsqueda y filtrado para una gestión rápida y eficiente. 
Esperamos que este sistema sea de gran ayuda para la gestión de asistencias y contribuye a la organización y productividad de su institución.
------------------------------------------------------------
Instrucciones para manejar el sistema:
------------------------------------------------------------
-Consultar Asistencia: Aquí se muestra una pestaña para todos los datos relacionados al docente, presionando en (mostrar asistencia) se puede visualizar los datos, en (generar pdf) este hace un archivo .pdf con la fecha que se creo para el manejo de horario sencillo este cuenta con todos los datos de todos los profesores que se ha registrado, (limpiar datos) este elimina todo lo registrado para una nueva inserción de datos dando como limpio toda la base de datos.
-Consultar Horas de los Docentes: En esta pestaña se puede buscar los datos del docente mediante la materia, el resultado será el nombre, cedula, materia, fecha, horas trabajadas estos datos son fundamentales para saber si el docente asistió y cuantas horas laboró, en la parte de abajo en el cuadro ingresas la materia y le das en buscar y el resultado aparecerá arriba ya sea uno o mas resultados aparecerá.
-Lectura: Aquí se podrá registrar el qr este tiene que ser tipo img o png para un exitoso registro, se le da al botón de Seleccionar Imagen y se procede a buscar y después seleccionada es automático el registro y ya con eso se puede consultar en Consultar Asistencia.

    """ 
    texto_informacion.config(text=informacion)
# /////////////////////////////////////////////////////////////////////////////////////////////////////////

# /////////////////////////////////////////////////////////////////////////////////////////////////////////

# Crear un notebook para organizar las pestañas
notebook = ttk.Notebook(ventana)
notebook.pack(fill='both', expand=True)

pestaña_informacion = ttk.Frame(notebook)
notebook.add(pestaña_informacion, text='Informacion sobre el Sistema')

# Crear un marco para la tabla
marco_inf = tk.Frame(pestaña_informacion)
marco_inf.pack(fill='both', expand=True)


# Crear un widget Text para mostrar la información 
texto_informacion = tk.Label(marco_inf, wraplength=600,anchor="center",font=("Arial", 10)) 
texto_informacion.pack(padx=10, pady=10,fill='both') 
# Crear un botón para mostrar la información 
boton_mostrar = ttk.Button(marco_inf, text="Mostrar Información", command=mostrar_informacion) 
boton_mostrar.pack(pady=10)



# //////////////////////////////////////////////////////////////////////////


pestaña_consulta = ttk.Frame(notebook)
notebook.add(pestaña_consulta, text='Consultar Asistencias')

# Crear un marco para la tabla
marco_tabla = tk.Frame(pestaña_consulta)
marco_tabla.pack(fill='both', expand=True)

# Crear la tabla para mostrar los registros
registros = ttk.Treeview(marco_tabla, columns=("ID", "Nombre","Apellido", "Cedula","Materia", "Fecha", "Hora-Entrada","Hora-Salida","Hora-Registrada","Hora-Diferencial"), show="headings")
registros.heading("ID", text="ID", anchor="center")
registros.heading("Nombre", text="Nombre", anchor="center")
registros.heading("Apellido", text="Apellido", anchor="center")
registros.heading("Cedula", text="Cedula", anchor="center")
registros.heading("Materia", text="Materia", anchor="center")
registros.heading("Fecha", text="Fecha", anchor="center")
registros.heading("Hora-Entrada", text="Hora-Entrada", anchor="center")
registros.heading("Hora-Salida", text="Hora-Salida", anchor="center")
registros.heading("Hora-Registrada", text="Hora-Registro-QR", anchor="center")
registros.heading("Hora-Diferencial", text="Hora-Diferencial", anchor="center")
# Ajusta el ancho según sea necesario
registros.column("ID", width=5, anchor="center")  
registros.column("Nombre", width=50, anchor="center")
registros.column("Apellido", width=50, anchor="center")
registros.column("Cedula", width=50, anchor="center")
registros.column("Materia", width=50, anchor="center")
registros.column("Fecha", width=50, anchor="center")
registros.column("Hora-Entrada", width=50, anchor="center")
registros.column("Hora-Salida", width=50, anchor="center")
registros.column("Hora-Registrada", width=50, anchor="center")
registros.column("Hora-Diferencial", width=50, anchor="center")
registros.pack(fill="both", expand=True)
# Cambiar el color de fondo de las cabeceras
style = ttk.Style()
style.configure("Treeview.Heading", background="lightgrey")
# Crear un botón para actualizar la tabla
boton_actualizar_tabla = tk.Button(marco_tabla, text="Mostrar Asistencia", command=mostrar_registros, width=20)
boton_actualizar_tabla.pack()

# /////////////////////////////////////////////////////////////////////////////////////////////////////////


# Crear un marco para el botón de generar PDF
marco_pdf = tk.Frame(pestaña_consulta)
marco_pdf.pack()

boton_pdf = tk.Button(marco_pdf, text="Generar PDF", command=generar_pdf,width=20)
boton_pdf.pack()

marco_limpiar = tk.Frame(pestaña_consulta)
marco_limpiar.pack()

boton_limpiar = tk.Button(marco_pdf, text="Limpiar Datos", command=Limpiar, width=20)
boton_limpiar.pack()

# /////////////////////////////////////////////////////////////////////////////////////////////////////////

# Crear la pestaña de búsqueda

pestaña_buscar = ttk.Frame(notebook)
notebook.add(pestaña_buscar, text='Consultar Horas de los Docentes')

# Crear un marco para la tabla
marco_busqueda = tk.Frame(pestaña_buscar)
marco_busqueda.pack(fill='both', expand=True)

busqueda = ttk.Treeview(marco_busqueda, columns=("ID","Nombre","Cedula","Materia","Fecha",'Hora_t'), show="headings")

busqueda.heading("ID", text="ID", anchor="center")
busqueda.heading("Nombre", text="Nombre", anchor="center")
busqueda.heading("Cedula", text="Cedula", anchor="center")
busqueda.heading("Materia", text="Materia", anchor="center")
busqueda.heading("Fecha", text="Fecha", anchor="center")
busqueda.heading("Hora_t", text="Horas de trabajo", anchor="center")


busqueda.column("ID", width=10, anchor="center")  
busqueda.column("Nombre", width=50, anchor="center")
busqueda.column("Cedula", width=50, anchor="center")
busqueda.column("Materia", width=50, anchor="center")
busqueda.column("Fecha", width=50, anchor="center")
busqueda.column("Hora_t", width=50, anchor="center")

busqueda.pack(fill="both", expand=True)


style = ttk.Style()
style.configure("Treeview.Heading", background="lightgrey")

ry_busqueda = ttk.Label(pestaña_buscar, text="Ingresa la materia a buscar:")
ry_busqueda.pack()

entry_busqueda = ttk.Entry(pestaña_buscar)
entry_busqueda.pack()

boton_buscar = ttk.Button(pestaña_buscar, text="Buscar", command=buscar)
boton_buscar.pack()


# /////////////////////////////////////////////////////////////////////////////////////

imagen_pestaña = ttk.Frame(notebook)
notebook.add(imagen_pestaña, text="Lectura")


image_label = tk.Label(imagen_pestaña)
image_label.pack()

result_entry = tk.Entry(imagen_pestaña,state='disabled')
result_entry.pack()

def resize_image(image, new_size):
    """Resizes an image while maintaining aspect ratio.

    Args:
        image (PIL.Image): The image to resize.
        new_size (tuple): The desired maximum dimensions (width, height) for the resized image.

    Returns:
        PIL.Image: The resized image.
    """
    width, height = image.size
    max_width, max_height = new_size  # Assuming new_size is a tuple

    # Calculate the scale factor to maintain aspect ratio
    scale_factor = min(max_width / width, max_height / height)
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)

    return image.resize((new_width, new_height)) 

def insert_data(cursor, data):
    try:
        # Parametrizar la consulta para prevenir inyección SQL
        query = """
            INSERT INTO asistencias (nombre, apellido, cedula, materia, fecha, hora_e, hora_s, hora_r, hora_t, diferencial) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data['nombre'],
            data['apellido'],
            data['cedula'],
            data['materia'],
            data['fecha'],
            data['hora_e'],
            data['hora_s'],
            data['hora_r'],
            data['hora_t'],
            data['diferencial']
        )
        cursor.execute(query, values)
        conn.commit()
        messagebox.showinfo("Éxito", "Asistencia registrada correctamente")
    except psycopg2.Error as e:
        # Proporcionar un mensaje de error más específico
        messagebox.showerror("Error", f"Error al insertar datos: {e}")
        print(e)
    except Exception as e:
        # Capturar otras posibles excepciones
        messagebox.showerror("Error", f"Error inesperado: {e}")

def calculate_time_difference(start_time, end_time):
    """Calculates the time difference between two datetime objects.

    Args:
        start_time: The starting datetime object.
        end_time: The ending datetime object.

    Returns:
        datetime.timedelta: The time difference.
    """
    return end_time - start_time

def select_image():
    """
    Handles image selection, processing, and database operations.
    """
    file_path = filedialog.askopenfilename()

    if file_path:
        try:
            # Open the image with PIL
            img = Image.open(file_path)

            # Resize the image (adjust new_size based on your needs)
            resized_img = resize_image(img, (400, 300))  # Example size

            # Convert the image to Tkinter-compatible format
            img_tk = ImageTk.PhotoImage(resized_img)

            # Show the image in the label
            image_label.config(image=img_tk)
            image_label.image = img_tk  # Keep a reference

            # Decode the QR code (replace with your actual decoding function)
            decoded_objects = decode(resized_img) 

            if decoded_objects:
                result = decoded_objects[0].data.decode('utf-8')
                result_entry.insert(0, result)
                result_entry.delete(0, tk.END)
                print(result)

                # Aquí puedes procesar el resultado del QR para obtener los datos
                # Ejemplo: Suponiendo que 'result' contiene una lista de datos
                lista_datos = result.split(',') 
                if len(lista_datos) == 7:
                    hora_r = datetime.now().strftime('%H:%M:%S')
                    hora_rr = datetime.strptime(hora_r, "%H:%M:%S") 
                    hora_ee = datetime.strptime(lista_datos[5], "%H:%M:%S") 
                    hora_ss = datetime.strptime(lista_datos[6], "%H:%M:%S") 
                    hora_tt = hora_rr - hora_ss 
                    diferenciall = hora_rr - hora_ee # Calcular el total de segundos en las 
                    total_segundos_1 = abs(hora_tt.total_seconds()) 
                    total_segundos_2 = abs(diferenciall.total_seconds()) # Convertir a horas, minutos y segundos 
                    hora_tt_horas = int(total_segundos_1 // 3600) 
                    hora_tt_minutos = int((total_segundos_1 % 3600) // 60) 
                    hora_tt_segundos = int(total_segundos_1 % 60) 
                    diferencial_horas = int(total_segundos_2 // 3600) 
                    diferencial_minutos = int((total_segundos_2 % 3600) // 60) 
                    diferencial_segundos = int(total_segundos_2 % 60) # Imprimir resultados formateados 
                    print(f"Diferencia (hora_tt): {hora_tt_horas:02}:{hora_tt_minutos:02}:{hora_tt_segundos:02}")
                    print(f"Diferencia (diferenciall): {diferencial_horas:02}:{diferencial_minutos:02}:{diferencial_segundos:02}")
                    # Calcular el total de segundos en las diferencias y convertir a valores absolutos 
                    hora_t = f"{hora_tt_horas:02}:{hora_tt_minutos:02}:{hora_tt_segundos:02}"
                    diferencial = f"{diferencial_horas:02}:{diferencial_minutos:02}:{diferencial_segundos:02}"
                # Convertir la diferencia a un formato más legible (opcional
                    
                    data = {
                            'nombre': lista_datos[0],
                            'apellido': lista_datos[1],
                            'cedula': lista_datos[2],
                            'materia': lista_datos[3],
                            'fecha': lista_datos[4],
                            'hora_e': lista_datos[5],
                            'hora_s': lista_datos[6],
                            'hora_r': hora_rr,
                            'hora_t': hora_t,
                            'diferencial': diferencial
                        }
                    insert_data(cursor, data) 
                else:
                    print("Datos incompletos en el QR.")
            else:
                result_entry.delete(0, tk.END)
                result_entry.insert(0, "Código QR no encontrado")

        except (FileNotFoundError) as e:
            print(f"Error processing image: {e}")
            messagebox.showerror("Error", "Imagen no válida. Intente nuevamente.")


        
        
select_button = tk.Button(imagen_pestaña, text="Seleccionar Imagen", command=select_image)
select_button.pack()

# /////////////////////////////////////////////////////////////////////////////////////////////////////////


if __name__ == "__main__":
    ventana.mainloop()

