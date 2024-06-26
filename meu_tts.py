
# Inicializando biblioteca
import re
from playsound import playsound
import requests
import winsound





i = 0
def remove_special_characters(text):
    # Expressão regular para encontrar caracteres especiais
    pattern = r'[^a-zA-Z0-9\sáéíóúâêîôûàèìòùãẽĩõũç,.!?-]'  # Irá manter letras com acentos, números, espaços e pontuações

    # Substituir os caracteres especiais por uma string vazia
    clean_text = re.sub(pattern, '', text)

    return clean_text


def main(mystring):
    global i
    mystring = remove_special_characters(mystring)
    # Use the public URL from the ngrok output
    colab_url = 'https://40ca-34-124-133-182.ngrok-free.app/run'

    data = {'input': mystring}  # Example input string
    response = requests.post(colab_url, json=data)

    # Save the wav file
    with open(f'output{i}.wav', 'wb') as f:
        f.write(response.content)


    filename = f'output{i}.wav'
    winsound.PlaySound(filename, winsound.SND_FILENAME)
    i += 1
