from flask import Flask, request, jsonify
from collections import defaultdict
import logging
import os

# Configuração do Flask
app = Flask(__name__)

# Configuração de logging para depuração
logging.basicConfig(level=logging.DEBUG)

# Função de otimização de cortes
def first_fit_decreasing(bar_length, cuts, cut_loss):
    cuts_sorted = sorted(cuts.items(), key=lambda x: x[0], reverse=True)
    bars = []
    for length, qty in cuts_sorted:
        for _ in range(qty):
            placed = False
            for bar in bars:
                if sum(bar) + length + cut_loss <= bar_length:
                    bar.append(length)
                    placed = True
                    break
            if not placed:
                bars.append([length])
    return bars

# Endpoint de otimização
@app.route('/optimize', methods=['POST'])
def optimize():
    try:
        # Log da requisição recebida
        app.logger.debug("Recebendo requisição...")
        data = request.json
        app.logger.debug(f"Payload recebido: {data}")

        # Validação dos dados
        if not data or not all(k in data for k in ['bar_length', 'cut_loss', 'cuts']):
            return jsonify({"error": "Faltam parâmetros obrigatórios"}), 400

        # Parâmetros de entrada
        bar_length = int(data['bar_length'])
        cut_loss = int(data['cut_loss'])
        cuts = defaultdict(int, {int(k): int(v) for k, v in data['cuts'].items()})

        # Executa a lógica de otimização
        bars = first_fit_decreasing(bar_length, cuts, cut_loss)

        # Retorna os resultados
        return jsonify({
            "bars": bars,
            "total_bars": len(bars)
        })
    except Exception as e:
        app.logger.error(f"Erro durante a otimização: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Configuração para rodar no Render
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
