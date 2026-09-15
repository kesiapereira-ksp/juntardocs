import os
from pypdf import PdfMerger


def mesclar_pdfs(pasta_origem, nome_projeto, mes, ano, pasta_saida=None):
    if pasta_saida is None:
        pasta_saida = pasta_origem

    # Garante que o mês tenha 2 dígitos (ex: 05 em vez de 5)
    mes_formatado = f"{int(mes):02d}"
    nome_arquivo_final = f"{nome_projeto}_{mes_formatado}-{ano}.pdf"
    caminho_final = os.path.join(pasta_saida, nome_arquivo_final)

    merger = PdfMerger()

    # Filtra e ordena os arquivos .pdf da pasta
    arquivos = [
        f for f in os.listdir(pasta_origem) if f.lower().endswith(".pdf")
    ]
    arquivos.sort()

    if not arquivos:
        print("Nenhum arquivo PDF encontrado na pasta informada.")
        return

    # Adiciona cada arquivo no mesclador
    for arquivo in arquivos:
        caminho_arquivo = os.path.join(pasta_origem, arquivo)
        merger.append(caminho_arquivo)
        print(f"Adicionado: {arquivo}")

    # Gera o arquivo final unificado
    merger.write(caminho_final)
    merger.close()

    print(f"\nSucesso! PDF unificado salvo em: {caminho_final}")


# --- Parâmetros de Uso ---
pasta_arquivos = r"C:\caminho\para\sua\pasta"  # Informe o caminho da pasta
nome_do_projeto = "Projeto_Exemplo"  # Nome do projeto
mes_competencia = "09"  # Mês (ex: 09 ou 9)
ano_competencia = "2026"  # Ano (ex: 2026)

# Execução
mesclar_pdfs(
    pasta_arquivos, nome_do_projeto, mes_competencia, ano_competencia
)
