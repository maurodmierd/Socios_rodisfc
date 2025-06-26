import tkinter as tk
from tkinter import messagebox
from src.WriterBuffer import WriterBuffer

def main():
    wb = WriterBuffer()

    root = tk.Tk()
    root.title("Xestión de Socios")
    
    label = tk.Label(root, text="Engade un novo socio")


    label.pack(pady=20)
    
    entryDNI = tk.Entry(root)
    entryDNI.pack(pady=10)

    entryNombre = tk.Entry(root)
    entryNombre.pack(pady=10)

    entryApelidos = tk.Entry(root)
    entryApelidos.pack(pady=10)

    entryPoboacion = tk.Entry(root)
    entryPoboacion.pack(pady=10)

    entryTelefono = tk.Entry(root)
    entryTelefono.pack(pady=10)

    entryEmail = tk.Entry(root)
    entryEmail.pack(pady=10)

    entryDireccion = tk.Entry(root)
    entryDireccion.pack(pady=10)
    

    # Frame para la lista y botones
    frame_lista = tk.Frame(root)
    frame_lista.pack(pady=10)

    # Listbox para mostrar los socios en el buffer
    listbox = tk.Listbox(frame_lista, width=40)
    listbox.pack(side=tk.LEFT, padx=5)

    # Scrollbar para la listbox
    scrollbar = tk.Scrollbar(frame_lista, orient="vertical", command=listbox.yview)
    scrollbar.pack(side=tk.LEFT, fill=tk.Y)
    listbox.config(yscrollcommand=scrollbar.set)

    def actualizar_listbox():
        listbox.delete(0, tk.END)
        for socio in wb.get_buffer():
            # Mostrar una representación legible del socio
            listbox.insert(tk.END, f"{socio['DNI']} - {socio['Nombre']} {socio['Apelidos']}")
            listbox.insert(tk.END, socio)
    def anadir_socio():
        dni = entryDNI.get().strip()
        if not dni:
            messagebox.showerror("Error", "O DNI non pode estar baleiro.")
            return
        nombre = entryNombre.get().strip()
        if not nombre:
            messagebox.showerror("Error", "O nome non pode estar baleiro.")
            return
        apelidos = entryApelidos.get().strip()
        if not apelidos:
            messagebox.showerror("Error", "Os apelidos non poden estar baleiros.")
            return
        poboacion = entryPoboacion.get().strip()
        if not poboacion:
            messagebox.showerror("Error", "A poboación non pode estar baleira.")
            return
        direccion = entryDireccion.get().strip()
        if not direccion:
            messagebox.showerror("Error", "A dirección non pode estar baleira.")
            return
        telefono = entryTelefono.get().strip()
        if not telefono:
            messagebox.showerror("Error", "O teléfono non pode estar baleiro.")
            return
        email = entryEmail.get().strip()
        if not email:
            messagebox.showerror("Error", "O email non pode estar baleiro.")
            return
        
        wb.add(item={
            'DNI': dni,
            'Nombre': nombre,
            'Apelidos': apelidos,
            'Poboacion': poboacion,
            'Direccion': direccion,
            'Telefono': telefono,
            'Email': email
        })
        actualizar_listbox()

    def eliminar_socio():
        seleccion = listbox.curselection()
        if not seleccion:
            messagebox.showerror("Error", "Non hai ningún socio seleccionado para eliminar.")
            return
        idx = seleccion[0]
        socio = wb.get_buffer()[idx]
        wb.pop(idx)
        messagebox.showinfo("Información", f"Socio {socio['DNI']} eliminado correctamente.")
        actualizar_listbox()

    # Función para cancelar selección
    def cancelar_seleccion():
        listbox.selection_clear(0, tk.END)
        entryDNI.delete(0, tk.END)
        entryNombre.delete(0, tk.END)
        entryApelidos.delete(0, tk.END)
        entryPoboacion.delete(0, tk.END)
        entryDireccion.delete(0, tk.END)
        entryTelefono.delete(0, tk.END)
        entryEmail.delete(0, tk.END)

    # Función para guardar los datos del buffer (aquí solo imprime, puedes cambiarlo)
    def guardar_buffer():
        print("Guardando socios:", wb.get_buffer())
        wb.clear()
        actualizar_listbox()

    # Al seleccionar un elemento, mostrarlo en el entry
    def on_select(event):
        seleccion = listbox.curselection()
        if seleccion:
            idx = seleccion[0]
            socio = wb.get_buffer()[idx]
            entryDNI.delete(0, tk.END)
            entryDNI.insert(0, socio['DNI'])
            entryNombre.delete(0, tk.END)
            entryNombre.insert(0, socio['Nombre'])
            entryApelidos.delete(0, tk.END)
            entryApelidos.insert(0, socio['Apelidos'])
            entryPoboacion.delete(0, tk.END)
            entryPoboacion.insert(0, socio['Poboacion'])
            entryDireccion.delete(0, tk.END)
            entryDireccion.insert(0, socio['Direccion'])
            entryTelefono.delete(0, tk.END)
            entryTelefono.insert(0, socio['Telefono'])
            entryEmail.delete(0, tk.END)
            entryEmail.insert(0, socio['Email'])

    listbox.bind('<<ListboxSelect>>', on_select)

    # Botones
    frame_botones = tk.Frame(root)
    frame_botones.pack(pady=10)

    btn_anadir = tk.Button(frame_botones, text="Añadir", command=anadir_socio)
    btn_anadir.grid(row=0, column=0, padx=5)

    btn_eliminar = tk.Button(frame_botones, text="Eliminar", command=eliminar_socio)
    btn_eliminar.grid(row=0, column=2, padx=5)

    btn_cancelar = tk.Button(frame_botones, text="Cancelar", command=cancelar_seleccion)
    btn_cancelar.grid(row=0, column=3, padx=5)

    btn_guardar = tk.Button(root, text="Guardar buffer", command=guardar_buffer)
    btn_guardar.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()