arquivo_log = "acesso.log"

contagem_ips = {}

print (f"Lendo arquivo : {arquivo_log}")

with open(arquivo_log, "r") as arquivo:
    
    for linha in arquivo:
        
        partes = linha.split()
        ip = partes[0]
        
        if ip in contagem_ips:
            contagem_ips[ip] = contagem_ips[ip] + 1
        else:
            contagem_ips[ip] = 1 

print("=" * 40)
print("   RELATÓRIO DE ACESSOS POR IP")
print("=" * 40)

ips_ordenados = sorted(contagem_ips.items(), key=lambda x: x[1], reverse=True)

for ip, quantidade in ips_ordenados:
    barra = "█" * quantidade
    print(f"  {ip:<15} | {quantidade:>3}x | {barra}")
    
print("=" * 40)

total_acessos = sum(contagem_ips.values())
total_ips = len(contagem_ips)

print(f" Total de acessos: {total_acessos}")
print(f" IPs únicos: {total_ips}")

          
