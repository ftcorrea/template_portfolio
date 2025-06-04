import json
import urllib.request
import urllib.error
import tkinter as tk
from tkinter import messagebox


def consultar_cep():
    cep = cep_entry.get().strip().replace('-', '')
    if not cep.isdigit() or len(cep) != 8:
        messagebox.showerror("Erro", "CEP Inv\xe1lido")
        return

    url = f"https://viacep.com.br/ws/{cep}/json/"

    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.load(response)
    except urllib.error.URLError:
        messagebox.showerror("Erro", "N\xe3o foi poss\xedvel conectar ao servi\xe7o.")
        return

    if data.get("erro"):
        messagebox.showinfo("Resultado", "CEP Inv\xe1lido")
    else:
        cidade = data.get("localidade", "")
        estado = data.get("uf", "")
        messagebox.showinfo(
            "Resultado",
            f"CEP V\xe1lido!\nCidade: {cidade}\nEstado: {estado}"
        )


def main():
    global cep_entry

    root = tk.Tk()
    root.title("Consulta CEP")

    tk.Label(root, text="Digite o CEP:").pack(padx=10, pady=5)
    cep_entry = tk.Entry(root, width=20)
    cep_entry.pack(padx=10, pady=5)
    cep_entry.focus()

    verificar_btn = tk.Button(root, text="Verificar", command=consultar_cep)
    verificar_btn.pack(pady=10)

    root.bind('<Return>', lambda event: consultar_cep())
    root.mainloop()


if __name__ == "__main__":
    main()
