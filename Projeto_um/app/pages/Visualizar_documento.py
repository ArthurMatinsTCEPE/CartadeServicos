import streamlit as st
import os
import pandas as pd
import sys

# Adiciona o diretório raiz do projeto ao sys.path para garantir que o utils seja encontrado
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.create_folder import create_project_folders
from utils.manage_dataframe import display_dataframe_with_checkboxes  # Importa a nova função

# Cria os diretórios do projeto
UPLOAD_FOLDER, OUTPUT_FOLDER = create_project_folders()

# Função para listar arquivos no diretório UPLOAD_FOLDER
def listar_arquivos():
    arquivos = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.pdf')]
    return arquivos

# Função para encontrar o arquivo mais recente
def arquivo_mais_recente(arquivos):
    arquivos_completos = [os.path.join(UPLOAD_FOLDER, f) for f in arquivos]
    return max(arquivos_completos, key=os.path.getctime) if arquivos_completos else None

st.title("Página 2 - Carregar Relatórios Antigos")

# Listar arquivos PDF no diretório UPLOAD_FOLDER
arquivos = listar_arquivos()

if arquivos:
    # Encontra o arquivo mais recente
    arquivo_recente = arquivo_mais_recente(arquivos)
    arquivo_recente_nome = os.path.basename(arquivo_recente)

    # Seleciona o arquivo, com o mais recente como padrão
    selected_file = st.selectbox("Selecione um arquivo para processar:", arquivos, index=arquivos.index(arquivo_recente_nome))

    if selected_file:
        # Caminho completo do arquivo selecionado
        file_path = os.path.join(UPLOAD_FOLDER, selected_file)
        # Nome do Excel correspondente
        excel_filename = os.path.splitext(selected_file)[0] + ".xlsx"
        excel_path = os.path.join(OUTPUT_FOLDER, excel_filename)

        if excel_path and os.path.exists(excel_path):
            # Exibe o Excel e permite marcar como lido
            display_dataframe_with_checkboxes(excel_path)

            # Botão para download do arquivo Excel selecionado
            with open(excel_path, "rb") as f:
                st.download_button(
                    label="Download Excel",
                    data=f,
                    file_name=os.path.basename(excel_path),
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.error("Erro ao processar o arquivo PDF ou carregar o arquivo Excel existente.")
else:
    st.write("Nenhum arquivo PDF disponível para exibir.")

# Botão para ir à página de envio de relatório
if st.button("Voltar a página Inicial"):
    st.switch_page("main.py")

# Botão para ir à página de visualização de relatórios
if st.button("Visualizar relatórios antigos"):
    st.switch_page("Pages/Visualizar_documento.py")
