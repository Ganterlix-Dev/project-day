from tkinter import *
from tkinter import ttk
import random
import time
import datetime
from tkinter import messagebox
import mysql.connector
import tkinter as tk 

class Ventana:
    def __init__(self,root):
        self.root=root
        self.root.title('Manejo de sistema')
        self.root.geometry('800x600')
        
        lbltitle=Label(self.root,bd=20,relief=RIDGE,text='manage students',fg='red',bg='white',font=('times new roman',30,'bold'))
        lbltitle.pack(side=TOP,fill=X)
        

root=Tk()
ob=Ventana(root)
root.mainloop()


# app = tk.Tk()
# tk.Wm.wm_title(app, 'Administracion')
# frm = ttk.Frame(app, padding=10)


# app.geometry('1000x800') #dimenciones
# app.configure(background='black') #fondo
# app.mainloop()

# def saludar():
#     print('hola')

# tk.Button(
#     app,
#     bg='red',
#     text='click',
#     font=('courier',14),
#     fg='blue',
#     #command=lambda: print('saludar'),
#     command=saludar
# ).pack(
#     fill=tk.BOTH,
#     expand=True,
# )
# tk.Button(app,
#         text="Quit",
#         command=app.destroy
#         ).pack(
#             fill=tk.BOTH,
#             expand=True,)