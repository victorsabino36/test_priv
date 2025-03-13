from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import yt_dlp
import whisper
import ffmpeg
import pandas as pd
from google.cloud import bigquery
from flask_cors import CORS

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/ymendes/projects/converter-backend/credenciais_bigquery.json"
 
load_dotenv() 
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
client = bigquery.Client()

@app.route('/get-all-crime', methods=['GET'])
def getAllCrime():
  name = request.args.get('name')
  limit = request.args.get('limit')

  if not name:
    return jsonify({"error": "A propriedade 'name' é obrigatória" }), 400

  try:
    limit = int(limit)
  except:
    return jsonify({"error": "O 'limit' deve ser um número inteiro." })

  if limit < 1 or limit > 10:
    return jsonify({"error": "O limite deve ser entre 1 e 10"}), 400

  try:
    query = f"""
    SELECT primary_type, case_number
    FROM `bigquery-public-data.chicago_crime.crime`
    WHERE  primary_type = '{name}'
    LIMIT {limit}
    """

    df = client.query(query).to_dataframe()
    if df.empty:
      return jsonify({"error": "Nenhum crime encontrado com o nome especificado."}), 404

    return jsonify(df.to_dict(orient="records")), 200
  
  except Exception as e:
    print(f"Erro: {e}")
    return jsonify({"error": str(e)}), 500

@app.route('/get-all-distinct', methods=['GET'])
def getAllCrime_distinct():
  
  try:
    query = f"""
    SELECT DISTINCT primary_type
    FROM `bigquery-public-data.chicago_crime.crime`
    ORDER BY primary_type
    LIMIT 20
    """

    df = client.query(query).to_dataframe()    
    return jsonify(df.to_dict(orient="records")), 200
  
  except Exception as e:
    print(f"Erro: {e}")
    return jsonify({"error": str(e)}), 500

@app.route('/get-all-count', methods=['GET'])
def getAllCrime_count():
  name = request.args.get('name')
  try:
    query = f"""
    SELECT primary_type, COUNT(*) AS total_casos
    FROM `bigquery-public-data.chicago_crime.crime`
    WHERE primary_type = '{name}'
    GROUP BY primary_type
    ORDER BY total_casos DESC
    LIMIT 20
    """

    df = client.query(query).to_dataframe()  
    return jsonify(df.to_dict(orient="records")), 200
  
  except Exception as e:
    print(f"Erro: {e}")
    return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
  app.run(debug=True)