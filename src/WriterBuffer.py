import pandas as pd

class WriterBuffer:
    def __init__(self):
        self.buffer = pd.DataFrame(columns=['DNI', 'Nome', 'Apelidos', 'Poboacion', 'direccion', 'telefono', 'email'])

    def add(self, item):
        self.buffer.add(item)

    def pop(self, index):
        if 0 <= index < len(self.buffer):
            return self.buffer.pop(index)

    def clear(self):
        self.buffer.clear()

    def get_buffer(self):
        return self.buffer.values.tolist()

    def write(self,columns = ['DNI','Nome','Apelidos','Poboacion','direccion','telefono','email']):
        from src.excelWriter import write_to_excel
        write_to_excel(self.buffer, columns)
        self.clear()