import pytesseract
import cv2
import os
import pdfplumber
import pandas as pd
from pdf2image import convert_from_path
from PIL import Image

# Set the correct Tesseract path
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"  # Update this path for your system

def preprocess_image(image):
    """Preprocess the image for better OCR results."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)  # Apply thresholding
    return binary

def extract_text_from_image(image_path):
    """Extract text from an image file."""
    try:
        img = cv2.imread(image_path)
        if img is None:
            print(f"Error: Image not found at {image_path}.")
            return ""

        processed_image = preprocess_image(img)
        text = pytesseract.image_to_string(processed_image)
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from {image_path}: {e}")
        return ""

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF using OCR and pdfplumber."""
    try:
        text = ""

        # Extract text from images (OCR)
        images = convert_from_path(pdf_path)
        for i, image in enumerate(images):
            image_path = f"page_{i}.png"
            image.save(image_path, "PNG")
            page_text = extract_text_from_image(image_path)
            text += f"Page {i + 1} (OCR):\n{page_text}\n\n"
            os.remove(image_path)

        # Extract text using pdfplumber (for embedded text)
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text += f"Page {i + 1} (pdfplumber):\n{page.extract_text()}\n\n"

        return text.strip()
    except Exception as e:
        print(f"Error processing PDF {pdf_path}: {e}")
        return ""

def extract_tables_from_pdf(pdf_path):
    """Extract tables from a PDF using pdfplumber."""
    tables = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                table = page.extract_table()
                if table:
                    df = pd.DataFrame(table)
                    tables.append(df)
        return tables
    except Exception as e:
        print(f"Error extracting tables from {pdf_path}: {e}")
        return []

# Test with a sample document
if __name__ == "__main__":
    pdf_path = "sample.pdf"  # Replace with your actual PDF file
    extracted_text = extract_text_from_pdf(pdf_path)
    extracted_tables = extract_tables_from_pdf(pdf_path)

    if extracted_text.strip():
        print("Extracted Text:\n", extracted_text)
    else:
        print("No text extracted. Check PDF quality.")

    if extracted_tables:
        print("\nExtracted Tables:")
        for idx, table in enumerate(extracted_tables):
            print(f"\nTable {idx + 1}:\n", table)
    else:
        print("No tables found.")
