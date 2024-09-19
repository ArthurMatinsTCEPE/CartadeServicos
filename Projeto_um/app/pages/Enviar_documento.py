import streamlit as st
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.create_folder import create_project_folders
from utils.process_pdf import process_pdf_to_excel  # Alterado para Excel

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

    # Processa o PDF para Excel
    excel_path = process_pdf_to_excel(file_path, OUTPUT_FOLDER)  # Alterado para gerar Excel

    if excel_path:
        st.success(f"Arquivo Excel gerado com sucesso: {excel_path}")
        
        # Redireciona para a página de visualização de documentos
        st.switch_page("Pages/Visualizar_documento.py")
    else:
        st.error("Erro ao processar o arquivo PDF.")
