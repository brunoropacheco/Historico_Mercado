from flask import Flask, render_template, request, redirect, url_for, flash
import os
import sys
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Adicionar o diretório raiz ao PYTHONPATH
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.controllers.process_controller import buscar_itens_por_termo, buscar_compras_recentes, obter_detalhes_compra

app = Flask(__name__, 
           template_folder=os.path.join('src', 'views', 'templates'),
           static_folder=os.path.join('src', 'views', 'static'))

@app.route('/')
def index():
    """Página inicial com formulário de busca e compras recentes"""
    resultado = buscar_compras_recentes(limit=10)
    
    if resultado['success']:
        compras_recentes = resultado['compras']
    else:
        compras_recentes = []
        if 'error' in resultado:
            logger.error(f"Erro ao buscar compras recentes: {resultado['error']}")
    
    return render_template('index.html', compras_recentes=compras_recentes)

@app.route('/buscar')
def buscar():
    """Busca itens de compra pela descrição"""
    termo = request.args.get('termo', '')
    
    if not termo:
        return redirect(url_for('index'))
    
    resultado = buscar_itens_por_termo(termo)
    
    if resultado['success']:
        itens = resultado['itens']
    else:
        itens = []
        if 'error' in resultado:
            logger.error(f"Erro na busca: {resultado['error']}")
    
    return render_template('resultados.html', termo=termo, itens=itens)

@app.route('/compra/<int:compra_id>')
def detalhes_compra(compra_id):
    """Exibe detalhes de uma compra específica"""
    resultado = obter_detalhes_compra(compra_id)
    
    if resultado['success']:
        compra = resultado['compra']
        return render_template('detalhes_compra.html', compra=compra)
    else:
        flash(f"Erro ao buscar detalhes da compra: {resultado.get('error', 'Compra não encontrada')}")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = os.environ.get('SECRET_KEY', 'desenvolvimento-secreto')
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=5000, debug=debug)