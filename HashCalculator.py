import hashlib
import os
import sys

def calcular_sha256(caminho: str) -> str:
    sha256 = hashlib.sha256()
    
    with open(caminho, "+rb") as arquivo:
        while True:
            bloco = arquivo.read(8192)
            if not bloco:
                break
            sha256.update(bloco)
            
    return sha256.hexdigest()


def formatar_bytes(num_bytes: int) -> str:
    for unidade in ("B", "KB", "MB", "GB", "TB"):
        if num_bytes < 1024:
            return f"{num_bytes:.1f} {unidade}"
        num_bytes /= 1024
    
    return f"{num_bytes:.1f} PB"


def escanear_pasta(pasta: str) -> None:
    if not os.path.isdir(pasta):
        print(f"Erro: '{pasta}' não é umas pasta válida")

    nomes = sorted(os.listdir(pasta))
    arquivos = []
    
    for nome in nomes:
        caminho = os.path.join(pasta, nome)
        if os.path.isfile(caminho):
            arquivos.append(caminho)
    
    if not arquivos:
        print("Nenhum arquivo encontrado na pasta.")
        return
    
    caminho_absoluto = os.path.abspath(pasta)
    print(f"\n Pasta: {caminho_absoluto}")
    print(f"   Arquivos : {len(arquivos)}")
    print("-" * 78)
    
    
    for caminho in arquivos:
        nome = os.path.basename(caminho)
        tamanho = os.path.getsize(caminho)
        hash256 = calcular_sha256(caminho)
        
        print(f" {hash256} {formatar_bytes(tamanho):>10} {nome}")
        
    print("-" * 78)
    print(f" {len(arquivos)} arquivos processados.")
    
if __name__ == "__main__":

    if len(sys.argv) > 1:
        pasta = sys.argv[1]
    else:
        pasta = input("Caminho da pasta: ").strip()

    escanear_pasta(pasta)
    