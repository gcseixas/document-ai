from flask import Flask, render_template, redirect, send_file, request, session, after_this_request, Response
import os
from services.services import upload , processar, PASTA_EXCEL,PASTA_UPLOAD, apagar_pdfs, apagar_excel_session
from pathlib import Path


app = Flask(__name__)

app.secret_key = "63f4945d921d599f27ae4fdf5bada3f1"


@app.route("/")
def pagina_inicial():
    
    relatorio_pronto = "relatorio" in session
    
    return render_template(
        'index.html',
        relatorio_pronto=relatorio_pronto
        )


@app.route("/processar", methods=['POST'])
def processar_rota():
    arquivos_rota = request.files.getlist('arquivos')
    
    arquivos =  upload(arquivos_rota)
    
    processar(arquivos)
    
    apagar_pdfs(PASTA_UPLOAD, arquivos)
    
    return redirect('/')
    

@app.route("/download")
def download():

    nome_arquivo = session.get("relatorio")

    if not nome_arquivo:
        return redirect("/")

    caminho = os.path.join(PASTA_EXCEL, nome_arquivo)

    return send_file(
        caminho,
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(debug=True)


@app.route("/remover-excel")
def remover_excel():
    nome_arquivo = session.get("relatorio")
    
    caminho = os.path.join(PASTA_EXCEL, nome_arquivo) # type: ignore
    
    arquivo = Path(caminho)
    
    arquivo.unlink()
    
    apagar_excel_session()
    return redirect("/")  
    
    
    
    
