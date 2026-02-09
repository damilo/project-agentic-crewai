import os, re
from pathlib import Path
from dotenv import load_dotenv
from crewai.tools import BaseTool
from pdf2image import convert_from_path
import pytesseract

env_path = Path (__file__).parent.parent
load_dotenv (dotenv_path=os.path.join (env_path, ".env"))

class PdfToTextTool (BaseTool):
    name : str = "pdf_to_text"
    description : str = "liest eine PDF-Datei (Typ Text oder Bild) und gibt deren gesamten Text zurück."


    def _run (self, pdf_path: str):

        poppler_path = os.getenv ('POPPLER_PATH')
        tesseract_cmd = os.getenv('TESSERACT_CMD')
        print ('#info ' + str (poppler_path))
        print ('#info ' + str (tesseract_cmd))
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd


        full_text = []
        full_text = [f"# source file name: {os.path.basename (pdf_path)}"]
        full_text.append ("\n")
        try:
            
            pages = convert_from_path (pdf_path, dpi=200, poppler_path=poppler_path)
            for i, page_image in enumerate (pages):
                
                try:
                    osd = pytesseract.image_to_osd (page_image)
                    rotation_match = re.search (r'Rotate: (\d+)', osd)
                    if rotation_match:
                        angle = int (rotation_match.group(1))
                        if angle != 0:
                            page_image = page_image.rotate (-angle, expand=True)
                except Exception as e:
                    return "#error " + str (e)
                
                custom_config = r'--oem 3 --psm 6'
                page_text = pytesseract.image_to_string (page_image, config=custom_config)
                if page_text:
                    full_text.append(f"## page {i+1}")
                    full_text.append("------")
                    full_text.append (page_text.strip ())
                    full_text.append ("\n")
        
        except Exception as e:
            return "#error " + str (e)
        
        return "\n".join (full_text)