import os

# Constante para o diretório do projeto
PROJECT_DIR = "Projeto_um"

# Função para criar diretórios de uploads e outputs
def create_project_folders():
    # Define os diretórios para uploads e outputs
    upload_folder = os.path.join(PROJECT_DIR, "uploads")
    output_folder = os.path.join(PROJECT_DIR, "outputs")

    # Criação dos diretórios se não existirem
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    return upload_folder, output_folder

