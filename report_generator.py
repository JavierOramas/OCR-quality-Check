import pandas as pd
from openpyxl import Workbook

def generate_excel_summary(raw_report_data, excel_file_path="summary.xlsx", acceptable_ratio=0.2):

    # Convert JSON data to a list of dictionaries
    good_legibility_records = []
    bad_legibility_records = []
    good_alphanumerical_records = []
    bad_alphanumerical_records = []
    
    summary_counts_legibility = {'< 20': 0, '20-40': 0, '40-60': 0, '60-80': 0, '80>': 0}
    summary_counts_alphanumerical = {'< 20': 0, '20-40': 0, '40-60': 0, '60-80': 0, '80>': 0}

    for path, info in raw_report_data.items():
        legible_ratio = info['legible_ratio_es']  
        alpha_ratio = info['non_alpha_ratio']

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
            
        if legible_ratio < 0.2:
            summary_counts_alphanumerical['< 20'] += 1
        elif legible_ratio < 0.4:
            summary_counts_alphanumerical['20-40'] += 1
        elif legible_ratio < 0.6:
            summary_counts_alphanumerical['40-60'] += 1
        elif legible_ratio < 0.8:
            summary_counts_alphanumerical['60-80'] += 1
        else:
            summary_counts_alphanumerical['80>'] += 1

        record = {'path': path, 'legible_characters': legible_ratio, 'alphanumerical_characters': alpha_ratio}
        if legible_ratio > acceptable_ratio:
            good_legibility_records.append(record)
        else:
            bad_legibility_records.append(record)
        if alpha_ratio > acceptable_ratio:
            good_alphanumerical_records.append(record)
        else:
            bad_alphanumerical_records.append(record)
        
    # Create DataFrames from the list of dictionaries
    df = pd.DataFrame(good_legibility_records)
    df_bad = pd.DataFrame(bad_legibility_records)
    df_summary = pd.DataFrame.from_dict(summary_counts_legibility, orient='index', columns=['Count'])

    
    df2 = pd.DataFrame(good_alphanumerical_records)
    df2_bad = pd.DataFrame(bad_alphanumerical_records)
    
    df2_summary = pd.DataFrame.from_dict(summary_counts_alphanumerical, orient='index', columns=['Count'])

    print(excel_file_path)
    # Export DataFrames to separate sheets in the Excel file
    with pd.ExcelWriter(excel_file_path) as writer:
        df_summary.to_excel(writer, sheet_name='Reporte de Legibilidad')
        df.to_excel(writer, sheet_name='Buena Legibilidad', index=False)
        df_bad.to_excel(writer, sheet_name='Mala Legibilidad', index=False)
        df2_summary.to_excel(writer, sheet_name='Reporte Alfanumerico')
        df2.to_excel(writer, sheet_name='Buenos Alfanumerico', index=False)
        df2_bad.to_excel(writer, sheet_name='Malos Alfanumerico', index=False)

if __name__ == "__main__":
    json_file_path = "input.json"  # Replace with the actual path of your JSON file
    excel_file_path = "output.xlsx"  # Replace with the desired output Excel file path
    generate_excel_summary(json_file_path, excel_file_path)
