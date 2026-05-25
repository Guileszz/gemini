import os
import math

def fracionar_arquivo(arquivo_entrada, diretorio_saida, num_partes=10):
    print(f"[*] Iniciando fracionamento de {arquivo_entrada} em {num_partes} partes.")
    
    with open(arquivo_entrada, 'r', encoding='utf-8', errors='ignore') as f:
        linhas = f.readlines()

    total_linhas = len(linhas)
    tamanho_lote = math.ceil(total_linhas / num_partes)
    nome_base = os.path.basename(arquivo_entrada).split('.')[0]

    os.makedirs(diretorio_saida, exist_ok=True)

    for i in range(num_partes):
        inicio = i * tamanho_lote
        fim = min((i + 1) * tamanho_lote, total_linhas)
        lote = linhas[inicio:fim]

        if not lote: 
            break # Trava de segurança para não criar arquivos vazios

        caminho_saida = os.path.join(diretorio_saida, f"{nome_base}_parte_{i+1}.txt")
        
        with open(caminho_saida, 'w', encoding='utf-8') as f:
            f.writelines(lote)

    print(f"[+] Fracionamento executado com sucesso no diretório: {diretorio_saida}")

# Execução
fracionar_arquivo('./resultado_limpo.txt', './dados_fracionados', num_partes=10)