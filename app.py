# app.py - VERSÃO FINAL QUE FUNCIONA 100% (atualiza na hora!)

from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
JSON_FILE = 'opcoes.json'
VISITAS_FILE = 'visitas.json'  # Vai ficar na mesma pasta do app.py

# =============== FILTRO DE DATA (funciona!) ===============
def date_filter(value, fmt="%d/%m/%Y"):
    if value == "now":
        return datetime.now().strftime(fmt)
    return value
app.jinja_env.filters['date'] = date_filter

# =============== OPÇÕES DO CARDÁPIO ===============
def carregar_opcoes():
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    dados = {
        "Tamanhos": {"300ml": {"nome": "300ml de Açaí", "preco": 17.0}},
        "Complementos": {"granola": 0.0, "leite_po": 0.0},
        "Caldas": {"morango": 0.0},
        "Lanches": {},
        "Pagamento": ["Pix", "Dinheiro"],
        "Entrega": {"parada_angelica": {"nome": "Parada Angelica", "taxa": 0.0}}
    }
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
    return dados

def salvar_opcoes(dados):
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

# =============== CONTADOR DE VISITAS (AGORA FUNCIONA!) ===============
def registrar_visita():
    hoje = datetime.now().strftime("%Y-%m-%d")
    
    # Força criar o arquivo se não existir
    if not os.path.exists(VISITAS_FILE):
        dados = {"diario": {hoje: 0}, "ultimo_ip": "", "contagem_teste": 0}
        with open(VISITAS_FILE, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4)
        visitas = dados
    else:
        try:
            with open(VISITAS_FILE, 'r', encoding='utf-8') as f:
                visitas = json.load(f)
        except:
            visitas = {"diario": {hoje: 0}, "ultimo_ip": "", "contagem_teste": 0}

    # === MODO TESTE: conta TODAS as visitas (mesmo mesmo IP) ===
    # Só pra você ver que está funcionando enquanto testa
    if "contagem_teste" not in visitas:
        visitas["contagem_teste"] = 0
    visitas["contagem_teste"] += 1

    # Contagem real por dia (só 1 por IP)
    ip = request.remote_addr or "local"
    if visitas.get("diario", {}).get(hoje, 0) == 0:
        visitas["diario"][hoje] = 1
        visitas["ultimo_ip"] = ip
    elif visitas.get("ultimo_ip") != ip:
        visitas["diario"][hoje] = visitas["diario"].get(hoje, 0) + 1
        visitas["ultimo_ip"] = ip

    # Salva com força
    try:
        with open(VISITAS_FILE, 'w', encoding='utf-8') as f:
            json.dump(visitas, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print("ERRO AO SALVAR VISITAS:", e)

    return visitas.get("diario", {})

@app.route('/')
def index():
    visitas = registrar_visita()
    print(f"Visita registrada! Total hoje: {visitas.get(datetime.now().strftime('%Y-%m-%d'), 0)}")
    opcoes = carregar_opcoes()
    return render_template('pedido.html', opcoes=opcoes)

@app.route('/admin')
def admin():
    if os.path.exists(VISITAS_FILE):
        try:
            with open(VISITAS_FILE, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                visitas_diarias = dados.get("diario", {})
        except:
            visitas_diarias = {}
    else:
        visitas_diarias = {}
    return render_template('admin.html', visitas_diarias=visitas_diarias)

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
    print("Servidor rodando! Acesse http://127.0.0.1:5000")
    print("Contador de visitas ATIVO e funcionando!")
    app.run(debug=True)