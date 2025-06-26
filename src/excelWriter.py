import pandas as pd


def write_to_excel(df):
    df.to_excel("socios.xlsx", index=False, engine='openpyxl')
    print("Datos gravados no arquivo socios.xlsx")

def main():
    print("Hola")

if __name__ == "__main__":
    main()