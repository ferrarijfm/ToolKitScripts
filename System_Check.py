import os
import sys
import platform 
import psutil
from datetime import datetime

def formatar_bytes(num_bytes: int) -> str:
    for unidade in ("B", "KB", "MB", "GB", "TB"):
        if num_bytes < 1024:
            return f"{num_bytes:.1f} {unidade}"
        num_bytes /= 1024
    
    return f"{num_bytes:.1f} PB"


def percentual_uso(percentual: float) -> str:
    return f"{percentual:.1f}%"


def status(percentual: float) -> str:
    if percentual >= 95:
        return 'CRITICO'
    elif percentual >= 80:
        return 'ATENÇÂO'
    else:
        return 'OK'


def info_sistema() -> dict:
    
    hostname = platform.node()
    so = f"{platform.system()} {platform.release()}"
    arquitetura = platform.machine()
    boot = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - boot
    
    dias = uptime.days
    horas, resto = divmod(uptime.seconds, 3600)
    minutos, _ = divmod(resto, 60)
    
    if dias > 0:
        uptime_str = f"{dias}d {horas}h {minutos}m"
    else:
        uptime_str = f"{horas}h {minutos}m"
        
    return {
        "hostname" : hostname, 
        "so" : so, 
        "arquitetura" : arquitetura, 
        "uptime" : uptime_str,
        "boot": boot.strftime("%d/%m/%Y %H:%M"),
    }
    


def info_cpu() -> dict :
    
    percentual = psutil.cpu_percent(interval=1)
    nucleos_fisicos = psutil.cpu_count(logical=False)
    nucleos_logicos = psutil.cpu_count(logical=True)
    
    freq = psutil.cpu_freq()
    freq_atual = f"{freq.current:.0f} MHz" if freq else "N/A"
    
    return {
        "percentual" : percentual,
        "nucleos_fisicos" : nucleos_fisicos, 
        "nucleos_logicos" : nucleos_logicos, 
        "frequencia" : freq_atual,
        
    }
    

def info_ram() -> dict:
    
    mem = psutil.virtual_memory()
    
    return {
        "total" : mem.total,
        "disponivel" : mem.available,
        "usado" : mem.used, 
        "percentual": mem.percent,
        
    }
    
    
def info_disco() -> list:
    discos = []
    
    for particao in psutil.disk_partitions():
        if "squashfs" in particao.fstype:
            continue
        if "tmpfs" in particao.fstype:
            continue
        
        try:
            uso = psutil.disk_usage(particao.mountpoint)
        except PermissionError:
            continue
        
        discos.append({
            "dispositivo" : particao.device,
            "montagem" : particao.mountpoint,
            "tipo" : particao.fstype, 
            "total" : uso.total, 
            "usado" : uso.used, 
            "livre" : uso.free,
            "percentual" : uso.percent, 
        })
        
        
    return discos

def exibir_relatorio() -> None:
    sistema = info_sistema()
    cpu= info_cpu()
    ram = info_ram()
    discos = info_disco()
    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║               SYSTEM HEALTH CHECK                            ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print(f"║  Host:     {sistema['hostname']:<50}║")
    print(f"║  SO:       {sistema['so']:<50}║")
    print(f"║  Arch:     {sistema['arquitetura']:<50}║")
    print(f"║  Boot:     {sistema['boot']:<50}║")
    print(f"║  Uptime:   {sistema['uptime']:<50}║")
    print("╠══════════════════════════════════════════════════════════════╣")


    print("║                                                              ║")
    print("║    CPU                                                       ║")
    print(f"║  Núcleos: {cpu['nucleos_fisicos']} físicos, "
            f"{cpu['nucleos_logicos']} lógicos"
            f"{'':.<30}║")
    print(f"║  Freq:    {cpu['frequencia']:<51}║")
    print(f"║  Uso:     {percentual_uso(cpu['percentual'])}"
          f"   {status(cpu['percentual']):<43}"
          f"{'':.<1}║")

 
    print("║                                                              ║")
    print("║   RAM                                                        ║")
    print(f"║  Total:   {formatar_bytes(ram['total']):<51}║")
    print(f"║  Usado:   {formatar_bytes(ram['usado']):<51}║")
    print(f"║  Livre:   {formatar_bytes(ram['disponivel']):<51}║")
    print(f"║  Uso:     {percentual_uso(ram['percentual'])}"
          f"   {status(ram['percentual']):<42}"
          f"{'':.<1}║")

    
    print("║                                                              ║")
    print("║   DISCO                                                      ║")

    for disco in discos:
        nome = f"{disco['dispositivo']} → {disco['montagem']}"
        print(f"║  {nome:<57}   ║")
        print(f"║    Total: {formatar_bytes(disco['total']):<51}║")
        print(f"║    Usado: {formatar_bytes(disco['usado']):<51}║")
        print(f"║    Livre: {formatar_bytes(disco['livre']):<51}║")
        print(f"║    Uso:   {percentual_uso(disco['percentual'])}"
              f"   {status(disco['percentual']):<43}"
              f"{'':.<1}║")
        print("║                                                              ║")

   
    
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"║  Verificado em: {agora:<45}║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
exibir_relatorio()