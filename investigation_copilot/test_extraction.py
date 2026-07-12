import pdfplumber


pdf_path = "docs/ncrb_citizen_booklet.pdf"

with pdfplumber.open(pdf_path) as pdf:
    print(f"Total pages: {len(pdf.pages)}")
    
    
    for i, page in enumerate(pdf.pages[:2]):
        text = page.extract_text()
        print(f"\n--- Page {i+1} ---")
        print(text)
        print(f"\n[Character count: {len(text) if text else 0}]")