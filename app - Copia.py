from flask import Flask, render_template

app = Flask(__name__)

OPCOES = {
    "Tamanhos": {
        "1": {"nome": "300ml", "preco": 17}
        
    },
    "Complementos": {
        "granola": 0, "leite_pÓ": 0, "Choco-bool": 0, "Amendoim": 0, "Sucrilho": 0, "Paçoca": 0
    },
    "Caldas": {
        "Morango": 0, "Menta": 0, "chocolate": 0, "Uva": 0, "Manga": 0,
    },
    "Lanches": {
        "misto_quente": {"nome": "Clássico simples + Ykó", "preco": 10},
        # Preço modificado: 0 -> 8.50
        "sanduiche_natural": {"nome": "Sanduíche Natural", "preco": 8.50},
        # Preço modificado: 0 -> 7.00
        "salgado_frango": {"nome": "Salgado de Frango", "preco": 7.00},
        # Preço modificado: 0 -> 4.50
        "pao_queijo": {"nome": "Pão de Queijo", "preco": 4.50}
    },
    "Pagamento": ["Cartão de Crédito/Débito", "Pix", "Dinheiro (Traga Troco?)"]
}

@app.route('/')
def index():
    # Certifique-se de que você tem um template chamado 'pedido.html' no diretório 'templates/'
    return render_template('pedido.html', opcoes=OPCOES)

if __name__ == '__main__':
    # 'debug=True' é ótimo para desenvolvimento
    app.run(debug=True)