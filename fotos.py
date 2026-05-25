import random
import time

# DNA DO IMPÉRIO - COMPONENTES MUTÁVEIS
styles = ["Cyberpunk Corporate", "Tactical Streetwear", "Dark Tech-Noir", "Ultra-Minimalist Gold"]
products = ["Algoritmo I.A.", "Pack de Contas Premium", "Planilha de ROI Infinito", "Script de Automação Ninja"]
environments = ["Underground Bunker", "High-Rise Office with Neon View", "Dark Server Room", "Virtual Reality Void"]
colors = ["Purple/Green Neon", "Gold/Black Luxury", "Red/Silver Industrial", "Cyan/Deep Blue Tech"]

def generate_mutant_prompt():
    style = random.choice(styles)
    product = random.choice(products)
    env = random.choice(environments)
    color = random.choice(colors)
    
    # O SEED PROMPT (A BASE QUE NÃO MUDA)
    base_prompt = (
        f"A professional product mockup of '{product}' in a {style} style. "
        f"Location: {env}. Lighting: {color} tones. "
        f"High-quality, 8k, cinematic, featuring the Mutant Empire biohazard logo. "
        f"Atmosphere: Sovereign, authoritative, and addictive."
    )
    return base_prompt

# LOOP DE ESCALA
def start_factory(iterations=5):
    for i in range(iterations):
        print(f"--- Gerando Mutação {i+1} ---")
        prompt = generate_mutant_prompt()
        print(f"Prompt Enviado: {prompt}")
        # Aqui entraria a conexão com a API de Imagem (DALL-E / Nano Banana)
        time.sleep(2) # Delay para não sobrecarregar

if __name__ == "__main__":
    start_factory()