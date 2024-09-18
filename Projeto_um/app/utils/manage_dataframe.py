import pandas as pd
import streamlit as st
import os

# Function to load data from CSV
def load_data(csv_path):
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        return pd.DataFrame()

# Function to save the DataFrame to CSV
def save_read_status(data, csv_path):
    data.to_csv(csv_path, index=False)

# Function to display DataFrame with checkboxes and manage read status
def display_dataframe_with_checkboxes(csv_path):
    # Load data
    data = load_data(csv_path)

    # Add "Lido" column if it doesn't exist
    if 'Lido' not in data.columns:
        data['Lido'] = False  # Initialize as unread

    # Display page title
    st.title('Processos - Marcar como Lido')

    # Display DataFrame with editor
    edited_data = st.data_editor(data, use_container_width=True)

    # Update DataFrame with edited data
    data = edited_data

    # Generate a unique key based on the file path
    unique_key = f'save_state_button_{os.path.basename(csv_path)}'

    # Button to save current state with a unique key
    if st.button('Salvar Estado', key=unique_key):
        save_read_status(data, csv_path)
        st.success('Estado salvo com sucesso!')

# Example usage:
# Replace 'your_file.csv' with your actual CSV file path.
csv_path = 'your_file.csv'
display_dataframe_with_checkboxes(csv_path)
