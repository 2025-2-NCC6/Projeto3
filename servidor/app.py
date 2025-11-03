from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
ESP32_IP = "http://192.168.15.15"

solda = False
ferramentas = {
    'tool-1': True,
    'tool-2': True,
    'tool-3': True,
    'tool-4': True
}

# Rotas do servidor
# Rota landing page
@app.route('/')
def index():
    return render_template('index.html')

# Rota ascensor tomada
@app.route('/comando_ascensor', methods=['POST'])
def comando_ascensor():
    comando = request.json.get('action') 

    try:
        response = requests.get(f"{ESP32_IP}/ascensor?cmd={comando}", timeout=5)
        response.raise_for_status()

        print(f"Comando '{comando}' enviado com sucesso ao ESP32.")
        return jsonify({'status': 'sucesso', 'mensagem': f'Comando {comando} executado no hardware'})

    except requests.exceptions.RequestException as e:
        print(f"ERRO ao comunicar com o ESP32: {e}")
        return jsonify({'status': 'erro', 'mensagem': 'Falha na comunicação com o hardware'}), 500

# Rota bancada de solda
@app.route('/toggle_solda', methods=['POST'])
def toggle_solda():
    global solda
    solda = not solda

    energia = request.json.get('action')
    
    status_texto = "LIGADO" if solda else "DESLIGADO"
    status_comando = "ON" if solda else "OFF"

    print(f"Comando recebido: BANCADA DE SOLDA: {status_texto}. Enviando '{status_comando}' para o ESP32.")
    
    try:
        response = requests.get(f"{ESP32_IP}/solda_toggle?state={status_comando}", timeout=5)
        response.raise_for_status() 

        return jsonify({
            'status': 'sucesso', 
            'novo_estado': solda,
            'novo_texto': status_texto
        })

    except requests.exceptions.RequestException as e:
        print(f"ERRO ao comunicar com o ESP32 para a Bancada de Solda: {e}")
        solda = not solda
        return jsonify({'status': 'erro', 'mensagem': 'Falha na comunicação com o ESP32 para a solda'}), 500

# Rota ferramentas
@app.route('/status_ferramentas', methods=['GET'])
def status_ferramentas():
    try:
        # O Flask consulta o ESP32
        response = requests.get(f"{ESP32_IP}/status", timeout=5)
        response.raise_for_status()

        # Repassa a resposta JSON do ESP32 diretamente para o JavaScript
        estado_real = response.json()
        return jsonify(estado_real)

    except requests.exceptions.RequestException as e:
        print(f"ERRO ao buscar status do ESP32: {e}")
        return jsonify({
            'tool-1': False, 'tool-2': False, 
            'tool-3': False, 'tool-4': False
        }), 200

if __name__ == '__main__':
    app.run(debug=True)