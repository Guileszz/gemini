import os
import glob

def fundir_arquivos(diretorio_alvo, arquivo_saida):
    print(f"[*] Iniciando fusão no diretório: {diretorio_alvo}")
    
    with open(arquivo_saida, 'w', encoding='utf-8') as outfile:
        # Pega todos os arquivos da pasta
        for filepath in glob.glob(os.path.join(diretorio_alvo, '*.*')):
            if filepath == arquivo_saida or filepath.endswith('.py'): 
                continue
                
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
                outfile.write(infile.read() + "\n")
                
    print(f"[+] Fusão concluída. Arquivo gerado: {arquivo_saida}")

# Execução
fundir_arquivos('./dados_brutos', './resultado_fusao.txt')