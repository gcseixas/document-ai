import pdfplumber

def extrair_texto(caminho_pdf):

    texto = ""

    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto += pagina.extract_text()

    return texto