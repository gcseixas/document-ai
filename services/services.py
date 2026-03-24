import os
from services.servicePDF import extrair_texto
from services.serviceAI import analisar_documento
import pandas as pd
import json
from flask import session
import uuid


PASTA_EXCEL = 'Excel'

PASTA_UPLOAD = "uploads/pdfs"


def upload(arquivos):
    
    arquivos_usuario = []
    
    for arquivo in arquivos:
        
        if arquivo.filename:

            caminho = os.path.join(PASTA_UPLOAD, arquivo.filename)
            
            arquivos_usuario.append(arquivo.filename)
            

        arquivo.save(caminho)
        
    return arquivos_usuario

def processar_gerando_texto(arquivos_usuario):
    
    analises = []
    for arquivo in arquivos_usuario:
        
        caminho_pdf =  os.path.join("uploads/pdfs", arquivo)
    
        analise = analisar_documento(caminho_pdf)
        
        analises.append(analise)
        
    return analises
        

    
def apagar_pdfs(pasta_pdfs, lista_pdfs):

    for arquivo in lista_pdfs:

        caminho = os.path.join(pasta_pdfs, arquivo)

        os.remove(caminho)
        
def processar_gerando_excel(arquivos_usuario):
    
    analises = []
    for arquivo in arquivos_usuario:
        
        caminho_pdf =  os.path.join("uploads/pdfs", arquivo)
    
        texto = extrair_texto(caminho_pdf)
        
        analise = analisar_documento(texto)
        
        dados = json.loads(analise)
        registro = {
            "Empresa": dados['Nome da empresa'],
            "CNPJ": dados['CNPJ'],
            "Tipo de certidão": dados['Tipo de certidão'],
            "Situação": dados['Situação'],
            "Data de validade": dados['Data de validade']
            }
        
        analises.append(registro)
        
    df = pd.DataFrame(analises)
    df = df.dropna()
    df = df[
    (df["Situação"].notna()) & 
    (df["Situação"] != "")
    ]
    df = df[
    (df["Data de validade"].notna()) & 
    (df["Data de validade"] != "")
    ]
    
    id_relatorio = str(uuid.uuid4())
    
    nome_excel = f"relatorio_{id_relatorio}.xlsx"
    
    session["relatorio"] = nome_excel
    
    df.to_excel(os.path.join(PASTA_EXCEL, nome_excel), index=False)
    

def apagar_excel_session():
    session.pop("relatorio",None)
    

