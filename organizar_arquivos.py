import os
import shutil
from pathlib import Path

def encontrar_arquivos_por_extensao(diretorio, extensoes):
    """
    Encontra recursivamente arquivos com determinadas extensões em um diretório.

    Args:
        diretorio (str): Caminho do diretório a ser pesquisado
        extensoes (set): Conjunto de extensões a procurar (ex: {'.pdf', '.rar'})

    Returns:
        list: Lista de caminhos de arquivos encontrados
    """
    arquivos_encontrados = []

    try:
        for root, dirs, files in os.walk(diretorio):
            # Filtrar pastas do sistema para evitar lentidão e permissões
            dirs[:] = [d for d in dirs if d not in {'Windows', 'Program Files', 'Program Files (x86)',
                                                    'ProgramData', '$Recycle.Bin', 'System Volume Information'}]

            for file in files:
                if Path(file).suffix.lower() in extensoes:
                    caminho_completo = Path(root) / file
                    arquivos_encontrados.append(caminho_completo)
    except PermissionError:
        # Ignorar diretórios sem permissão
        pass
    except Exception as e:
        print(f"[ERRO ao percorrer diretório: {str(e)}] {diretorio}")

    return arquivos_encontrados

def organizar_arquivos():
    """
    Função principal que encontra arquivos PDF, RAR e scripts e os organiza em pastas na área de trabalho.
    """
    print("Iniciando busca por arquivos PDF, RAR, scripts e JSON...")
    print("=" * 70)

    # Definir pastas de destino na área de trabalho
    desktop = Path.home() / "Desktop"
    pasta_pdf = desktop / "PDF_Files"
    pasta_rar = desktop / "RAR_Files"
    pasta_scripts = desktop / "Script_Files"

    # Criar pastas se não existirem
    pasta_pdf.mkdir(exist_ok=True)
    pasta_rar.mkdir(exist_ok=True)
    pasta_scripts.mkdir(exist_ok=True)

    print(f"Pasta para PDFs: {pasta_pdf}")
    print(f"Pasta para arquivos compactados: {pasta_rar}")
    print(f"Pasta para scripts e JSON: {pasta_scripts}")
    print("-" * 70)

    # Buscar arquivos PDF e semelhantes
    extensoes_pdf = {'.pdf', '.epub', '.mobi', '.djvu', '.cbz', '.cbr'}
    print("Buscando arquivos PDF e semelhantes...")
    arquivos_pdf = encontrar_arquivos_por_extensao(Path.home(), extensoes_pdf)

    # Copiar arquivos PDF para a pasta correspondente
    print(f"Encontrados {len(arquivos_pdf)} arquivos PDF e semelhantes")
    for idx, arquivo in enumerate(arquivos_pdf, 1):
        try:
            destino = pasta_pdf / arquivo.name
            # Se já existir um arquivo com o mesmo nome, adicionar sufixo numérico
            contador = 1
            while destino.exists():
                nome_base = destino.stem
                extensao = destino.suffix
                novo_nome = f"{nome_base}_{contador}{extensao}"
                destino = pasta_pdf / novo_nome
                contador += 1

            shutil.copy2(arquivo, destino)  # Copiar mantendo metadados
            print(f"  [{idx}/{len(arquivos_pdf)}] Copiado: {arquivo.name}")
        except Exception as e:
            print(f"  [ERRO ao copiar {arquivo.name}: {str(e)}]")

    # Buscar arquivos RAR e semelhantes
    extensoes_rar = {'.rar', '.zip', '.7z', '.tar', '.gz', '.bz2', '.xz', '.iso', '.cab'}
    print("\nBuscando arquivos compactados (RAR, ZIP, etc.)...")
    arquivos_rar = encontrar_arquivos_por_extensao(Path.home(), extensoes_rar)

    # Mover arquivos RAR para a pasta correspondente
    print(f"Encontrados {len(arquivos_rar)} arquivos compactados")
    for idx, arquivo in enumerate(arquivos_rar, 1):
        try:
            destino = pasta_rar / arquivo.name
            # Se já existir um arquivo com o mesmo nome, adicionar sufixo numérico
            contador = 1
            while destino.exists():
                nome_base = destino.stem
                extensao = destino.suffix
                novo_nome = f"{nome_base}_{contador}{extensao}"
                destino = pasta_rar / novo_nome
                contador += 1

            shutil.move(arquivo, destino)  # Mover arquivo (não copiar)
            print(f"  [{idx}/{len(arquivos_rar)}] Movido: {arquivo.name}")
        except Exception as e:
            print(f"  [ERRO ao mover {arquivo.name}: {str(e)}]")

    # Buscar arquivos de script e JSON
    extensoes_scripts = {'.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.css', '.json', '.xml',
                         '.sh', '.bat', '.cmd', '.ps1', '.vbs', '.sql', '.php', '.rb', '.java',
                         '.cpp', '.c', '.h', '.cs', '.go', '.rs', '.yaml', '.yml'}
    print("\nBuscando arquivos de script e JSON...")
    arquivos_scripts = encontrar_arquivos_por_extensao(Path.home(), extensoes_scripts)

    # Copiar arquivos de script e JSON para a pasta correspondente
    print(f"Encontrados {len(arquivos_scripts)} arquivos de script e JSON")
    for idx, arquivo in enumerate(arquivos_scripts, 1):
        try:
            destino = pasta_scripts / arquivo.name
            # Se já existir um arquivo com o mesmo nome, adicionar sufixo numérico
            contador = 1
            while destino.exists():
                nome_base = destino.stem
                extensao = destino.suffix
                novo_nome = f"{nome_base}_{contador}{extensao}"
                destino = pasta_scripts / novo_nome
                contador += 1

            shutil.copy2(arquivo, destino)  # Copiar mantendo metadados
            print(f"  [{idx}/{len(arquivos_scripts)}] Copiado: {arquivo.name}")
        except Exception as e:
            print(f"  [ERRO ao copiar {arquivo.name}: {str(e)}]")

    print("\n" + "=" * 70)
    print("Processo concluído!")
    print(f"- {len(arquivos_pdf)} arquivos PDF e semelhantes foram COPIADOS para: {pasta_pdf}")
    print(f"- {len(arquivos_rar)} arquivos compactados foram MOVIDOS para: {pasta_rar}")
    print(f"- {len(arquivos_scripts)} arquivos de script e JSON foram COPIADOS para: {pasta_scripts}")

    # Salvar log do processo na área de trabalho
    log_path = desktop / "organizacao_arquivos_log.txt"
    with open(log_path, 'w', encoding='utf-8') as log_file:
        log_file.write("Log de organização de arquivos\n")
        log_file.write("="*40 + "\n")
        log_file.write(f"Data: {Path(__file__).stat().st_mtime}\n\n")
        log_file.write(f"Arquivos PDF e semelhantes encontrados: {len(arquivos_pdf)}\n")
        log_file.write(f"Arquivos compactados encontrados: {len(arquivos_rar)}\n")
        log_file.write(f"Scripts e JSON encontrados: {len(arquivos_scripts)}\n\n")

        log_file.write("Detalhes dos arquivos encontrados:\n")
        log_file.write("-" * 30 + "\n")
        log_file.write("PDFs e semelhantes:\n")
        for arquivo in arquivos_pdf:
            log_file.write(f"  {arquivo}\n")
        log_file.write("\nArquivos compactados:\n")
        for arquivo in arquivos_rar:
            log_file.write(f"  {arquivo}\n")
        log_file.write("\nScripts e JSON:\n")
        for arquivo in arquivos_scripts:
            log_file.write(f"  {arquivo}\n")

    print(f"- Um log do processo foi salvo em: {log_path}")

def main():
    try:
        organizar_arquivos()
    except KeyboardInterrupt:
        print("\nOperação interrompida pelo usuário.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {str(e)}")

if __name__ == "__main__":
    main()