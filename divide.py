import os

def dividir_arquivo_em_3(nome_arquivo):
    if not os.path.exists(nome_arquivo):
        print(f"[!] ERRO: Arquivo {nome_arquivo} não encontrado na pasta.")
        return

    # Leitura de todas as linhas (Néctar Puro)
    with open(nome_arquivo, 'r', encoding='utf-8', errors='ignore') as f:
        linhas = f.readlines()

    total_linhas = len(linhas)
    # Cálculo tático da divisão
    tamanho_parte = total_linhas // 3
    sobra = total_linhas % 3

    indices = [
        (0, tamanho_parte + (1 if sobra > 0 else 0)),
        (tamanho_parte + (1 if sobra > 0 else 0), 2 * tamanho_parte + (1 if sobra > 1 else 0)),
        (2 * tamanho_parte + (1 if sobra > 1 else 0), total_linhas)
    ]

    # Geração dos arquivos de saída
    base_nome = os.path.splitext(nome_arquivo)[0]
    for i, (inicio, fim) in enumerate(indices):
        nome_saida = f"{base_nome}_parte_{i+1}.txt"
        with open(nome_saida, 'w', encoding='utf-8') as f_out:
            f_out.writelines(linhas[inicio:fim])
        print(f"[+] Ativo gerado: {nome_saida} ({fim - inicio} linhas)")

if __name__ == "__main__":
    # Altere para o nome do seu arquivo original
    alvo = "lista.txt" 
    dividir_arquivo_em_3(alvo)