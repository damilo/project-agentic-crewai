import os, re
from pathlib import Path
from dotenv import load_dotenv
from crewai.tools import BaseTool
from pdf2image import convert_from_path
import pytesseract

env_path = Path (__file__).parent.parent
load_dotenv (dotenv_path=os.path.join (env_path, ".env"))

class PDFMRNExtractorTool (BaseTool):
    name : str = "pdf_mrn_extractor"
    description : str = "analysiert eine PDF-Datei und extrahiert alle validen 18-stelligen Master Reference Numbers (MRN)."

    def _run (self, pdf_path: str):
        poppler_path = os.getenv ('POPPLER_PATH')
        tesseract_cmd = os.getenv('TESSERACT_CMD')
        print ('#info ' + str (poppler_path))
        print ('#info ' + str (tesseract_cmd))
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

        #mrn_pattern = r'\b\d{2}[A-Z]{2}[A-Z0-9]{14}\b'
        mrn_pattern = r'[0-9A-Z]{18}'
        mrns = []
        try:
            
            pages = convert_from_path (pdf_path, dpi=200, poppler_path=poppler_path)
            for page_image in pages:
                
                try:
                    osd = pytesseract.image_to_osd (page_image)
                    angle = int (re.search (r'Rotate: (\d+)', osd).group(1))
                    if angle != 0:
                        page_image = page_image.rotate (-angle, expand=True)
                except Exception as e:
                    return "#error " + str(e)
                
                page_text = pytesseract.image_to_string (page_image)
                if page_text:
                    print (page_text)
                    found = re.findall (mrn_pattern, page_text)
                    mrns.extend (found)
            
            mrns = list (set (mrns))
        
        except Exception as e:
            return "#error " + str(e)
        
        return mrns