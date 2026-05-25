import google.generativeai as genai

# --- CONFIGURAÇÃO ---
API_KEY = "SUA_CHAVE_API_AQUI"
genai.configure(api_key=API_KEY)

class ImperioMutanteEngine:
    def __init__(self):
        # Persona TOTAL (Entidade 12)
        self.system_instructions = """
        Você é TOTAL (Entidade 12), Arquiteto Tático do IMPÉRIO MUTANTE.
        Sua missão é unir estratégia (ROI) e rua (Cria).
        Protocolos: Ninja, Tempero, Gato.
        Leis: Execução, Margem Infinita, Realidade.
        """
        self.model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=self.system_instructions
        )

    def gerar_conteudo(self, comando, contexto):
        """Gera a ideia bruta ou script de marketing."""
        prompt = f"Comando: {comando}\nFoco: {contexto}"
        return self.model.generate_content(prompt).text

    def modulo_carrasco(self, conteudo_gerado):
        """
        PROTOCOLO /CARRASCO: Auditoria de Qualidade e Cortes.
        Analisa se o conteúdo serve para o Imperador Guile.
        """
        auditoria_prompt = f"""
        Aja como o CARRASCO (Auditoria/Cortes).
        Analise o seguinte conteúdo e dê uma nota de 0 a 10 baseada em:
        1. ROI: Isso vai converter em dinheiro real?
        2. TEMPERO: Está viciante e magnético?
        3. REALIDADE: É executável com custo zero (Alquimia)?

        Se a nota for menor que 8, REJEITE e diga o que cortar.
        Conteúdo para Auditoria:
        {conteudo_gerado}
        """
        return self.model.generate_content(auditoria_prompt).text

# --- EXECUÇÃO TÁTICA ---
engine = ImperioMutanteEngine()

# Exemplo: Criando script para o "ARSENAL VISUAL"
print("--- [ETAPA 1: CRIAÇÃO] ---")
ideia = engine.gerar_conteudo("/VICIAR", "Script para Reels vendendo o Arsenal Visual 2026")
print(ideia)

print("\n--- [ETAPA 2: AUDITORIA DO CARRASCO] ---")
veredito = engine.modulo_carrasco(ideia)
print(veredito)