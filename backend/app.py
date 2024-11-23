from flask import Flask, request, jsonify
from collections import defaultdict
import logging
import os

# Configuração do Flask
app = Flask(__name__)

# Configuração de logging para produção e desenvolvimento
logging.basicConfig(level=logging.DEBUG if os.environ.get("FLASK_ENV") == "development" else logging.INFO)

# Função de otimização de cortes
def first_fit_decreasing(bar_length, cuts, cut_loss):
    # Ordena os cortes em ordem decrescente
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

# Endpoint principal para otimização
@app.route('/optimize', methods=['POST'])
def optimize():
    try:
        # Log da requisição recebida
        app.logger.debug("Recebendo requisição de otimização...")
        data = request.json
        app.logger.debug(f"Payload recebido: {data}")

        # Validação dos dados recebidos
        if not data or not all(k in data for k in ['bar_length', 'cut_loss', 'cuts']):
            return jsonify({"error": "Faltam parâmetros obrigatórios (bar_length, cut_loss, cuts)"}), 400

        # Extração e validação dos parâmetros
        bar_length = int(data['bar_length'])
        cut_loss = int(data['cut_loss'])
        cuts = defaultdict(int, {int(k): int(v) for k, v in data['cuts'].items()})

        # Chamada da lógica de otimização
        bars = first_fit_decreasing(bar_length, cuts, cut_loss)

        # Retorno da resposta
        return jsonify({
            "bars": bars,
            "total_bars": len(bars)
        })
    except Exception as e:
        app.logger.error(f"Erro durante a otimização: {str(e)}")
        return jsonify({"error": "Erro interno no servidor"}), 500

# Health check (opcional, útil para monitoramento)
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

# Configuração do ambiente de execução
if __name__ == "__main__":
    # Configuração da porta dinâmica para Render ou padrão para local
    port = int(os.environ.get("PORT", 5000))
    
    # Verificar ambiente
    env = os.environ.get("FLASK_ENV", "production")
    debug_mode = env == "development"

    # Logs adicionais para depuração
    app.logger.info(f"Iniciando o servidor no modo {env}. Escutando em 0.0.0.0:{port}")

    # Inicializar o servidor Flask (usado apenas para desenvolvimento local)
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
