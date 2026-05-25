import os
import shutil

# Definição dos alvos
keywords = ["ULP", "MIX", "HOT"]

def executar_operacao():
    print("[+] Iniciando varredura tática...")
    
    # Lista todos os arquivos da pasta atual
    for arquivo in os.listdir("."):
        if not arquivo.endswith(".txt"):
            continue
            
        pasta_destino = None
        arquivo_upper = arquivo.upper()
        
        # 1. Checagem prioritária no nome do arquivo
        for kw in keywords:
            if kw in arquivo_upper:
                pasta_destino = kw
                break
                
        # 2. Checagem secundária no conteúdo do arquivo
        if not pasta_destino:
            try:
                with open(arquivo, 'r', encoding='utf-8', errors='ignore') as f:
                    conteudo = f.read().upper()
                    for kw in keywords:
                        if kw in conteudo:
                            pasta_destino = kw
                            break
            except Exception as e:
                print(f"[!] Erro ao ler {arquivo}: {e}")
                continue
                
        # 3. Movimentação tática
        if pasta_destino:
            # Cria a pasta se ela não existir
            if not os.path.exists(pasta_destino):
                os.makedirs(pasta_destino)
                print(f"[!] Pasta criada: {pasta_destino}/")
                
            # Move o arquivo
            shutil.move(arquivo, os.path.join(pasta_destino, arquivo))
            print(f"[OK] {arquivo} -> {pasta_destino}/")

    print("[+] Operação finalizada. Ativos organizados.")

if __name__ == "__main__":
    executar_operacao()