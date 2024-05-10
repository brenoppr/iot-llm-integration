
# Inicializando biblioteca
import pyttsx3
import re
def remove_special_characters(text):
    # Expressão regular para encontrar caracteres especiais
    pattern = r'[^a-zA-Z0-9\sáéíóúâêîôûàèìòùãẽĩõũç,.!?-]'  # Irá manter letras com acentos, números, espaços e pontuações

    # Substituir os caracteres especiais por uma string vazia
    clean_text = re.sub(pattern, '', text)

    return clean_text

def main(string):
  nstring = remove_special_characters(string)
  speaker=pyttsx3.init()

#   Definindo atributos:
#    Lingua: portugues do Brasil
#    Velocidade: padrao (200) -45
  speaker.setProperty('voice', 'brazil')
  rate = speaker.getProperty('rate')
  speaker.setProperty('rate', rate+50)

# Passando texto a ser dito e executando
  speaker.say(nstring)
  speaker.runAndWait()
