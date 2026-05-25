import os
import shutil

# Configuração das pastas e palavras-chave (Keywords)
# O script verifica se o nome do arquivo contém alguma dessas palavras
CATEGORIAS = {
    "01_Dinheiro_e_Negocios": [
        "money", "cash", "business", "negocio", "renda", "lucro", "profit", 
        "empreendedor", "startup", "affiliate", "afiliado", "finance", 
        "riqueza", "milhao", "million", "dropshipping", "ecommerce", "loja"
    ],
    "02_Marketing_e_Vendas": [
        "marketing", "copywriting", "copy", "traffic", "trafego", "ads", 
        "anuncio", "funnel", "funil", "sales", "venda", "social media", 
        "instagram", "facebook", "youtube", "twitter", "tiktok", "email marketing",
        "seo", "branding", "lead", "launch", "lancamento"
    ],
    "03_Cripto_e_Trading": [
        "bitcoin", "btc", "crypto", "cripto", "blockchain", "ethereum", 
        "trading", "trader", "forex", "invest", "stock", "bolsa", 
        "analise tecnica", "candlestick", "coin"
    ],
    "04_Desenvolvimento_Pessoal": [
        "mindset", "mental", "psychology", "psicologia", "persuasion", "persuasao",
        "habit", "habito", "success", "sucesso", "produtividade", "foco", 
        "pnl", "inteligencia", "coach", "lideranca", "influence", "influencia"
    ],
    "05_Saude_e_Fitness": [
        "fitness", "fit", "workout", "treino", "gym", "academia", "diet", "dieta",
        "weight loss", "perder peso", "emagrecer", "muscle", "musculo", 
        "health", "saude", "nutrition", "nutricao", "recipe", "receita", "cozinha"
    ],
    "06_Tech_e_Hacking": [
        "hack", "security", "seguranca", "code", "coding", "programacao", 
        "python", "java", "script", "linux", "excel", "design", "adobe", 
        "photoshop", "web", "developer", "android", "iphone"
    ],
    "07_Conteudo_Adulto_Restrito": [
        "porn", "sex", "adult", "onlyfans", "whore", "ewhoring", "nude", 
        "pack", "kamasutra", "seduction", "seducao", "mulher", "women", "girl"
    ]
}

PASTA_OUTROS = "99_Outros"

def organizar_arquivos():
    # Pega o diretório onde o script está rodando
    diretorio_atual = os.getcwd()
    
    # Lista todos os arquivos
    arquivos = [f for f in os.listdir(diretorio_atual) if os.path.isfile(f)]
    
    # Contador para relatório final
    movidos_count = 0
    
    print(f"Iniciando organização de {len(arquivos)} arquivos...")

    for arquivo in arquivos:
        # Pula o próprio script para não se mover
        if arquivo == os.path.basename(__file__):
            continue
            
        nome_lower = arquivo.lower()
        destino = None

        # Verifica em qual categoria o arquivo se encaixa
        for pasta, keywords in CATEGORIAS.items():
            for keyword in keywords:
                # Verifica se a palavra chave está no nome do arquivo
                if keyword in nome_lower:
                    destino = pasta
                    break
            if destino:
                break
        
        # Se não encontrou categoria, vai para Outros
        if not destino:
            destino = PASTA_OUTROS

        # Cria a pasta se não existir
        caminho_destino = os.path.join(diretorio_atual, destino)
        if not os.path.exists(caminho_destino):
            os.makedirs(caminho_destino)
            print(f"Pasta criada: {destino}")

        # Move o arquivo
        try:
            shutil.move(os.path.join(diretorio_atual, arquivo), os.path.join(caminho_destino, arquivo))
            movidos_count += 1
            # print(f"Movido: {arquivo} -> {destino}") # Descomente se quiser ver um a um
        except Exception as e:
            print(f"Erro ao mover {arquivo}: {e}")

    print("-" * 30)
    print(f"Concluído! {movidos_count} arquivos foram organizados.")
    print(f"Verifique a pasta '{PASTA_OUTROS}' para itens que precisam de revisão manual.")

if __name__ == "__main__":
    organizar_arquivos()