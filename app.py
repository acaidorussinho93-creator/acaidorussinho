# app.py
from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)
JSON_FILE = 'opcoes.json'

def carregar_opcoes():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        dados = {
            "Tamanhos": {"300ml": {"nome": "300ml de Açaí", "preco": 17.0}},
            "Complementos": {"granola": 0.0, "leite_po": 0.0},
            "Caldas": {"morango": 0.0},
            "Lanches": {},
            "Pagamento": ["Pix", "Dinheiro"],
            "Entrega": {"parada_angelica": {"nome": "Parada Angelica", "taxa": 0.0}}
        }
        salvar_opcoes(dados)
        return dados

def salvar_opcoes(dados):
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    opcoes = carregar_opcoes()
    return render_template('pedido.html', opcoes=opcoes)

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/api/opcoes')
def api_opcoes():
    return jsonify(carregar_opcoes())

@app.route('/admin/salvar', methods=['POST'])
def salvar_admin():
    dados = request.get_json()
    if dados:
        salvar_opcoes(dados)
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 400

if __name__ == '__main__':
    app.run(debug=True)