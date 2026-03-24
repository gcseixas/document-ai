from openai import OpenAI
from dotenv import load_dotenv
import os
import base64
import tempfile
import fitz  # PyMuPDF — instale com: pip install pymupdf

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()


def encode_image(caminho_imagem):
    with open(caminho_imagem, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def pdf_para_imagens(caminho_pdf, dpi=150):
    """
    Rasteriza cada página do PDF em imagens JPEG usando PyMuPDF.
    Retorna uma lista de caminhos para as imagens geradas.
    Compatível com Windows, Linux e macOS sem dependências externas.
    """
    pasta_temp = tempfile.mkdtemp()
    imagens = []

    doc = fitz.open(caminho_pdf)
    zoom = dpi / 72  # PyMuPDF usa 72 DPI como base
    matriz = fitz.Matrix(zoom, zoom)

    for i, pagina in enumerate(doc): # type: ignore
        pix = pagina.get_pixmap(matrix=matriz)
        caminho_img = os.path.join(pasta_temp, f"pagina-{i + 1:03d}.jpg")
        pix.save(caminho_img)
        imagens.append(caminho_img)

    doc.close()
    return imagens


def analisar_documento(caminho_arquivo):
    """
    Analisa um documento (imagem PNG/JPG ou PDF) quanto à conformidade com a NR-34.
    """
    prompt = """
Você é um auditor especializado em NR-34 (Condições e Meio Ambiente de Trabalho na Indústria da Construção e Reparação Naval).

Sua função é analisar documentos de treinamento e verificar conformidade com a NR-34.

Critérios obrigatórios:

1. Carga horária:
- Treinamento inicial (admissional): mínimo de 6 horas
- Treinamento de reciclagem: mínimo de 4 horas

2. Conteúdo programático:
- Riscos inerentes à atividade
- Condições e meio ambiente de trabalho
- Equipamentos de Proteção Coletiva (EPC)
- Equipamentos de Proteção Individual (EPI)

3. Formalização:
- Identificação do colaborador
- Assinatura do colaborador
- Identificação da empresa ou responsável
- Data de realização

4. Coerência:
- Informações consistentes

Regras de resposta:

Status: (Conforme / Não conforme / Parcialmente conforme)

Justificativa:
- Explique objetivamente

Não conformidades:
- Liste itens não atendidos

Observações:
- Pontos adicionais

Importante:
- Não inventar dados
- Falta de info = não conforme ou inconclusivo
"""

    extensao = os.path.splitext(caminho_arquivo)[1].lower()

    if extensao == ".pdf":
        imagens = pdf_para_imagens(caminho_arquivo)
        content = [{"type": "input_text", "text": prompt}]

        for caminho_img in imagens:
            base64_img = encode_image(caminho_img)
            content.append({
                "type": "input_image",
                "image_url": f"data:image/jpeg;base64,{base64_img}"
            })

        # Limpa arquivos temporários
        pasta_temp = os.path.dirname(imagens[0])
        for img in imagens:
            os.remove(img)
        os.rmdir(pasta_temp)

    elif extensao in (".png", ".jpg", ".jpeg"):
        base64_image = encode_image(caminho_arquivo)
        media_type = "image/png" if extensao == ".png" else "image/jpeg"
        content = [
            {"type": "input_text", "text": prompt},
            {"type": "input_image", "image_url": f"data:{media_type};base64,{base64_image}"}
        ]

    else:
        raise ValueError(f"Formato de arquivo não suportado: {extensao}. Use PDF, PNG ou JPG.")

    response = client.responses.create(
        model="gpt-4.1",
        input=[{
            "role": "user",
            "content": content
        }]  # pyright: ignore[reportArgumentType]
    )

    return response.output_text