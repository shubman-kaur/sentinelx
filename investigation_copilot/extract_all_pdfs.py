import pdfplumber
import os


DOCS_FOLDER = "docs"
OUTPUT_FOLDER = "docs/extracted"


os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def clean_text(text):
    """Extra blank lines aur whitespace hatata hai"""
    lines = text.split("\n")
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    return "\n".join(cleaned_lines)

def extract_pdf(pdf_path, output_path):
    """Ek PDF ka poora text nikal ke .txt file mein save karta hai"""
    all_text = []
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"  Total pages: {len(pdf.pages)}")
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                all_text.append(text)
    
    full_text = "\n\n".join(all_text)
    full_text = clean_text(full_text)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_text)
    
    print(f"  Saved: {output_path} ({len(full_text)} characters)")


pdf_files = [
    "cert_in_handbook.pdf",
    "rbi_beaware.pdf",
    "ncrb_citizen_booklet.pdf",
    "cyber_dost_ebook.pdf"
]


pdf_files = [
    "CERT-In_Digital_Safety_Compass_Handbook.pdf",
    "BEAWARE07032022.pdf",
    "ncrb_citizen_booklet.pdf",
    "Cyber-security-tips-by-cyber-dost.pdf"
]

for pdf_file in pdf_files:
    pdf_path = os.path.join(DOCS_FOLDER, pdf_file)
    output_filename = os.path.splitext(pdf_file)[0].lower().replace("-", "_") + ".txt"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
    
    print(f"\nProcessing: {pdf_file}")
    
    if not os.path.exists(pdf_path):
        print(f"  ⚠️ File not found, skipping: {pdf_path}")
        continue
    
    extract_pdf(pdf_path, output_path)

print("\n✅ All PDFs processed!")