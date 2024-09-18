import streamlit as st
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.create_folder import create_project_folders
from utils.process_pdf import process_pdf_to_csv
from utils.manage_dataframe import display_dataframe_with_checkboxes  # Importa a nova função

# Cria os diretórios do projeto
UPLOAD_FOLDER, OUTPUT_FOLDER = create_project_folders()

st.title("Página Inicial - Enviar Novos Relatórios")

# Componente de upload de arquivo
uploaded_file = st.file_uploader("Carregar arquivo PDF", type="pdf")

if uploaded_file is not None:
    # Salva o arquivo carregado no diretório de uploads
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"Arquivo {uploaded_file.name} salvo com sucesso!")

    # Processa o PDF para CSV
    csv_path = process_pdf_to_csv(file_path, OUTPUT_FOLDER)

    if csv_path:
        st.success(f"CSV gerado com sucesso: {csv_path}")
        
        # Exibe o CSV e permite marcar como lido
        display_dataframe_with_checkboxes(csv_path)
        
        # Botão para download do CSV gerado
        with open(csv_path, "rb") as f:
            st.download_button(
                label="Download CSV",
                data=f,
                file_name=os.path.basename(csv_path),
                mime="text/csv"
            )
    else:
        st.error("Erro ao processar o arquivo PDF.")

# Botão para ir à página de envio de relatório
if st.button("Voltar a página Inicial"):
    st.switch_page("main.py")

# Botão para ir à página de visualização de relatórios
if st.button("Visualizar relatórios antigos"):
    st.switch_page("Pages/Visualizar_documento.py")