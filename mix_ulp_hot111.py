import os
import shutil

# /SOBERANIA: Infraestrutura Base
DIRETORIO_ALVO = os.path.dirname(os.path.abspath(__file__))

PASTA_MICROSOFT = os.path.join(DIRETORIO_ALVO, "MICROSOFT")
PASTA_ULP = os.path.join(DIRETORIO_ALVO, "ULP")
PASTA_MIX = os.path.join(DIRETORIO_ALVO, "MIX")

# Domínios para capturar Outlook, Hotmail, MSN, Live, etc.
DOMINIOS_MS = ["hotmail.com", "outlook.com", "msn.com", "live.com"]

# 🚨 SINALIZADORES REFINADOS: Apenas URLs explícitas
SINALIZADORES_URL = ["http", "www."]

# /APOGEU: Garante que as pastas de destino existam
for pasta in [PASTA_MICROSOFT, PASTA_ULP, PASTA_MIX]:
    os.makedirs(pasta, exist_ok=True)


def classificar_arquivo(caminho_arquivo):
    try:
        # /CARRASCO: Contagem de linhas com Custo Zero de RAM (Sem readlines)
        with open(caminho_arquivo, "r", encoding="utf-8", errors="ignore") as f:
            total_linhas = sum(1 for _ in f)
        
        if total_linhas == 0:
            return None  # Arquivo vazio

        # 🎯 /GLITCH: Calculando o núcleo (Middle Point)
        meio = total_linhas // 2
        
        # Pega 10 linhas antes e 10 depois do centro (Totalizando até 20 linhas)
        inicio = max(0, meio - 10)
        fim = min(total_linhas, meio + 10)

        # /NEURO-TOXINA: Extraindo apenas o miolo, ignorando o resto do arquivo
        linhas_meio = []
        with open(caminho_arquivo, "r", encoding="utf-8", errors="ignore") as f:
            for i, linha in enumerate(f):
                if i >= inicio and i < fim:
                    linhas_meio.append(linha)
                elif i >= fim:
                    break # Latência Negativa: Para de ler assim que pega o miolo

        # Prepara a matriz de análise
        texto_analise = " ".join(linhas_meio).lower()

        # /ESPECTRO: Análise de Sinais e Direcionamento
        # 1. Se contiver 'http' ou 'www.', o arquivo é ULP
        if any(ind in texto_analise for ind in SINALIZADORES_URL):
            return PASTA_ULP

        # 2. Se NÃO tem URL, mas tem domínios MS -> MICROSOFT
        if any(dom in texto_analise for dom in DOMINIOS_MS):
            return PASTA_MICROSOFT

        # 3. Não bateu em nenhuma regra -> MIX
        return PASTA_MIX

    except Exception as e:
        print(f"[X] Quebra de Flow ao ler {caminho_arquivo}: {e}")
        return None


# /FLOW: Execução da Operação
print(f"🚀 Iniciando triagem /MUTAR na pasta: {DIRETORIO_ALVO}")

for item in os.listdir(DIRETORIO_ALVO):
    caminho_completo = os.path.join(DIRETORIO_ALVO, item)

    # Evita mover o próprio script e processa apenas arquivos .txt
    if (
        os.path.isfile(caminho_completo)
        and item.endswith(".txt")
        and item != os.path.basename(__file__)
    ):
        pasta_destino = classificar_arquivo(caminho_completo)

        if pasta_destino:
            shutil.move(caminho_completo, os.path.join(pasta_destino, item))
            print(f"[✔] Movido: {item} -> {os.path.basename(pasta_destino)}")

print("⚡ Operação concluída. Latência Negativa.")