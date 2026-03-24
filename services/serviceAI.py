from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

def analisar_certidao(texto):

    prompt = f"""
 
    DOCUMENTO:
    {texto}
    """

    resposta = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return resposta.output_text