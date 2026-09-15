import io
import streamlit as st
from pypdf import PdfWriter

st.set_page_config(page_title="Mesclador de PDFs", page_icon="📄")

st.title("📄 Juntar Arquivos PDF")
st.write(
    "Selecione os arquivos PDF, informe os dados do projeto e baixe o arquivo unificado."
)

# Formulário de entrada de dados
nome_projeto = st.text_input("Nome do Projeto", value="Projeto_Exemplo")

col1, col2 = st.columns(2)
with col1:
    mes = st.number_input("Mês Competência", min_value=1, max_value=12, value=9)
with col2:
    ano = st.number_input("Ano Competência", min_value=2020, max_value=2030, value=2026)

# Upload dos PDFs
arquivos_pdf = st.file_uploader(
    "Carregue os arquivos PDF aqui", type=["pdf"], accept_multiple_files=True
)

if arquivos_pdf:
    st.info(f"{len(arquivos_pdf)} arquivo(s) selecionado(s).")

    if st.button("Unificar PDFs"):
        try:
            writer = PdfWriter()

            # Ordena os arquivos alfabeticamente pelo nome original
            arquivos_ordenados = sorted(arquivos_pdf, key=lambda x: x.name)

            for pdf in arquivos_ordenados:
                writer.append(pdf)

            # Salva o arquivo mesclado na memória
            output_pdf = io.BytesIO()
            writer.write(output_pdf)
            writer.close()
            output_pdf.seek(0)

            # Formata o nome final do arquivo (ex: Projeto_Exemplo_09-2026.pdf)
            mes_formatado = f"{int(mes):02d}"
            nome_arquivo_final = f"{nome_projeto}_{mes_formatado}-{ano}.pdf"

            st.success("PDFs unificados com sucesso!")

            # Botão de download para o usuário
            st.download_button(
                label="📥 Baixar PDF Unificado",
                data=output_pdf,
                file_name=nome_arquivo_final,
                mime="application/pdf",
            )
        except Exception as e:
            st.error(f"Ocorreu um erro ao processar os arquivos: {e}")
