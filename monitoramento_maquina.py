import requests
import time
import logging

# Configuração do log
logging.basicConfig(filename='monitoramento.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# URL para verificar a conexão
URL = "https://www.google.com"

# Função para verificar a conexão com a internet
def verificar_conexao():
    try:
        response = requests.get(URL, timeout=5)
        if response.status_code == 200:
            logging.info("Conexão com a internet estável.")
            return True
    except requests.ConnectionError:
        logging.error("Falha na conexão com a internet.")
        enviar_alerta()
        return False

# Função para enviar alerta (exemplo com Telegram)
def enviar_alerta():
    # Substitua pelo token do seu bot e chat_id
    token = "SEU_BOT_TOKEN"
    chat_id = "SEU_CHAT_ID"
    mensagem = "🚨 Alerta: A conexão com a internet caiu!"

    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={mensagem}"
    try:
        requests.get(url)
        logging.info("Alerta enviado com sucesso!")
    except Exception as e:
        logging.error(f"Erro ao enviar alerta: {e}")

# Loop para monitoramento contínuo
while True:
    verificar_conexao()
    time.sleep(60)  # Verifica a cada 1 minuto
