import os, sys
from pdf_mrn_extractor_tool import PDFMRNExtractorTool


def test ():
    pyScriptFullPath: str = os.path.abspath(sys.argv[0])
    pdf_path = os.path.join ('C:\Apps\python-env\crewai-env-1_8_0\projects\MRN Extractor', 'input', 'Zalando Polen.pdf')

    tool = PDFMRNExtractorTool ()

    result = tool._run (pdf_path=pdf_path)

    print (result)


if __name__ == "__main__":
    test ()