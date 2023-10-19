import pandas as pd
from openpyxl import Workbook

def generate_excel_summary(raw_report_data, excel_file_path="summary.xlsx"):

    # Convert JSON data to a list of dictionaries
    records = []
    
    summary_counts_legibility = {'< 20': 0, '20-40': 0, '40-60': 0, '60-80': 0, '80>': 0}
    summary_counts_alphanumerical = {'< 20': 0, '20-40': 0, '40-60': 0, '60-80': 0, '80>': 0}

    for path, info in raw_report_data.items():
        legible_ratio = info['legible_ratio_es']  
        alpha_ratio = info['non_alpha_ratio']
        num_tokens = info['num_tokens']
        detected_entities = info['detected_entities']

        # Check and update the summary count
        if legible_ratio < 0.2:
            summary_counts_legibility['< 20'] += 1
        elif legible_ratio < 0.4:
            summary_counts_legibility['20-40'] += 1
        elif legible_ratio < 0.6:
            summary_counts_legibility['40-60'] += 1
        elif legible_ratio < 0.8:
            summary_counts_legibility['60-80'] += 1
        else:
            summary_counts_legibility['80>'] += 1
            
        if alpha_ratio < 0.2:
            summary_counts_alphanumerical['< 20'] += 1
        elif alpha_ratio < 0.4:
            summary_counts_alphanumerical['20-40'] += 1
        elif alpha_ratio < 0.6:
            summary_counts_alphanumerical['40-60'] += 1
        elif alpha_ratio < 0.8:
            summary_counts_alphanumerical['60-80'] += 1
        else:
            summary_counts_alphanumerical['80>'] += 1

        record = {'ruta': path, 
                  'palabras legibles': legible_ratio, 
                  'palabras no alfanuméricas': alpha_ratio, 
                  "cantidad de palabras": num_tokens,
                  "entidades detectades": detected_entities
                  }
        records.append(record)
        
    # Create DataFrames from the list of dictionaries
    df = pd.DataFrame(records)
    df_summary = pd.DataFrame.from_dict(summary_counts_legibility, orient='index', columns=['Counteo Legible'])
    df_summary['Counteo No alanumerico'] = list(summary_counts_alphanumerical.values())
    
    print(excel_file_path)
    
    # Export DataFrames to separate sheets in the Excel file
    with pd.ExcelWriter(excel_file_path) as writer:
        df_summary.to_excel(writer, sheet_name='Resumen')
        df.to_excel(writer, sheet_name='Detalles', index=False)


if __name__ == "__main__":
    json_file_path = "input.json"  # Replace with the actual path of your JSON file
    excel_file_path = "output.xlsx"  # Replace with the desired output Excel file path
    generate_excel_summary(json_file_path, excel_file_path)
