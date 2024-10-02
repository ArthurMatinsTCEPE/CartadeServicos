import fitz  # PyMuPDF 
import re
import os
import pandas as pd

def extract_text_from_pdf(pdf_path):
    text_data = []
    with fitz.open(pdf_path) as pdf:
        for page_num in range(len(pdf)):
            page = pdf[page_num]
            text = page.get_text()
            text_data.append((page_num + 1, text))
    return text_data

def extract_diario_date(text):
    # Regex para capturar a data no formato "Recife, 09 de outubro de 2024"
    data_diario_regex = r"Recife,\s+(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})"
    match = re.search(data_diario_regex, text)

    if match:
        dia = match.group(1).zfill(2)  # Preenche com zero à esquerda se necessário
        mes_extenso = match.group(2).lower()  # Converte o nome do mês para minúsculo
        ano = match.group(3)

        # Dicionário para mapear os meses do formato extenso para o numérico
        meses = {
            "janeiro": "01",
            "fevereiro": "02",
            "março": "03",
            "abril": "04",
            "maio": "05",
            "junho": "06",
            "julho": "07",
            "agosto": "08",
            "setembro": "09",
            "outubro": "10",
            "novembro": "11",
            "dezembro": "12"
        }

        mes = meses.get(mes_extenso, "00")  # Se o mês não for encontrado, retorna "00"
        return f"{dia}/{mes}/{ano}"

    return ""

def extract_process_and_extrato(text, page_num):
    processos = []
    extratos = []
    
    # Regex para processos e extratos
    numero_processo_regex = r"PROCESSO\s?TC\s?N[º°]\s?(\S+)"
    numero_extrato_regex = r"EXTRATO\s?DA\s?DECISÃO\s?MONOCRÁTICA\s?DE\s?N[º°]\s?(\S+)"

    processos_encontrados = re.findall(numero_processo_regex, text)
    extratos_encontrados = re.findall(numero_extrato_regex, text)

    # Adiciona processos e extratos às suas respectivas listas
    for numero_processo in processos_encontrados:
        processos.append((numero_processo, page_num))

    for numero_extrato in extratos_encontrados:
        # Formata o extrato conforme necessário
        numero_extrato = '0' + numero_extrato
        numero_extrato = re.sub(r'/\d{4}', lambda x: f'/{x.group()[3:]}', numero_extrato)
        extratos.append((numero_extrato, page_num))

    return processos, extratos

def save_to_excel(processos_extratos, output_excel):
    header = ["Numero do Processo", "Numero do Extrato", "Data da Publicacao", "Numero da Pagina", "Tipo de Decisão"]
    
    # Criação de um DataFrame com os processos
    df = pd.DataFrame(processos_extratos, columns=header)
    
    # Salvando em Excel
    df.to_excel(output_excel, index=False, engine='openpyxl')

def process_pdf_to_excel(pdf_path, output_folder):
    text_data = extract_text_from_pdf(pdf_path)
    data_diario = extract_diario_date(' '.join([text for _, text in text_data]))  # Captura a data do diário de todo o texto
    processos = []
    extratos = []

    # Extrai informações de cada seção
    for page_num, text in text_data:
        novos_processos, novos_extratos = extract_process_and_extrato(text, page_num)
        processos.extend(novos_processos)
        extratos.extend(novos_extratos)

    # Combinar processos e extratos
    processos_extratos = []
    for i in range(min(len(processos), len(extratos))):
        processo, processo_page = processos[i]
        extrato, extrato_page = extratos[i]
        
        # Cria uma linha no formato desejado
        processos_extratos.append([processo, extrato, data_diario, extrato_page, "Aposentadorias, Pensões e Reformas"])

    # Definir o nome e caminho do arquivo Excel
    excel_filename = os.path.splitext(os.path.basename(pdf_path))[0] + ".xlsx"
    excel_path = os.path.join(output_folder, excel_filename)
    
    # Salvar os processos no arquivo Excel
    save_to_excel(processos_extratos, excel_path)

    return excel_path
