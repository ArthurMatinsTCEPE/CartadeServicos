import pdfplumber
import re
import os
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
                elif "Decisões Monocráticas - Medidas Cautelares" in text:
                    current_section_type = "Medidas Cautelares"

                # Coleta o texto se estamos na seção correta
                if current_section_type:
                    sections.append((page_num + 1, text, current_section_type))

        return sections

def extract_diario_date(text):
    data_diario_regex = r"Recife,\s+(\d{1,2}\s+de\s+\w+\s+de\s+\d{4})"
    match = re.search(data_diario_regex, text)
    return match.group(1) if match else ""

def extract_process_info(text, page_num, data_diario, tipo_decisao):
    processos = []

    if tipo_decisao == "Medidas Cautelares":
        # Regex específico para "Medidas Cautelares"
        numero_processo_regex = r"Número:\s?(\S+)"
        processos_encontrados = re.findall(numero_processo_regex, text)
        
        # Para "Medidas Cautelares", o número do extrato é vazio
        for numero_processo in processos_encontrados:
            processos.append([numero_processo, '', data_diario, page_num, tipo_decisao])
    
    else:
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

            processos.append([numero_processo, numero_extrato, data_diario, page_num, tipo_decisao])

    return processos

def save_to_csv(processos, output_csv):
    header = ["Numero do Processo", "Numero do Extrato", "Data da Publicacao", "Numero da Pagina", "Tipo de Decisão"]
    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(processos)

def process_pdf_to_csv(pdf_path, output_folder):
    sections = extract_sections_with_type(pdf_path)
    if not sections:
        print("No sections found.")
        return None

    data_diario = extract_diario_date(sections[0][1])
    processos = []

    for page_num, text, tipo_decisao in sections:
        processos.extend(extract_process_info(text, page_num, data_diario, tipo_decisao))

    csv_filename = os.path.splitext(os.path.basename(pdf_path))[0] + ".csv"
    csv_path = os.path.join(output_folder, csv_filename)
    
    save_to_csv(processos, csv_path)

    return csv_path
