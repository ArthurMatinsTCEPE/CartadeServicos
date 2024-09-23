import pdfplumber
import re
import os
import pandas as pd
import csv

def extract_sections_with_type(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        sections = []
        current_section_type = ""

        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()

            if text:
                # Verifica se encontramos uma nova seção de tipo
                if "Decisões Monocráticas - Aposentadorias, Pensões e Reformas" in text:
                    current_section_type = "Aposentadorias, Pensões e Reformas"

                # Coleta o texto se estamos na seção correta
                if current_section_type:
                    sections.append((page_num + 1, text, current_section_type))

        return sections

def extract_diario_date(text):
    # Regex para capturar a data no formato "09 de outubro de 2024"
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

        # Formata a data no padrão "DD/MM/AAAA"
        data_formatada = f"{dia}/{mes}/{ano}"
        return data_formatada

    return ""

def extract_process_info(text, page_num, data_diario, tipo_decisao):
    processos = []

    # Regex para outros tipos de decisões monocráticas
    numero_processo_regex = r"PROCESSO TC N[º°]\s?(\S+)"
    numero_extrato_regex = r"EXTRATO DA DECISÃO MONOCRÁTICA DE N[º°]\s?(\S+)"

    processos_encontrados = re.findall(numero_processo_regex, text)
    extratos_encontrados = re.findall(numero_extrato_regex, text)

    for i in range(len(processos_encontrados)):
        numero_processo = processos_encontrados[i] if i < len(processos_encontrados) else ''
        numero_extrato = extratos_encontrados[i] if i < len(extratos_encontrados) else ''

        # Adiciona um zero à frente de todos os números de extrato
        if numero_extrato:
            numero_extrato = '0' + numero_extrato
            
            # Ajusta o número do extrato para o formato "01234/24" (removendo os dois primeiros dígitos do ano)
            numero_extrato = re.sub(r'/\d{4}', lambda x: f'/{x.group()[3:]}', numero_extrato)

        processos.append([numero_processo, numero_extrato, data_diario, page_num, tipo_decisao])

    return processos

def save_to_excel(processos, output_excel):
    header = ["Numero do Processo", "Numero do Extrato", "Data da Publicacao", "Numero da Pagina", "Tipo de Decisão"]
    
    # Criação de um DataFrame com os processos
    df = pd.DataFrame(processos, columns=header)
    
    # Salvando em Excel
    df.to_excel(output_excel, index=False, engine='openpyxl')

# Função para processar o PDF e salvar os dados no formato Excel
def process_pdf_to_excel(pdf_path, output_folder):
    sections = extract_sections_with_type(pdf_path)
    if not sections:
        print("No sections found.")
        return None

    data_diario = extract_diario_date(sections[0][1])
    processos = []

    # Extrai informações dos processos de cada seção
    for page_num, text, tipo_decisao in sections:
        processos.extend(extract_process_info(text, page_num, data_diario, tipo_decisao))

    # Definir o nome e caminho do arquivo Excel
    excel_filename = os.path.splitext(os.path.basename(pdf_path))[0] + ".xlsx"
    excel_path = os.path.join(output_folder, excel_filename)
    
    # Salvar os processos no arquivo Excel
    save_to_excel(processos, excel_path)

    return excel_path