import pandas as pd
import openpyxl

def write_to_excel(df):
    try:
        df.to_excel("output\\socios.xlsx", index=False, engine='openpyxl')
        print("Datos gardados no arquivo socios.xlsx")
    except Exception as e:
        print(f"Erro ao gardar o arquivo: {e}")

def main():
    print("Este é un módulo de escritura, non está pensado para ser executado directamente.")

if __name__ == "__main__":
    main()