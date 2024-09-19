import pandas as pd
import streamlit as st
import os

# Função para carregar dados do Excel
def load_data(excel_path):
    if os.path.exists(excel_path):
        return pd.read_excel(excel_path)  # Lê um arquivo Excel
    else:
        return pd.DataFrame()

# Função para salvar o DataFrame em um arquivo Excel
def save_read_status(data, excel_path):
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        data.to_excel(writer, index=False)

# Função para exibir o DataFrame com checkboxes e gerenciar o status de leitura
def display_dataframe_with_checkboxes(excel_path):
    # Carregar os dados
    data = load_data(excel_path)

    # Adicionar a coluna "Lido" se não existir
    if 'Lido' not in data.columns:
        data['Lido'] = False  # Inicializa como não lido

    # Exibir título da página
    st.title('Processos - Marcar como Lido')

    # Exibir o DataFrame com editor
    edited_data = st.data_editor(data, use_container_width=True)

    # Atualizar o DataFrame com os dados editados
    data = edited_data

    # Gerar uma chave única com base no caminho do arquivo
    unique_key = f'save_state_button_{os.path.basename(excel_path)}'

    # Botão para salvar o estado atual com uma chave única
    if st.button('Salvar Estado', key=unique_key):
        save_read_status(data, excel_path)
        st.success('Estado salvo com sucesso!')

# Exemplo de uso:
# Substitua 'your_file.xlsx' pelo caminho do seu arquivo Excel real.
excel_path = 'your_file.xlsx'
display_dataframe_with_checkboxes(excel_path)
