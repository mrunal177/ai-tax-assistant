import pdfplumber
import json
import csv

def extract_salary_data(pdf_path, output_json="salary_data.json", output_csv="salary_data.csv"):
    """Extracts table data from a PDF and saves it as JSON and CSV."""
    extracted_data = {}

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                tables = page.extract_tables()

                if not tables:
                    continue  # Skip if no tables on the page

                for table in tables:
                    for row in table:
                        if len(row) >= 2 and row[0]:  # Ensure there's a key-value pair
                            key = row[0].strip()
                            value = row[1].strip() if row[1] else ""
                            extracted_data[key] = value

        # Save as JSON
        with open(output_json, "w", encoding="utf-8") as json_file:
            json.dump(extracted_data, json_file, indent=4)

        # Save as CSV
        with open(output_csv, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Field", "Value"])  # Header row
            for key, value in extracted_data.items():
                writer.writerow([key, value])

        print(f"Extraction completed. JSON saved to {output_json}, CSV saved to {output_csv}")

    except Exception as e:
        print(f"Error extracting salary data: {e}")

if __name__ == "__main__":
    pdf_path = "sample.pdf"  # Change to your actual PDF file
    extract_salary_data(pdf_path)
