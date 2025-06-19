#!/usr/bin/env python
"""
Extract and display text content from PDF files
"""

import os

try:
    from PyPDF2 import PdfReader
    PDF_SUPPORT = True
except ImportError:
    print("PyPDF2 not installed. Install with: pip install PyPDF2")
    PDF_SUPPORT = False

def extract_text_from_pdf(pdf_path):
    """Extract text content from a PDF file"""
    if not PDF_SUPPORT:
        return "PDF text extraction not available - install PyPDF2"
    
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            
            text = ""
            print(f"PDF has {len(reader.pages)} pages")
            
            for i, page in enumerate(reader.pages, 1):
                page_text = page.extract_text()
                text += f"\n--- Page {i} ---\n{page_text}\n"
            
            return text.strip()
    except Exception as e:
        return f"Error extracting PDF text: {e}"

def main():
    print("=== PDF Text Extraction ===")
    
    # Check for downloaded PDF files
    pdf_files = [
        "downloaded_v2_UK_Standby_Callout_Overtime_Exploded_pdf.pdf",
        "downloaded_v3_UK_Standby_Callout_Overtime_Exploded_pdf.pdf"
    ]
    
    for pdf_file in pdf_files:
        if os.path.exists(pdf_file):
            print(f"\n--- Extracting text from: {pdf_file} ---")
            
            file_size = os.path.getsize(pdf_file)
            print(f"File size: {file_size} bytes")
            
            if file_size > 0:
                text = extract_text_from_pdf(pdf_file)
                
                print(f"\nEXTRACTED TEXT:")
                print("=" * 60)
                print(text)
                print("=" * 60)
                
                # Save text to file
                text_file = pdf_file.replace('.pdf', '_text.txt')
                with open(text_file, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"\nText saved to: {text_file}")
            else:
                print("File is empty (0 bytes)")
        else:
            print(f"File not found: {pdf_file}")

if __name__ == "__main__":
    main() 