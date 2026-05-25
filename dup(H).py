import os

def executar_limpeza():
    # 1. Radar: Escaneia a pasta atual em busca de arquivos .txt
    arquivos_alvo = [f for f in os.listdir('.') if f.endswith('.txt') and not f.startswith('CLEAN_')]

    if not arquivos_alvo:
        print(">>> Nenhum alvo .txt detectado no perímetro.")
        return

    print(f">>> {len(arquivos_alvo)} alvos detectados. Iniciando protocolo de limpeza...\n")

    for arquivo in arquivos_alvo:
        print(f"[PROCESSANDO] Alvo: {arquivo}")

        try:
            # 2. Extração: Lê o conteúdo bruto
            with open(arquivo, 'r', encoding='utf-8') as f:
                linhas = f.readlines()

            # 3. Refinaria: Remove duplicatas mantendo a ordem (Lógica de Cria)
            # dict.fromkeys() é o método mais rápido e mantém a ordem de inserção
            linhas_unicas = list(dict.fromkeys(linhas))

            # Cálculo de eficiência (ROI da operação)
            cortadas = len(linhas) - len(linhas_unicas)

            # 4. Consolidação: Salva o novo ativo limpo
            nome_saida = f"CLEAN_{arquivo}"
            with open(nome_saida, 'w', encoding='utf-8') as f:
                f.writelines(linhas_unicas)

            print(f"   |__ Status: SUCESSO")
            print(f"   |__ Arquivo Gerado: {nome_saida}")
            print(f"   |__ Redundância Eliminada: {cortadas} linhas removidas.\n")

        except Exception as e:
            print(f"   |__ ERRO TÁTICO: {e}\n")

if __name__ == "__main__":
    executar_limpeza()
    input(">>> Operação finalizada. Pressione ENTER para sair.")