import psutil
import time

def monitorar_ritmo_imperial():
    print("[!] MONITOR: Sincronizando Bio-Wealth com Ciclos de CPU...")
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        # Transforma uso de CPU em "Intensidade de Néctar"
        if cpu_usage > 80:
            print(f"🔥 FLOW AGRESSIVO: CPU a {cpu_usage}% | Margem Infinita em curso.")
        elif cpu_usage < 20:
            print(f"💤 STANDBY: Sistema aguardando input do Imperador.")
        time.sleep(2)

if __name__ == "__main__":
    monitorar_ritmo_imperial()