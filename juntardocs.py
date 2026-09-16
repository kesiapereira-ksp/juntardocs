from collections import defaultdict
import io
import zipfile
import streamlit as st
from pypdf import PdfWriter

st.set_page_config(page_title="Mesclador de PDFs em Lote", page_icon="📦")

st.title("📦 Juntar Várias Pastas de PDF")
st.write(
    "Envie um arquivo **.ZIP** contendo subpastas com PDFs. Cada subpasta gerará"
    " um arquivo PDF unificado com o nome da pasta e a competência."
)

# Entrada da Competência
col1, col2 = st.columns(2)
with col1:
    mes = st.number_input("Mês Competência", min_value=1, max_value=12, value=9)
with col2:
    ano = st.number_input(
        "Ano Competência", min_value=2020, max_value=2030, value=2026
    )

# Upload do arquivo ZIP
arquivo_zip_enviado = st.file_uploader(
    "Carregue o arquivo .ZIP com as pastas", type=["zip"]
)

if arquivo_zip_enviado:
    if st.button("Unificar Pastas em Lote"):
        try:
            grupos_pastas = defaultdict(list)

            # Leitura do ZIP em memória
            with zipfile.ZipFile(arquivo_zip_enviado, "r") as z:
                for filename in z.namelist():
                    # Ignora pastas do sistema ou arquivos que não são PDF
                    if filename.startswith("__MACOSX") or filename.endswith("/"):
                        continue

                    if filename.lower().endswith(".pdf"):
                        partes = filename.split("/")
                        if len(partes) > 1:
                            nome_pasta = partes[0]  # Nome da subpasta principal
                            nome_arquivo = partes[-1]
                            conteudo = z.read(filename)
                            grupos_pastas[nome_pasta].append(
                                (nome_arquivo, conteudo)
                            )

            if not grupos_pastas:
                st.warning(
                    "Nenhuma subpasta com arquivos PDF foi encontrada dentro"
                    " do arquivo ZIP."
                )
            else:
                zip_saida = io.BytesIO()
                mes_formatado = f"{int(mes):02d}"

                # Criação do ZIP final contendo todos os PDFs gerados
                with zipfile.ZipFile(
                    zip_saida, "w", zipfile.ZIP_DEFLATED
                ) as z_out:
                    for nome_pasta, arquivos in grupos_pastas.items():
                        writer = PdfWriter()

                        # Ordena arquivos em ordem alfabética
                        arquivos_ordenados = sorted(arquivos, key=lambda x: x[0])

                        for _, dados_pdf in arquivos_ordenados:
                            writer.append(io.BytesIO(dados_pdf))

                        pdf_mesclado = io.BytesIO()
                        writer.write(pdf_mesclado)
                        writer.close()

                        # Nome final: NomeDaPasta_MM-AAAA.pdf
                        nome_pdf_final = (
                            f"{nome_pasta}_{mes_formatado}-{ano}.pdf"
                        )
                        z_out.writestr(nome_pdf_final, pdf_mesclado.getvalue())

                zip_saida.seek(0)
                st.success(
                    f"Processamento concluído! {len(grupos_pastas)} pasta(s)"
                    " unificada(s) com sucesso."
                )

                st.download_button(
                    label="📥 Baixar Todos os PDFs Unificados (.ZIP)",
                    data=zip_saida,
                    file_name=f"PDFs_Unificados_{mes_formatado}-{ano}.zip",
                    mime="application/zip",
                )
        except Exception as e:
            st.error(f"Ocorreu um erro ao processar o arquivo: {e}")
