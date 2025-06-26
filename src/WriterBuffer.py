import pandas as pd
from tkinter import messagebox

class WriterBuffer:
    def __init__(self):
        self.columns = ['DNI', 'Nome', 'Apelidos', 'Poboacion', 'Enderezo', 'Telefono', 'Email']
        self.buffer = pd.DataFrame(columns=self.columns)

    def add(self, item):
        # Convertir el item (diccionario) a un DataFrame de una fila
        new_row_df = pd.DataFrame([item])
        # Concatenar el nuevo df con el buffer existente
        self.buffer = pd.concat([self.buffer, new_row_df], ignore_index=True)

    def pop(self, index):
        if 0 <= index < len(self.buffer):
            # Eliminar la fila por su índice
            self.buffer = self.buffer.drop(self.buffer.index[index]).reset_index(drop=True)

    def clear(self):
        # Reiniciar el buffer a un DataFrame vacío con las columnas correctas
        self.buffer = pd.DataFrame(columns=self.columns)
        messagebox.showinfo("Gardado", "Os socios foron gardados correctamente e a lista foi limpada.")


    def get_buffer(self):
        # Devolver el buffer como una lista de diccionarios
        return self.buffer.to_dict('records')

    def write(self):
        from src.excelWriter import write_to_excel
        if not self.buffer.empty:
            write_to_excel(self.buffer)
            self.clear()
        else:
            messagebox.showwarning("Aviso", "Non hai socios na lista para gardar.")