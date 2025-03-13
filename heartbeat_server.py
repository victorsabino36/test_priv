from flask import Flask
import psutil
import time
import logging
import requests

# Configuração do log
logging.basicConfig(filename='monitoramento_local.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Nome do processo do Recarga Fácil
PROCESSO_RECARGA_FACIL = "RecargaFacil.exe"  # Substitua pelo nome correto do processo

# Configuração do servidor Flask
app = Flask(__name__)

# URL da VM na nuvem para receber o heartbeat
CLOUD_MONITOR_URL = "http://SEU_IP_VM:5000/heartbeat"

# Função para verificar se o Recarga Fácil está rodando
def verificar_recarga_facil():
    for processo in psutil.process_iter(attrs=['pid', 'name']):
        if processo.info['name'] == PROCESSO_RECARGA_FACIL:
            logging.info("Recarga Fácil está rodando.")
            return True
    logging.error("🚨 Recarga Fácil não está rodando!")
    return False

# Rota para heartbeat (a VM do Google Cloud irá verificar esta rota)
@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return "OK", 200

# Loop para monitoramento contínuo
def enviar_heartbeat_para_vm():
    while True:
        try:
            requests.get(CLOUD_MONITOR_URL)
            logging.info("Heartbeat enviado para a VM.")
        except requests.ConnectionError:
            logging.error("🚨 Falha ao enviar heartbeat para a VM!")
        verificar_recarga_facil()
        time.sleep(60)  # Envia heartbeat a cada 1 minuto

if __name__ == "__main__":
    from threading import Thread
    Thread(target=enviar_heartbeat_para_vm).start()
    app.run(host="0.0.0.0", port=5000)
