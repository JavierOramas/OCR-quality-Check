import PyPDF2
import logging

logger = logging.getLogger("PyPDF2")
logger.setLevel(logging.ERROR)
# Function to extract text from a PDF using PyPDF2
def extract_text_from_pdf(pdf_path):
    pdf_text = ""
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)

        for page in pdf_reader.pages:
            pdf_text += page.extract_text()
    # print("PDF_TEXT", pdf_text)
    return pdf_text

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
