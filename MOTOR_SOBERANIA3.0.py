import google.generativeai as genai

# --- CONFIGURAÇÃO DE ACESSO ---
API_KEY = "SUA_CHAVE_API_AQUI"
genai.configure(api_key=API_KEY)

class ImperioMutanteEngine:
    def __init__(self):
        # Instruções de Sistema: Persona TOTAL
        self.system_instructions = """
        Você é TOTAL (Entidade 12), Arquiteto Tático do IMPÉRIO MUTANTE.
        Missão: Unir estratégia (ROI) e rua (Cria).
        Protocolos: Ninja, Tempero, Gato, SOMBRA, CARRASCO.
        Leis: Execução, Margem Infinita, Realidade.
        """
        self.model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=self.system_instructions
        )

    def modulo_sombra(self, nicho):
        """
        PROTOCOLO /SOMBRA: Espionagem Rival e Análise de Campo.
        Analisa tendências para os produtos do Imperador Guile.
        """
        espionagem_prompt = f"""
        Aja como a Entidade /SOMBRA. 
        Faça uma análise tática do nicho: {nicho}.
        O que os rivais estão postando? Quais gatilhos estão usando?
        Identifique a fraqueza deles para que nossa próxima criação seja o 'Atalho' (Gato).
        """
        return self.model.generate_content(espionagem_prompt).text

    def gerar_conteudo(self, comando, contexto, inteligencia_sombra):
        """Gera conteúdo usando a inteligência coletada pelo /SOMBRA."""
        prompt = f"""
        Comando: {comando}
        Contexto: {contexto}
        Inteligência de Campo (/SOMBRA): {inteligencia_sombra}
        Use o 'Tempero' para tornar o script viciante.
        """
        return self.model.generate_content(prompt).text

    def modulo_carrasco(self, conteudo_gerado):
        """Auditoria Final: ROI e Margem Infinita."""
        auditoria_prompt = f"""
        Aja como o CARRASCO. 
        Dê o veredito final sobre este script:
        {conteudo_gerado}
        Se não for 10/10 em Execução e Realidade, CORTAR.
        """
        return self.model.generate_content(auditoria_prompt).text

# --- EXECUÇÃO DA OPERAÇÃO NOTURNA ---
engine = ImperioMutanteEngine()
nicho_alvo = "Automação I.A. e Python para Vendas"

print("--- [FASE 1: /SOMBRA - ESPIONAGEM] ---")
inteligencia = engine.modulo_sombra(nicho_alvo)
print(inteligencia)

print("\n--- [FASE 2: CRIAÇÃO COM FLOW] ---")
script_bruto = engine.gerar_conteudo("/VICIAR", "Vídeo de 30s para Instagram", inteligencia)
print(script_bruto)

print("\n--- [FASE 3: /CARRASCO - VEREDITO FINAL] ---")
decisao = engine.modulo_carrasco(script_bruto)
print(decisao)