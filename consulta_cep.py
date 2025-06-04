import json
import urllib.request
import urllib.error
import tkinter as tk
from tkinter import messagebox


def _consulta_api(cep: str):
    """Consulta a API ViaCEP e retorna dicion\xc1rio com os dados."""
    url = f"https://viacep.com.br/ws/{cep}/json/"
    with urllib.request.urlopen(url, timeout=5) as response:
        return json.load(response)


def _validar_cep(cep: str) -> bool:
    """Valida se o CEP possui apenas d\xedgitos e exatamente oito caracteres."""
    return cep.isdigit() and len(cep) == 8


def consultar_cep():
    """Consulta o CEP digitado na interface Tkinter."""
    cep = cep_entry.get().strip().replace('-', '')
    if not _validar_cep(cep):
        messagebox.showerror("Erro", "CEP Inv\xe1lido")
        return

    try:
        data = _consulta_api(cep)
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


def consultar_cli():
    """Vers\xe3o de linha de comando para ambientes sem interface gr\xe1fica."""
    cep = input("Digite o CEP (apenas n\xfa meros): ").strip().replace('-', '')
    if not _validar_cep(cep):
        print("CEP Inv\xe1lido")
        return

    try:
        data = _consulta_api(cep)
    except urllib.error.URLError:
        print("N\xe3o foi poss\xedvel conectar ao servi\xe7o.")
        return

    if data.get("erro"):
        print("CEP Inv\xe1lido")
    else:
        cidade = data.get("localidade", "")
        estado = data.get("uf", "")
        print(f"CEP V\xe1lido! Cidade: {cidade} - Estado: {estado}")


def main():
    global cep_entry

    try:
        root = tk.Tk()
    except tk.TclError:
        # Ambiente sem display: usar modo CLI
        consultar_cli()
        return

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
