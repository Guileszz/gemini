import os

def limpar_duplicatas():
    print("--- [ ENTIDADE 12: PROTOCOLO DE LIMPEZA ] ---")
    
    # 1. Input Tático: Pede o nome do arquivo
    nome_arquivo = input(">> Digite o nome do arquivo .txt de entrada: ").strip()

    # Garante que tenha a extensão .txt
    if not nome_arquivo.lower().endswith('.txt'):
        nome_arquivo += '.txt'

    # Verifica se o arquivo existe na base (pasta atual)
    if not os.path.exists(nome_arquivo):
        print(f"\n❌ Erro: O arquivo '{nome_arquivo}' não foi encontrado aqui.")
        input("\nPressione Enter para sair...")
        return

    print(f"\n🔄 Processando '{nome_arquivo}'... Extraindo o Néctar.")

    # 2. Processamento (Mantendo a ordem original)
    linhas_vistas = set()
    linhas_unicas = []

    try:
        # Tenta abrir com utf-8 (padrão moderno), se falhar tenta latin-1 (padrão antigo/windows)
        try:
            encoding_type = 'utf-8'
            with open(nome_arquivo, 'r', encoding=encoding_type) as f:
                linhas = f.readlines()
        except UnicodeDecodeError:
            encoding_type = 'latin-1'
            with open(nome_arquivo, 'r', encoding=encoding_type) as f:
                linhas = f.readlines()

        # Filtragem
        for linha in linhas:
            # Removemos espaços em branco das pontas apenas para conferência, 
            # mas salvamos a linha original se quiser preservar formatação.
            # Se quiser remover linhas vazias também, descomente a linha abaixo:
            # if not linha.strip(): continue 
            
            if linha not in linhas_vistas:
                linhas_unicas.append(linha)
                linhas_vistas.add(linha)

        # 3. Output (Gênesis)
        nome_saida = nome_arquivo.replace(".txt", "_limpo.txt")
        
        with open(nome_saida, 'w', encoding=encoding_type) as f_saida:
            f_saida.writelines(linhas_unicas)

        print(f"\n✅ SUCESSO ABSOLUTO.")
        print(f"📊 Original: {len(linhas)} linhas")
        print(f"💎 Final:    {len(linhas_unicas)} linhas únicas")
        print(f"📂 Arquivo gerado: {nome_saida}")

    except Exception as e:
        print(f"\n⚠️ Falha crítica: {e}")

    input("\n>> Pressione Enter para encerrar a missão.")

if __name__ == "__main__":
    limpar_duplicatas()