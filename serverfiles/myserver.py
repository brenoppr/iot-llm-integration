from TTS.api import TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)

import google.generativeai as genai

genai.configure(api_key='')
model = genai.GenerativeModel('gemini-1.0-pro-latest')
chat = model.start_chat(history=[])

#Descrevendo para o modelo seu modo de operação
response = chat.send_message('''Você é um assistente virtual chamado Gilberto Gil com uma funcionalidade para acender uma lâmpada. Sempre que você receber um prompt com qualquer texto relacionado a acender a luz, responda apenas 'Acender.', e mais nenhuma outra palavra. Caso contrário, responda de acordo com as duas regras a seguir.
                             :Nunca gere listas em suas respostas.
                             :Suas respostas devem ser de no máximo 2 frases.''')
print(response.text) #puramente por debug


from flask import Flask, request, send_file
from flask_ngrok import run_with_ngrok
import os

app = Flask(__name__)
run_with_ngrok(app)  # Start ngrok when app is run
import locale
locale.getpreferredencoding = lambda: "UTF-8"

os.environ['NGROK_AUTHTOKEN'] = ''

import re
def mytts(response):
  pattern = r'[^a-zA-Z0-9\sáéíóúâêîôûàèìòùãẽĩõũç,.!?-]'
  clean_response = re.sub(pattern, '', response)
  tts.tts_to_file(text=clean_response,
            file_path="output.wav",
            speaker_wav=["/mnt/my-volume-1/sounds/gilberto.wav"],
            language="pt",
            split_sentences=True
            )
  return "output.wav"

  def run(text):
  response = chat.send_message(text)
  print(response.text)
  audio_file = mytts(response.text)
  return audio_file

  from flask import Flask, request, send_file

app = Flask(__name__)

@app.route('/output.mp3', methods=['GET'])
def get_mp3():
    # Extract 'text' from the query parameters
    text = request.args.get('text')

    if not text:
        return "Missing 'text' parameter", 400

    # Call the run(text) function to generate the mp3 file
    print("Received text:", text)
    audio_file = run(text)
    #audio_file="/content/drive/MyDrive/TelecomVozes/arquivo1.mp3"
    print("Generated audio file:", audio_file)
    # Send the generated mp3 file as a response
    if os.path.exists(audio_file):
        return send_file(audio_file, mimetype='audio/mpeg')
    else:
        return "Audio file not found", 404

import ngrok
listener = ngrok.forward("localhost:5000", authtoken_from_env=True, domain="kid-relative-polecat.ngrok-free.app")

if __name__ == "__main__":
    app.run(port=5000)
