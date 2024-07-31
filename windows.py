import tkinter as tk

app = tk.Tk()
tk.Wm.wm_title(app, 'Administracion')

def saludar():
    print('hola')

tk.Button(
    app,
    bg='red',
    text='click',
    font=('courier',14),
    fg='blue',
    #command=lambda: print('saludar'),
    command=saludar
).pack(
    fill=tk.BOTH,
    expand=True,
)


app.geometry('1000x800') #dimenciones
app.configure(background='black') #fondo
app.mainloop()