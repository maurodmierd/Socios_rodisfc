import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from src.WriterBuffer import WriterBuffer
from src.excelWriter import write_to_excel

def main():
    wb = WriterBuffer()
    root = tk.Tk()
    root.title("Xestión de Socios")
    root.geometry("650x775")

    style = ttk.Style(root)
    style.theme_use("clam")

    # --- Notebook para las pestañas ---
    notebook = ttk.Notebook(root)
    notebook.pack(pady=10, padx=10, fill='both', expand=True)

    # --- Pestaña 1: Engadir Socios ---
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text='Engadir Socios')

    main_frame = ttk.Frame(tab1, padding="10")
    main_frame.pack(fill=tk.BOTH, expand=True)

    form_frame = ttk.LabelFrame(main_frame, text="Datos do Socio", padding="10")
    form_frame.pack(fill=tk.X, pady=10)

    labels_texts = ["DNI:", "Nome:", "Apelidos:", "Poboacion:", "Enderezo:", "Telefono:", "Email:"]
    entries = {}

    for i, text in enumerate(labels_texts):
        label = ttk.Label(form_frame, text=text)
        label.grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
        entry = ttk.Entry(form_frame, width=40)
        entry.grid(row=i, column=1, padx=5, pady=5, sticky=tk.EW)
        entries[text.replace(":", "")] = entry
        
    form_frame.columnconfigure(1, weight=1)

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

    action_buttons_frame = ttk.Frame(main_frame)
    action_buttons_frame.pack(fill=tk.X, pady=5)

    btn_anadir = ttk.Button(action_buttons_frame, text="Engadir á Lista", command=anadir_socio)
    btn_anadir.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

    btn_eliminar = ttk.Button(action_buttons_frame, text="Eliminar da Lista", command=eliminar_socio)
    btn_eliminar.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

    btn_cancelar = ttk.Button(action_buttons_frame, text="Limpar Selección", command=clear_entries)
    btn_cancelar.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

    btn_guardar = ttk.Button(main_frame, text="Gardar Socios en Excel", command=wb.write)
    btn_guardar.pack(pady=10, fill=tk.X)

    # --- Pestaña 2: Ver Socios ---
    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text='Ver Socios')

    db_frame = ttk.Frame(tab2, padding="10")
    db_frame.pack(fill='both', expand=True)

    tree_frame = ttk.Frame(db_frame)
    tree_frame.pack(fill='both', expand=True)

    tree = ttk.Treeview(tree_frame, columns=labels_texts, show='headings')
    
    for col in labels_texts:
        tree.heading(col, text=col)
        tree.column(col, anchor='w', width=80)

    tree.pack(side='left', fill='both', expand=True)

    tree_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree_scrollbar.pack(side='right', fill='y')
    tree.configure(yscrollcommand=tree_scrollbar.set)

    btn_refresh = ttk.Button(db_frame, text="Actualizar Lista de Socios", command=lambda: print('Holaaa'))
    btn_refresh.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()