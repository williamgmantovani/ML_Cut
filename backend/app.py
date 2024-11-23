from flask import Flask, request, jsonify
from collections import defaultdict
import os

app = Flask(__name__)

# Função de otimização
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

@app.route('/optimize', methods=['POST'])
def optimize():
    try:
        # Recebe os dados da requisição
        data = request.json
        bar_length = int(data['bar_length'])
        cut_loss = int(data['cut_loss'])
        cuts = defaultdict(int, {int(k): int(v) for k, v in data['cuts'].items()})

        # Executa a lógica de otimização
        bars = first_fit_decreasing(bar_length, cuts, cut_loss)
        return jsonify({
            "bars": bars,
            "total_bars": len(bars)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render fornece a porta pelo ambiente
    app.run(host="0.0.0.0", port=port, debug=False)  # Desative o debug para produção
