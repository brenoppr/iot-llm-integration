
import meu_reconhecimento
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
import meu_tts
import clicker
import apikey
#importante: Executar como administrador ou a função de clicar na tela não funciona

#Inicializando o modelo e iniciando o chat
genai.configure(api_key=apikey.mygoogleapikey)
model = genai.GenerativeModel('gemini-1.0-pro-latest')
chat = model.start_chat(history=[])

#Descrevendo para o modelo seu modo de operação
response = chat.send_message('''Você é uma assistente pessoal com uma funcionalidade para acender uma lâmpada. Sempre que você receber um prompt com qualquer texto relacionado a acender a luz, responda apenas 'Acender.', e mais nenhuma outra palavra. Caso contrário, responda de acordo com as duas regras a seguir. 
                             :Nunca gere listas em suas respostas. 
                             :Suas respostas devem ser de no máximo 3 frases.''')
print(response.text) #puramente por debug



while True:
  conteudo = meu_reconhecimento.ouvir_e_armazenar() #Escuta o comando
  if conteudo == None:
    continue
  print("Você disse:", conteudo) #novamente opcional, pelo debug
  response = chat.send_message(conteudo) #enviando para o modelo
  if response.text == "Acender.": #lógica de acender a lâmpada
    lampada_acesa = 1
    meu_tts.main("Ok, vou acender a lâmpada")
    clicker.click(1429, 947)
    continue
  else:
    meu_tts.main(response.text) #na função do TTS, arquivo é sanitizado para caracteres especiais


