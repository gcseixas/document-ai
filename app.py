from flask import Flask, render_template, redirect, send_file, request, session, after_this_request, Response
import os
from services.services import upload , processar_gerando_texto, PASTA_UPLOAD, apagar_pdfs, apagar_excel_session
from pathlib import Path


app = Flask(__name__)

app.secret_key = "63f4945d921d599f27ae4fdf5bada3f1"


@app.route("/", methods=['POST', 'GET'])
def pagina_inicial():
    
    if request.method == 'POST':
        arquivos_rota = request.files.getlist('arquivos')
    
        arquivos = upload(arquivos_rota)
        texto = processar_gerando_texto(arquivos)
    
        apagar_pdfs(PASTA_UPLOAD, arquivos)
    
        return render_template(
            'index.html',
            relatorio_pronto=texto
        )
    
    return render_template(
        'index.html',
        relatorio_pronto=''
    )

    
    
if __name__ == "__main__":
    app.run(debug=True)
    
    
