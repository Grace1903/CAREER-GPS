import os
import pdfplumber
import spacy
import re


class PDFExtractor:

    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            print("Downloading spacy model...")
            os.system("python -m spacy download en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
    
    def extract_text(self, file_path):
        """Main method to extract text from PDF"""
        
        print(f"\n[DEBUG] Opening file: {file_path}")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        text = self.extract_text_from_pdf(file_path)
        
        print(f"[DEBUG] Total extracted text length: {len(text)} characters")
        
        if text:
            print(f"[DEBUG] First 200 characters: {text[:200]}")
        
        if not text or len(text.strip()) < 20:
            print("[WARNING] Very little text extracted! Check if PDF is scanned or protected.")
            raise Exception("Failed to extract text from PDF. The file may be scanned, image-based, or protected.")
        
        return text
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text using pdfplumber"""
        
        raw_text = ""
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                print(f"[DEBUG] PDF has {len(pdf.pages)} pages")
                
                for i, page in enumerate(pdf.pages):
                    page_text = page.extract_text()
                    if page_text:
                        raw_text += page_text + "\n"
                        print(f"[DEBUG] Page {i+1}: Extracted {len(page_text)} characters")
                        print(f"[DEBUG] Page {i+1} sample: {page_text[:100]}")
                    else:
                        print(f"[DEBUG] Page {i+1}: NO text found - page may be an image")
                        
        except Exception as e:
            print(f"[ERROR] Failed to open PDF: {e}")
            return ""
        
        if not raw_text.strip():
            print("[ERROR] No text found in any page. Resume may be a scanned image.")
            return ""
        
        # Clean the text - keep original for skill extraction
        raw_text = raw_text.lower()
        
        # Don't remove too much for skill extraction
        # Just basic cleaning
        cleaned_text = re.sub(r'\s+', ' ', raw_text)
        
        return cleaned_text