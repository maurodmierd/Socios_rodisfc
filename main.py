import tkinter as tk
from tkinter import ttk, messagebox
from src.WriterBuffer import WriterBuffer

def main():
    wb = WriterBuffer()
    root = tk.Tk()
    root.title("Xestión de Socios")
    root.geometry("550x750") # Tamaño inicial de la ventana

    # Estilo para los widgets de ttk
    style = ttk.Style(root)
    style.theme_use("clam") # Puedes probar otros temas como 'alt', 'default', 'classic'

    # --- Frame principal ---
    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # --- Frame para el formulario de entrada ---
    form_frame = ttk.LabelFrame(main_frame, text="Datos do Socio", padding="10")
    form_frame.pack(fill=tk.X, pady=10)

    # Labels y Entries para los datos del socio
    labels_texts = ["DNI:", "Nome:", "Apelidos:", "Poboacion:", "Enderezo:", "Telefono:", "Email:"]
    entries = {}

    for i, text in enumerate(labels_texts):
        label = ttk.Label(form_frame, text=text)
        label.grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
        entry = ttk.Entry(form_frame, width=40)
        entry.grid(row=i, column=1, padx=5, pady=5, sticky=tk.EW)
        entries[text.replace(":", "")] = entry
        
    form_frame.columnconfigure(1, weight=1)

    # --- Frame para la lista y botones ---
    list_frame = ttk.LabelFrame(main_frame, text="Socios a Engadir", padding="10")
    list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    listbox = tk.Listbox(list_frame, height=10)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

    scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.config(yscrollcommand=scrollbar.set)
    
    def clear_entries():
        for entry in entries.values():
            entry.delete(0, tk.END)

    def actualizar_listbox():
        listbox.delete(0, tk.END)
        for socio in wb.get_buffer():
            listbox.insert(tk.END, f"{socio['DNI']} - {socio['Nome']} {socio['Apelidos']}")

    def anadir_socio():
        socio_data = {key.replace(" ", ""): entry.get().strip() for key, entry in entries.items()}
        
        # Renombrar 'Enderezo' a 'Enderezo' para coincidir con WriterBuffer
        socio_data['Enderezo'] = socio_data.pop('Enderezo')

        for key, value in socio_data.items():
            if not value:
                messagebox.showerror("Error", f"O campo '{key}' non pode estar baleiro.")
                return
        
        wb.add(socio_data)
        actualizar_listbox()
        clear_entries()

    def eliminar_socio():
        seleccion = listbox.curselection()
        if not seleccion:
            messagebox.showerror("Error", "Non hai ningún socio seleccionado para eliminar.")
            return
        
        idx = seleccion[0]
        wb.pop(idx)
        actualizar_listbox()
        messagebox.showinfo("Información", f"Socio eliminado da lista.")

    def on_select(event):
        seleccion = listbox.curselection()
        if seleccion:
            idx = seleccion[0]
            socio = wb.get_buffer()[idx]
            clear_entries()
            entries['DNI'].insert(0, socio.get('DNI', ''))
            entries['Nome'].insert(0, socio.get('Nome', ''))
            entries['Apelidos'].insert(0, socio.get('Apelidos', ''))
            entries['Poboacion'].insert(0, socio.get('Poboacion', ''))
            entries['Enderezo'].insert(0, socio.get('Enderezo', ''))
            entries['Telefono'].insert(0, socio.get('Telefono', ''))
            entries['Email'].insert(0, socio.get('Email', ''))

    listbox.bind('<<ListboxSelect>>', on_select)

    # --- Frame para los botones de acción ---
    action_buttons_frame = ttk.Frame(main_frame)
    action_buttons_frame.pack(fill=tk.X, pady=5)

    btn_anadir = ttk.Button(action_buttons_frame, text="Engadir á Lista", command=anadir_socio)
    btn_anadir.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

    btn_eliminar = ttk.Button(action_buttons_frame, text="Eliminar da Lista", command=eliminar_socio)
    btn_eliminar.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

    btn_cancelar = ttk.Button(action_buttons_frame, text="Limpar Selección", command=clear_entries)
    btn_cancelar.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

    # --- Botón para guardar el buffer ---
    btn_guardar = ttk.Button(main_frame, text="Gardar Socios en Excel", command=wb.write)
    btn_guardar.pack(pady=10, fill=tk.X)

    root.mainloop()

if __name__ == "__main__":
    main()