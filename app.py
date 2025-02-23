import pytesseract
import cv2
from PIL import Image
import os

# ✅ Path to Tesseract (Mac users, adjust if needed)
pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"

def extract_text(image_path):
    # ✅ Get absolute path for debugging
    abs_path = os.path.abspath(image_path)
    print(f"🔍 Loading image from: {abs_path}")

    # ✅ Load image
    img = cv2.imread(image_path)

    if img is None:
        print("❌ Error: Image not found or could not be loaded. Check path and format.")
        return ""

    # ✅ Convert to grayscale (improves OCR accuracy)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # ✅ Apply OCR
    text = pytesseract.image_to_string(gray)

    return text

# ✅ Test with a sample document
if __name__ == "__main__":
    image_path = "img.png"  # Replace with your actual image file

    extracted_text = extract_text(image_path)

    if extracted_text.strip():
        print("\n📜 Extracted Text:\n", extracted_text)
    else:
        print("⚠️ No text extracted. Check image quality or OCR setup.")
