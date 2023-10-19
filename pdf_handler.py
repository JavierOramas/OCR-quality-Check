import logging
from tika import parser

logger = logging.getLogger("tika")
logger.setLevel(logging.ERROR)

def extract_text_from_pdf(file_path):
    # Parse the document
    parsed_data = parser.from_file(file_path)

    # Extract text from parsed data
    content = parsed_data.get('content')
    text = content.strip() if content else ""
   
    return text.replace('\n', ' ').replace('\r', '').replace('\t', '').strip()

# # Function to perform OCR on extracted text using pytesseract
# def perform_ocr(text):
#     # Run OCR on the text extracted from the PDF
#     ocr_text = pytesseract.image_to_string(Image.frombytes("RGB", (1, 1), text))
#     return ocr_text

def get_ocr(pdf_file_path):
    # Step 1: Extract text from the PDF
    extracted_text = extract_text_from_pdf(pdf_file_path)
   
    # Step 2: Perform OCR on the extracted text
    # ocr_result = perform_ocr(extracted_text)

    # Step 3: Display OCR result
    # print(extracted_text)
    
    return extracted_text

if __name__ == "__main__":
    text = extract_text_from_pdf('rddm/FCE_0001_02564.pdf')
    print(text)