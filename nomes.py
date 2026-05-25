import os

def mapear_territorio():
    # Obtém o caminho da pasta onde o script está rodando
    caminho_atual = os.path.dirname(os.path.realpath(__file__))
    
    print(f"--- SCANNING: {caminho_atual} ---")
    
    # Lista todos os itens e filtra apenas arquivos
    try:
        ativos = [f for f in os.listdir(caminho_atual) if os.path.isfile(os.path.join(caminho_atual, f))]
        
        if not ativos:
            print("[!] Zona vazia. Nenhum arquivo encontrado.")
            return

        for idx, arquivo in enumerate(ativos, 1):
            print(f"[{idx:02d}] {arquivo}")
            
        print(f"\n--- TOTAL DE ATIVOS: {len(ativos)} ---")
        return ativos

    except Exception as e:
        print(f"[!] Glitch detectado no mapeamento: {e}")

if __name__ == "__main__":
    mapear_territorio()